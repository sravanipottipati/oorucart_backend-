from django.urls import path
from . import views

urlpatterns = [
    path('buyer/<uuid:order_id>/',           views.buyer_invoice,            name='buyer-invoice'),
    path('commission/<uuid:order_id>/',      views.commission_invoice,       name='commission-invoice'),
    path('seller/<uuid:order_id>/',          views.seller_dashboard_invoice, name='seller-invoice'),
    path('settlement/',                      views.settlement_statement,     name='settlement'),
    path('tcs/',                             views.tcs_certificate,          name='tcs-certificate'),
]
