from rest_framework import serializers
from .models import Vendor, Product
import math

def calculate_distance(lat1, lon1, lat2, lon2):
    """Calculate distance in km between two GPS coordinates using Haversine formula"""
    R = 6371  # Earth radius in km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat/2) ** 2 +
         math.cos(math.radians(lat1)) *
         math.cos(math.radians(lat2)) *
         math.sin(dlon/2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return round(R * c, 1)

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Product
        fields = ['id', 'name', 'description', 'price',
                  'category', 'is_available', 'created_at']

class VendorSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)
    distance = serializers.SerializerMethodField()

    class Meta:
        model  = Vendor
        fields = ['id', 'shop_name', 'category', 'description',
                  'phone_number', 'address', 'town',
                  'latitude', 'longitude',
                  'delivery_type', 'estimated_delivery_time',
                  'rating', 'total_reviews', 'platform_fee',
                  'is_open', 'status', 'products',
                  'distance', 'created_at']

    def get_distance(self, obj):
        request = self.context.get('request')
        if not request:
            return None
        try:
            buyer_lat = float(request.query_params.get('lat', 0))
            buyer_lng = float(request.query_params.get('lng', 0))
            if buyer_lat and buyer_lng and obj.latitude and obj.longitude:
                return calculate_distance(buyer_lat, buyer_lng, obj.latitude, obj.longitude)
        except (ValueError, TypeError):
            pass
        return None

class VendorRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Vendor
        fields = ['shop_name', 'category', 'description',
                  'phone_number', 'address', 'town',
                  'latitude', 'longitude',
                  'delivery_type', 'estimated_delivery_time']

    def create(self, validated_data):
        user     = self.context['request'].user
        fee_map  = {
            'vegetables':  5,
            'bakery':      7,
            'restaurant':  10,
            'supermarket': 7,
        }
        category     = validated_data.get('category', 'other')
        platform_fee = fee_map.get(category, 7)
        vendor = Vendor.objects.create(
            user=user,
            platform_fee=platform_fee,
            **validated_data
        )
        return vendor

class AddProductSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Product
        fields = ['name', 'description', 'price', 'category', 'is_available']
