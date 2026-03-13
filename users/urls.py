from django.urls import path
from .views import (RegisterView, LoginView, ProfileView,
                    AddressListView, AddressDetailView, SetDefaultAddressView)
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('register/',                           RegisterView.as_view(),          name='register'),
    path('login/',                              LoginView.as_view(),             name='login'),
    path('profile/',                            ProfileView.as_view(),           name='profile'),
    path('token/refresh/',                      TokenRefreshView.as_view(),      name='token_refresh'),
    path('addresses/',                          AddressListView.as_view(),       name='addresses'),
    path('addresses/<uuid:address_id>/',        AddressDetailView.as_view(),     name='address-detail'),
    path('addresses/<uuid:address_id>/default/', SetDefaultAddressView.as_view(), name='address-default'),
]