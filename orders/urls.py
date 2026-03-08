from django.urls import path
from .views import (PlaceOrderView, BuyerOrdersView,
                    VendorOrdersView, UpdateOrderStatusView,
                    OrderDetailView)

urlpatterns = [
    path('place/', PlaceOrderView.as_view(), name='place-order'),
    path('mine/', BuyerOrdersView.as_view(), name='buyer-orders'),
    path('vendor/', VendorOrdersView.as_view(), name='vendor-orders'),
    path('<uuid:order_id>/', OrderDetailView.as_view(), name='order-detail'),
    path('<uuid:order_id>/status/', UpdateOrderStatusView.as_view(), name='update-status'),
]