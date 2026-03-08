from rest_framework import serializers
from .models import WalletTransaction


class WalletTransactionSerializer(serializers.ModelSerializer):
    order_id = serializers.UUIDField(source='order.id', read_only=True)

    class Meta:
        model = WalletTransaction
        fields = ['id', 'order_id', 'amount', 'transaction_type',
                  'status', 'description', 'settled_at', 'created_at']