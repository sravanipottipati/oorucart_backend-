from django.http import HttpResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from orders.models import Order

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def buyer_invoice(request, order_id):
    from .invoice_generator import generate_buyer_invoice
    try:
        order = Order.objects.get(id=order_id, buyer=request.user)
    except Order.DoesNotExist:
        return Response({'error': 'Order not found'}, status=404)
    buffer = generate_buyer_invoice(order)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="invoice_{str(order.id)[:8].upper()}.pdf"'
    return response

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def commission_invoice(request, order_id):
    from .invoice_generator import generate_commission_invoice
    try:
        vendor = request.user.vendor
        order = Order.objects.get(id=order_id, vendor=vendor)
    except Exception:
        return Response({'error': 'Order not found'}, status=404)
    buffer = generate_commission_invoice(order)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="commission_{str(order.id)[:8].upper()}.pdf"'
    return response
