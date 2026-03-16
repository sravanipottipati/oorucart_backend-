from django.contrib import admin
from .models import Vendor, Product, ProductVariant


# ─── PRODUCT VARIANT INLINE ───────────────────────────────────────────────────
class ProductVariantInline(admin.TabularInline):
    model       = ProductVariant
    extra       = 1
    fields      = ['name', 'price', 'stock_quantity', 'is_available']
    show_change_link = True


# ─── PRODUCT INLINE ───────────────────────────────────────────────────────────
class ProductInline(admin.TabularInline):
    model  = Product
    extra  = 0
    fields = ['name', 'price', 'category', 'is_available']
    show_change_link = True


# ─── VENDOR ADMIN ─────────────────────────────────────────────────────────────
@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display   = ['shop_name', 'category', 'town', 'status', 'is_open', 'rating', 'created_at']
    list_filter    = ['status', 'category', 'town', 'is_open']
    search_fields  = ['shop_name', 'town']
    list_editable  = ['status', 'is_open']
    inlines        = [ProductInline]


# ─── PRODUCT ADMIN ────────────────────────────────────────────────────────────
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display   = ['name', 'vendor', 'price', 'category', 'is_available', 'created_at']
    list_filter    = ['category', 'is_available', 'vendor']
    search_fields  = ['name', 'vendor__shop_name']
    list_editable  = ['price', 'is_available']
    inlines        = [ProductVariantInline]


# ─── PRODUCT VARIANT ADMIN ────────────────────────────────────────────────────
@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display  = ['product', 'name', 'price', 'stock_quantity', 'is_available']
    list_filter   = ['is_available']
    search_fields = ['product__name', 'name']
    list_editable = ['price', 'stock_quantity', 'is_available']