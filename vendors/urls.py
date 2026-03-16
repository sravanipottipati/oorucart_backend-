from django.urls import path
from .views import (VendorRegisterView, NearbyShopsView,
                    ShopDetailView, AddProductView,
                    ShopProductsView, MyShopView, ToggleShopView,
                    EditProductView, SearchView, WishlistView,
                    ProductVariantView, EditVariantView)

urlpatterns = [
    # ─── VENDOR ───────────────────────────────────────────────────────────────
    path('register/',                                VendorRegisterView.as_view(),  name='vendor-register'),
    path('nearby/',                                  NearbyShopsView.as_view(),     name='nearby-shops'),
    path('myshop/',                                  MyShopView.as_view(),          name='my-shop'),
    path('toggle/',                                  ToggleShopView.as_view(),      name='toggle-shop'),

    # ─── SEARCH & WISHLIST ────────────────────────────────────────────────────
    path('search/',                                  SearchView.as_view(),          name='search'),
    path('wishlist/',                                WishlistView.as_view(),        name='wishlist'),

    # ─── PRODUCTS ─────────────────────────────────────────────────────────────
    path('products/add/',                            AddProductView.as_view(),      name='add-product'),
    path('products/<uuid:product_id>/',              EditProductView.as_view(),     name='edit-product'),

    # ─── PRODUCT VARIANTS ─────────────────────────────────────────────────────
    path('products/<uuid:product_id>/variants/',     ProductVariantView.as_view(),  name='product-variants'),
    path('variants/<uuid:variant_id>/',              EditVariantView.as_view(),     name='edit-variant'),

    # ─── SHOP ─────────────────────────────────────────────────────────────────
    path('<uuid:vendor_id>/',                        ShopDetailView.as_view(),      name='shop-detail'),
    path('<uuid:vendor_id>/products/',               ShopProductsView.as_view(),    name='shop-products'),
]