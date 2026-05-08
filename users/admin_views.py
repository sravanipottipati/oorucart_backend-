from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Sum, Count
from datetime import datetime
from orders.models import Order
from users.models import User

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def admin_stats(request):
    if not request.user.user_type == 'admin':
        return Response({'error': 'Admin access required'}, status=403)

    month = int(request.GET.get('month', datetime.now().month))
    year  = int(request.GET.get('year', datetime.now().year))

    # All time stats
    total_orders   = Order.objects.count()
    total_revenue  = Order.objects.filter(status='delivered').aggregate(Sum('total_amount'))['total_amount__sum'] or 0
    total_vendors  = User.objects.filter(user_type='vendor').count()
    total_buyers   = User.objects.filter(user_type='buyer').count()

    # This month stats
    month_orders  = Order.objects.filter(created_at__month=month, created_at__year=year).count()
    month_revenue = Order.objects.filter(status='delivered', created_at__month=month, created_at__year=year).aggregate(Sum('total_amount'))['total_amount__sum'] or 0
    month_delivered = Order.objects.filter(status='delivered', created_at__month=month, created_at__year=year).count()
    month_cancelled = Order.objects.filter(status='cancelled', created_at__month=month, created_at__year=year).count()
    month_pending   = Order.objects.filter(status='pending', created_at__month=month, created_at__year=year).count()

    # Commission this month
    month_commission = Order.objects.filter(status='delivered', created_at__month=month, created_at__year=year).aggregate(Sum('commission_amount'))['commission_amount__sum'] or 0
    month_tcs        = Order.objects.filter(status='delivered', created_at__month=month, created_at__year=year).aggregate(Sum('tcs_amount'))['tcs_amount__sum'] or 0

    return Response({
        'all_time': {
            'total_orders':  total_orders,
            'total_revenue': float(total_revenue),
            'total_vendors': total_vendors,
            'total_buyers':  total_buyers,
        },
        'this_month': {
            'month':           month,
            'year':            year,
            'total_orders':    month_orders,
            'total_revenue':   float(month_revenue),
            'delivered':       month_delivered,
            'cancelled':       month_cancelled,
            'pending':         month_pending,
            'commission':      float(month_commission),
            'tcs':             float(month_tcs),
        }
    })
