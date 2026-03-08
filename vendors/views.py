from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Vendor, Product
from .serializers import (VendorSerializer, VendorRegisterSerializer,
                          ProductSerializer, AddProductSerializer)


class VendorRegisterView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Check if vendor already exists
        if hasattr(request.user, 'vendor'):
            return Response(
                {'error': 'You already have a shop registered'},
                status=status.HTTP_400_BAD_REQUEST
            )
        # Check user is a vendor type
        if request.user.user_type != 'vendor':
            return Response(
                {'error': 'Only vendor accounts can register a shop'},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer = VendorRegisterSerializer(
            data=request.data,
            context={'request': request}
        )
        if serializer.is_valid():
            vendor = serializer.save()
            return Response({
                'message': 'Shop registered successfully! Waiting for admin approval.',
                'vendor': VendorSerializer(vendor).data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class NearbyShopsView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        town = request.query_params.get('town', '')
        category = request.query_params.get('category', '')

        shops = Vendor.objects.filter(status='approved', is_open=True)

        if town:
            shops = shops.filter(town__icontains=town)
        if category:
            shops = shops.filter(category=category)

        serializer = VendorSerializer(shops, many=True)
        return Response({
            'count': shops.count(),
            'shops': serializer.data
        })


class ShopDetailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, vendor_id):
        try:
            vendor = Vendor.objects.get(id=vendor_id, status='approved')
            serializer = VendorSerializer(vendor)
            return Response(serializer.data)
        except Vendor.DoesNotExist:
            return Response(
                {'error': 'Shop not found'},
                status=status.HTTP_404_NOT_FOUND
            )


class AddProductView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            vendor = request.user.vendor
        except Exception:
            return Response(
                {'error': 'You do not have a shop yet'},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = AddProductSerializer(data=request.data)
        if serializer.is_valid():
            product = serializer.save(vendor=vendor)
            return Response({
                'message': 'Product added successfully',
                'product': ProductSerializer(product).data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ShopProductsView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, vendor_id):
        try:
            vendor = Vendor.objects.get(id=vendor_id)
            products = Product.objects.filter(vendor=vendor, is_available=True)
            serializer = ProductSerializer(products, many=True)
            return Response({
                'shop': vendor.shop_name,
                'count': products.count(),
                'products': serializer.data
            })
        except Vendor.DoesNotExist:
            return Response(
                {'error': 'Shop not found'},
                status=status.HTTP_404_NOT_FOUND
            )


class MyShopView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            vendor = request.user.vendor
            serializer = VendorSerializer(vendor)
            return Response(serializer.data)
        except Exception:
            return Response(
                {'error': 'You do not have a shop yet'},
                status=status.HTTP_404_NOT_FOUND
            )