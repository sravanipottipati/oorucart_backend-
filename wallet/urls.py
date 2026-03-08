from django.urls import path
from .views import (WalletSummaryView, WalletTransactionsView,
                    WeeklyReportView, AdminSettlementView)

urlpatterns = [
    path('summary/', WalletSummaryView.as_view(), name='wallet-summary'),
    path('transactions/', WalletTransactionsView.as_view(), name='wallet-transactions'),
    path('report/', WeeklyReportView.as_view(), name='weekly-report'),
    path('admin/settlement/', AdminSettlementView.as_view(), name='admin-settlement'),
]