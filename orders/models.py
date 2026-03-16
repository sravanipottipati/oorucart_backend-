from django.db import models
from users.models import User
from vendors.models import Vendor, Product
import uuid


class Order(models.Model):
    STATUS_CHOICES = (
        ('placed',     'Placed'),
        ('accepted',   'Accepted'),
        ('rejected',   'Rejected'),
        ('preparing',  'Preparing'),
        ('dispatched', 'Dispatched'),
        ('delivered',  'Delivered'),
        ('cancelled',  'Cancelled'),
    )
    PAYMENT_CHOICES = (
        ('cod',    'Cash on Delivery'),
        ('online', 'Online Payment'),
    )
    id               = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    buyer            = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    vendor           = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='orders')
    status           = models.CharField(max_length=20, choices=STATUS_CHOICES, default='placed')
    total_amount     = models.DecimalField(max_digits=10, decimal_places=2)
    platform_fee     = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    delivery_address = models.TextField()
    instructions     = models.TextField(blank=True, null=True)
    payment_mode     = models.CharField(max_length=10, choices=PAYMENT_CHOICES, default='cod')
    created_at       = models.DateTimeField(auto_now_add=True)
    updated_at       = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order {self.id} — {self.buyer.full_name} from {self.vendor.shop_name}"


class OrderItem(models.Model):
    id       = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order    = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product  = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price    = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"{self.product.name} x{self.quantity}"


class Notification(models.Model):
    TYPE_CHOICES = (
        ('order_placed',     'Order Placed'),
        ('order_accepted',   'Order Accepted'),
        ('order_rejected',   'Order Rejected'),
        ('order_preparing',  'Order Preparing'),
        ('order_dispatched', 'Order Dispatched'),
        ('order_delivered',  'Order Delivered'),
        ('order_cancelled',  'Order Cancelled'),
        ('new_order',        'New Order'),
        ('settlement',       'Settlement'),
    )
    id         = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user       = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    type       = models.CharField(max_length=30, choices=TYPE_CHOICES)
    title      = models.CharField(max_length=200)
    message    = models.TextField()
    order      = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True)
    is_read    = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.full_name} - {self.title}"


class Review(models.Model):
    id         = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order      = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='review')
    buyer      = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='reviews')
    vendor     = models.ForeignKey('vendors.Vendor', on_delete=models.CASCADE, related_name='reviews')
    rating     = models.IntegerField(default=5)
    comment    = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        from django.db.models import Avg
        avg   = Review.objects.filter(vendor=self.vendor).aggregate(Avg('rating'))['rating__avg']
        count = Review.objects.filter(vendor=self.vendor).count()
        self.vendor.rating       = round(avg, 1)
        self.vendor.total_reviews = count
        self.vendor.save()

    def __str__(self):
        return f"{self.buyer.full_name} → {self.vendor.shop_name} ({self.rating}★)"


# ─── CART MODEL ───────────────────────────────────────────────────────────────
class Cart(models.Model):
    id         = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    buyer      = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart_items')
    product    = models.ForeignKey(Product, on_delete=models.CASCADE)
    vendor     = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='cart_items')
    quantity   = models.PositiveIntegerField(default=1)
    added_at   = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('buyer', 'product')
        ordering        = ['-added_at']

    def __str__(self):
        return f"{self.buyer.full_name} - {self.product.name} x{self.quantity}"

    @property
    def subtotal(self):
        return self.product.price * self.quantity