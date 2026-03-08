from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import WalletTransaction
from .serializers import WalletTransactionSerializer
from vendors.models import Vendor
from orders.models import Order
from django.db.models import Sum
from django.utils import timezone
from datetime import timedelta


class WalletSummaryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            vendor = request.user.vendor
        except Exception:
            return Response(
                {'error': 'You do not have a shop'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Total pending fees (not yet settled)
        pending_fees = WalletTransaction.objects.filter(
            vendor=vendor,
            transaction_type='debit',
            status='pending'
        ).aggregate(total=Sum('amount'))['total'] or 0

        # Total settled fees (already paid to platform)
        settled_fees = WalletTransaction.objects.filter(
            vendor=vendor,
            transaction_type='debit',
            status='settled'
        ).aggregate(total=Sum('amount'))['total'] or 0

        # Total orders delivered
        total_orders = Order.objects.filter(
            vendor=vendor,
            status='delivered'
        ).count()

        return Response({
            'shop_name': vendor.shop_name,
            'platform_fee_per_order': vendor.platform_fee,
            'pending_fees': pending_fees,
            'settled_fees': settled_fees,
            'total_orders_delivered': total_orders,
            'message': f'You owe ₹{pending_fees} to OoruCart (pending settlement)'
        })


class WalletTransactionsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            vendor = request.user.vendor
        except Exception:
            return Response(
                {'error': 'You do not have a shop'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Optional filter by status
        filter_status = request.query_params.get('status', None)
        transactions = WalletTransaction.objects.filter(
            vendor=vendor
        ).order_by('-created_at')

        if filter_status:
            transactions = transactions.filter(status=filter_status)

        serializer = WalletTransactionSerializer(transactions, many=True)
        return Response({
            'count': transactions.count(),
            'transactions': serializer.data
        })


class WeeklyReportView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            vendor = request.user.vendor
        except Exception:
            return Response(
                {'error': 'You do not have a shop'},
                status=status.HTTP_400_BAD_REQUEST
            )

        today = timezone.now()
        week_ago = today - timedelta(days=7)

        weekly_orders = Order.objects.filter(
            vendor=vendor,
            created_at__gte=week_ago
        )

        delivered  = weekly_orders.filter(status='delivered').count()
        cancelled  = weekly_orders.filter(status='cancelled').count()
        rejected   = weekly_orders.filter(status='rejected').count()
        pending    = weekly_orders.filter(
            status__in=['placed', 'accepted', 'preparing', 'dispatched']
        ).count()

        # Revenue from delivered orders this week
        weekly_revenue = weekly_orders.filter(
            status='delivered'
        ).aggregate(total=Sum('total_amount'))['total'] or 0

        # Fees this week (pending + settled)
        weekly_fees = WalletTransaction.objects.filter(
            vendor=vendor,
            transaction_type='debit',
            created_at__gte=week_ago
        ).aggregate(total=Sum('amount'))['total'] or 0

        # Pending fees this week
        weekly_pending_fees = WalletTransaction.objects.filter(
            vendor=vendor,
            transaction_type='debit',
            status='pending',
            created_at__gte=week_ago
        ).aggregate(total=Sum('amount'))['total'] or 0

        return Response({
            'period': f"{week_ago.strftime('%d %b')} — {today.strftime('%d %b %Y')}",
            'shop_name': vendor.shop_name,
            'orders': {
                'total': weekly_orders.count(),
                'delivered': delivered,
                'cancelled': cancelled,
                'rejected': rejected,
                'pending': pending,
            },
            'financials': {
                'gross_revenue': weekly_revenue,
                'platform_fees_this_week': weekly_fees,
                'pending_fees_to_pay': weekly_pending_fees,
                'net_revenue': float(weekly_revenue) - float(weekly_fees),
            }
        })


class AdminSettlementView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Admin sees all vendors with pending fees
        if request.user.user_type != 'admin':
            return Response(
                {'error': 'Admin access only'},
                status=status.HTTP_403_FORBIDDEN
            )

        vendors = Vendor.objects.filter(status='approved')
        result = []

        for vendor in vendors:
            pending = WalletTransaction.objects.filter(
                vendor=vendor,
                transaction_type='debit',
                status='pending'
            ).aggregate(total=Sum('amount'))['total'] or 0

            settled = WalletTransaction.objects.filter(
                vendor=vendor,
                transaction_type='debit',
                status='settled'
            ).aggregate(total=Sum('amount'))['total'] or 0

            result.append({
                'vendor_id': str(vendor.id),
                'shop_name': vendor.shop_name,
                'town': vendor.town,
                'category': vendor.category,
                'pending_fees': pending,
                'settled_fees': settled,
            })

        total_pending = WalletTransaction.objects.filter(
            transaction_type='debit',
            status='pending'
        ).aggregate(total=Sum('amount'))['total'] or 0

        total_settled = WalletTransaction.objects.filter(
            transaction_type='debit',
            status='settled'
        ).aggregate(total=Sum('amount'))['total'] or 0

        return Response({
            'total_pending_collection': total_pending,
            'total_collected_so_far': total_settled,
            'vendors': result
        })

    def post(self, request):
        # Admin marks a vendor's pending fees as settled
        if request.user.user_type != 'admin':
            return Response(
                {'error': 'Admin access only'},
                status=status.HTTP_403_FORBIDDEN
            )

        vendor_id = request.data.get('vendor_id')
        if not vendor_id:
            return Response(
                {'error': 'vendor_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            vendor = Vendor.objects.get(id=vendor_id)
        except Vendor.DoesNotExist:
            return Response(
                {'error': 'Vendor not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        # Mark all pending transactions as settled
        pending_transactions = WalletTransaction.objects.filter(
            vendor=vendor,
            status='pending'
        )

        count = pending_transactions.count()
        total = pending_transactions.aggregate(
            total=Sum('amount')
        )['total'] or 0

        pending_transactions.update(
            status='settled',
            settled_at=timezone.now()
        )

        return Response({
            'message': f'Settlement done for {vendor.shop_name}',
            'transactions_settled': count,
            'total_amount_settled': total
        })