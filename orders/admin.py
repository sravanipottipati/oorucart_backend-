from django.contrib import admin
from .models import Order, OrderItem, Notification, Review, Cart


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display  = ['id', 'buyer', 'vendor', 'status', 'total_amount', 'created_at']
    list_filter   = ['status', 'payment_mode']
    search_fields = ['buyer__full_name', 'vendor__shop_name']


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display  = ['order', 'product', 'quantity', 'price']
    search_fields = ['product__name']


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display  = ['user', 'title', 'type', 'is_read', 'created_at']
    list_filter   = ['type', 'is_read']
    search_fields = ['user__full_name', 'title']


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display  = ['buyer', 'vendor', 'rating', 'created_at']
    list_filter   = ['rating']
    search_fields = ['buyer__full_name', 'vendor__shop_name']


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display  = ['buyer', 'product', 'vendor', 'quantity', 'added_at']
    list_filter   = ['vendor']
    search_fields = ['buyer__full_name', 'product__name']
from .models import Coupon

@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display  = ['code', 'discount_type', 'discount_value', 'min_order', 'used_count', 'max_uses', 'valid_until', 'is_active']
    list_editable = ['is_active']
    search_fields = ['code']
