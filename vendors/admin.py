from django.contrib import admin
from .models import Vendor, Product

@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ['shop_name', 'category', 'town', 'status', 'is_open', 'created_at']
    list_filter = ['status', 'category', 'town']
    search_fields = ['shop_name', 'town']
    list_editable = ['status', 'is_open']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'vendor', 'price', 'category', 'is_available']
    list_filter = ['category', 'is_available']
    search_fields = ['name', 'vendor__shop_name']