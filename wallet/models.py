from django.db import models
from vendors.models import Vendor
from orders.models import Order
import uuid


class WalletTransaction(models.Model):
    TYPE_CHOICES = (
        ('debit', 'Debit'),
        ('credit', 'Credit'),
    )

    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('settled', 'Settled'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='transactions')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    transaction_type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    description = models.TextField()
    settled_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.transaction_type} ₹{self.amount} — {self.vendor.shop_name} ({self.status})"