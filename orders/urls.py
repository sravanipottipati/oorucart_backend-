from django.urls import path
from .views import (PlaceOrderView, BuyerOrdersView,
                    VendorOrdersView, UpdateOrderStatusView,
                    OrderDetailView, NotificationListView,
                    MarkNotificationReadView, SubmitReviewView,
                    get_cart, add_to_cart, update_cart_item,
                    remove_from_cart, clear_cart,
                    ValidateCouponView)

urlpatterns = [
    # ─── ORDERS ───────────────────────────────────────────────────────────────
    path('place/',                               PlaceOrderView.as_view(),           name='place-order'),
    path('mine/',                                BuyerOrdersView.as_view(),          name='buyer-orders'),
    path('vendor/',                              VendorOrdersView.as_view(),         name='vendor-orders'),
    path('<uuid:order_id>/',                     OrderDetailView.as_view(),          name='order-detail'),
    path('<uuid:order_id>/status/',              UpdateOrderStatusView.as_view(),    name='update-status'),
    path('<uuid:order_id>/review/',              SubmitReviewView.as_view(),         name='submit-review'),

    # ─── NOTIFICATIONS ────────────────────────────────────────────────────────
    path('notifications/',                       NotificationListView.as_view(),     name='notifications'),
    path('notifications/read/',                  MarkNotificationReadView.as_view(), name='mark-all-read'),
    path('notifications/<uuid:notif_id>/read/',  MarkNotificationReadView.as_view(), name='mark-read'),

    # ─── CART ─────────────────────────────────────────────────────────────────
    path('cart/',                                get_cart,                           name='get-cart'),
    path('cart/add/',                            add_to_cart,                        name='add-to-cart'),
    path('cart/update/<uuid:item_id>/',          update_cart_item,                   name='update-cart'),
    path('cart/remove/<uuid:item_id>/',          remove_from_cart,                   name='remove-from-cart'),
    path('cart/clear/',                          clear_cart,                         name='clear-cart'),

    # ─── COUPON ───────────────────────────────────────────────────────────────
    path('coupon/validate/',                     ValidateCouponView.as_view(),       name='validate-coupon'),
]