from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Order, OrderItem
from .serializers import PlaceOrderSerializer, OrderSerializer
from vendors.models import Vendor, Product
from wallet.models import WalletTransaction
from django.utils import timezone


class PlaceOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.user.user_type != 'buyer':
            return Response(
                {'error': 'Only buyers can place orders'},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = PlaceOrderSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data

        try:
            vendor = Vendor.objects.get(id=data['vendor_id'], status='approved')
        except Vendor.DoesNotExist:
            return Response(
                {'error': 'Shop not found or not approved'},
                status=status.HTTP_404_NOT_FOUND
            )

        total_amount = 0
        order_items = []

        for item in data['items']:
            try:
                product = Product.objects.get(
                    id=item['product_id'],
                    vendor=vendor,
                    is_available=True
                )
                quantity = int(item['quantity'])
                price = product.price
                total_amount += price * quantity
                order_items.append({
                    'product': product,
                    'quantity': quantity,
                    'price': price
                })
            except Product.DoesNotExist:
                return Response(
                    {'error': f"Product {item['product_id']} not found"},
                    status=status.HTTP_404_NOT_FOUND
                )

        order = Order.objects.create(
            buyer=request.user,
            vendor=vendor,
            total_amount=total_amount,
            platform_fee=vendor.platform_fee,
            delivery_address=data['delivery_address'],
            instructions=data.get('instructions', ''),
            payment_mode=data.get('payment_mode', 'cod'),
            status='placed'
        )

        for item in order_items:
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                quantity=item['quantity'],
                price=item['price']
            )

        return Response({
            'message': 'Order placed successfully!',
            'order': OrderSerializer(order).data
        }, status=status.HTTP_201_CREATED)


class BuyerOrdersView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        orders = Order.objects.filter(
            buyer=request.user
        ).order_by('-created_at')
        serializer = OrderSerializer(orders, many=True)
        return Response({
            'count': orders.count(),
            'orders': serializer.data
        })


class VendorOrdersView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            vendor = request.user.vendor
        except Exception:
            return Response(
                {'error': 'You do not have a shop'},
                status=status.HTTP_400_BAD_REQUEST
            )
        orders = Order.objects.filter(
            vendor=vendor
        ).order_by('-created_at')
        serializer = OrderSerializer(orders, many=True)
        return Response({
            'count': orders.count(),
            'orders': serializer.data
        })


class UpdateOrderStatusView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, order_id):
        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return Response(
                {'error': 'Order not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        new_status = request.data.get('status')
        user = request.user

        # Vendor actions
        if user.user_type == 'vendor':
            try:
                vendor = user.vendor
            except Exception:
                return Response({'error': 'Not a vendor'}, status=400)

            if order.vendor != vendor:
                return Response(
                    {'error': 'This is not your order'},
                    status=status.HTTP_403_FORBIDDEN
                )

            allowed = ['accepted', 'rejected', 'preparing', 'dispatched', 'delivered']
            if new_status not in allowed:
                return Response(
                    {'error': f'Invalid status. Choose from: {allowed}'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Record fee as pending when order is accepted — no wallet deduction
            if new_status == 'accepted' and order.status == 'placed':
                WalletTransaction.objects.create(
                    vendor=order.vendor,
                    order=order,
                    amount=order.platform_fee,
                    transaction_type='debit',
                    status='pending',
                    description=f'Platform fee for order {order.id}'
                )

            order.status = new_status
            order.save()

            return Response({
                'message': f'Order status updated to {new_status}',
                'order': OrderSerializer(order).data
            })

        # Buyer can only cancel
        elif user.user_type == 'buyer':
            if order.buyer != user:
                return Response({'error': 'Not your order'}, status=403)
            if new_status != 'cancelled':
                return Response({'error': 'Buyers can only cancel orders'}, status=400)
            if order.status not in ['placed']:
                return Response(
                    {'error': 'Can only cancel orders that are just placed'},
                    status=400
                )
            order.status = 'cancelled'
            order.save()
            return Response({
                'message': 'Order cancelled',
                'order': OrderSerializer(order).data
            })

        return Response({'error': 'Unauthorized'}, status=403)


class OrderDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, order_id):
        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return Response({'error': 'Order not found'}, status=404)

        user = request.user
        if order.buyer != user and (
            not hasattr(user, 'vendor') or order.vendor != user.vendor
        ):
            return Response({'error': 'Unauthorized'}, status=403)

        return Response(OrderSerializer(order).data)