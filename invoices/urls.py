from django.urls import path
from . import views

urlpatterns = [
    path('buyer/<uuid:order_id>/', views.buyer_invoice, name='buyer-invoice'),
    path('commission/<uuid:order_id>/', views.commission_invoice, name='commission-invoice'),
]
