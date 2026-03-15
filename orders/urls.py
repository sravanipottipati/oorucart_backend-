from django.urls import path
from .views import (PlaceOrderView, BuyerOrdersView,
                    VendorOrdersView, UpdateOrderStatusView,
                    OrderDetailView, NotificationListView,
                    MarkNotificationReadView, SubmitReviewView)

urlpatterns = [
    path('place/',                               PlaceOrderView.as_view(),           name='place-order'),
    path('mine/',                                BuyerOrdersView.as_view(),          name='buyer-orders'),
    path('vendor/',                              VendorOrdersView.as_view(),         name='vendor-orders'),
    path('<uuid:order_id>/',                     OrderDetailView.as_view(),          name='order-detail'),
    path('<uuid:order_id>/status/',              UpdateOrderStatusView.as_view(),    name='update-status'),
    path('<uuid:order_id>/review/',              SubmitReviewView.as_view(),         name='submit-review'),
    path('notifications/',                       NotificationListView.as_view(),     name='notifications'),
    path('notifications/read/',                  MarkNotificationReadView.as_view(), name='mark-all-read'),
    path('notifications/<uuid:notif_id>/read/',  MarkNotificationReadView.as_view(), name='mark-read'),
]
