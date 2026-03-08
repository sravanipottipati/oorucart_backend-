from rest_framework import serializers
from .models import Vendor, Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 
                  'category', 'is_available', 'created_at']


class VendorSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = Vendor
        fields = ['id', 'shop_name', 'category', 'description',
                  'phone_number', 'address', 'town', 'delivery_type',
                  'estimated_delivery_time', 'rating', 'total_reviews',
                  'is_open', 'status', 'products', 'created_at']


class VendorRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = ['shop_name', 'category', 'description',
                  'phone_number', 'address', 'town',
                  'delivery_type', 'estimated_delivery_time']

    def create(self, validated_data):
        user = self.context['request'].user
        # Set platform fee based on category
        fee_map = {
            'vegetables': 5,
            'bakery': 7,
            'restaurant': 10,
            'supermarket': 7,
        }
        category = validated_data.get('category', 'other')
        platform_fee = fee_map.get(category, 7)
        vendor = Vendor.objects.create(
            user=user,
            platform_fee=platform_fee,
            **validated_data
        )
        return vendor


class AddProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'category', 'is_available']