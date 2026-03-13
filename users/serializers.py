from rest_framework import serializers
from .models import User, Address

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)
    class Meta:
        model  = User
        fields = ['full_name', 'phone_number', 'email', 'password', 'user_type', 'town']
    def create(self, validated_data):
        password = validated_data.pop('password')
        user     = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model  = User
        fields = ['id', 'full_name', 'phone_number', 'email', 'user_type', 'town', 'created_at']

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Address
        fields = ['id', 'label', 'full_address', 'town', 'pincode', 'is_default', 'created_at']
