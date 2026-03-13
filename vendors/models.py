from django.db import models
from users.models import User
import uuid


class Vendor(models.Model):
    CATEGORY_CHOICES = (
        ('vegetables',  'Vegetables'),
        ('bakery',      'Bakery'),
        ('restaurant',  'Restaurant'),
        ('supermarket', 'Supermarket'),
    )
    DELIVERY_CHOICES = (
        ('delivery', 'Delivery'),
        ('pickup',   'Pickup'),
        ('both',     'Both'),
    )
    STATUS_CHOICES = (
        ('pending',  'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )
    id                      = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user                    = models.OneToOneField(User, on_delete=models.CASCADE, related_name='vendor')
    shop_name               = models.CharField(max_length=200)
    category                = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    description             = models.TextField(blank=True, null=True)
    phone_number            = models.CharField(max_length=10)
    address                 = models.TextField()
    town                    = models.CharField(max_length=100)
    delivery_type           = models.CharField(max_length=10, choices=DELIVERY_CHOICES, default='both')
    estimated_delivery_time = models.IntegerField(default=30)
    platform_fee            = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    wallet_balance          = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    rating                  = models.FloatField(default=0.0)
    total_reviews           = models.IntegerField(default=0)
    is_open                 = models.BooleanField(default=True)
    status                  = models.CharField(max_length=10, choices=STATUS_CHOICES, default='approved')
    created_at              = models.DateTimeField(auto_now_add=True)
    updated_at              = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.shop_name} ({self.town})"


class Product(models.Model):
    CATEGORY_CHOICES = (
        ('vegetables', 'Vegetables'),
        ('fruits',     'Fruits'),
        ('dairy',      'Dairy'),
        ('bakery',     'Bakery'),
        ('snacks',     'Snacks'),
        ('beverages',  'Beverages'),
        ('food',       'Food'),
        ('grocery',    'Grocery'),
        ('other',      'Other'),
    )
    id           = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    vendor       = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='products')
    name         = models.CharField(max_length=200)
    description  = models.TextField(blank=True, null=True)
    price        = models.DecimalField(max_digits=8, decimal_places=2)
    category     = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='other')
    is_available = models.BooleanField(default=True)
    created_at   = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.vendor.shop_name}"


class Wishlist(models.Model):
    id         = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user       = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wishlist')
    product    = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='wishlisted_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')

    def __str__(self):
        return f"{self.user.full_name} - {self.product.name}"
