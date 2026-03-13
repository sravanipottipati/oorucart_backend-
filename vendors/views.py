from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Vendor, Product, Wishlist
from .serializers import (VendorSerializer, VendorRegisterSerializer,
                          ProductSerializer, AddProductSerializer)


class VendorRegisterView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if hasattr(request.user, 'vendor'):
            return Response(
                {'error': 'You already have a shop registered'},
                status=status.HTTP_400_BAD_REQUEST
            )
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
                'vendor':  VendorSerializer(vendor).data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class NearbyShopsView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        town     = request.query_params.get('town', '')
        category = request.query_params.get('category', '')
        shops    = Vendor.objects.filter(status='approved', is_open=True)
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
            vendor     = Vendor.objects.get(id=vendor_id, status='approved')
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
            vendor   = Vendor.objects.get(id=vendor_id)
            products = Product.objects.filter(vendor=vendor, is_available=True)
            serializer = ProductSerializer(products, many=True)
            return Response({
                'shop':     vendor.shop_name,
                'count':    products.count(),
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
            vendor     = request.user.vendor
            serializer = VendorSerializer(vendor)
            return Response(serializer.data)
        except Exception:
            return Response(
                {'error': 'You do not have a shop yet'},
                status=status.HTTP_404_NOT_FOUND
            )


class ToggleShopView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            vendor         = Vendor.objects.get(user=request.user)
            vendor.is_open = not vendor.is_open
            vendor.save()
            return Response({
                'is_open': vendor.is_open,
                'message': 'Shop is now Open!' if vendor.is_open else 'Shop is now Closed!'
            })
        except Vendor.DoesNotExist:
            return Response({'error': 'Vendor not found'}, status=404)


class EditProductView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, product_id):
        try:
            product = Product.objects.get(id=product_id, vendor=request.user.vendor)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=404)
        serializer = AddProductSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'Product updated',
                'product': ProductSerializer(product).data
            })
        return Response(serializer.errors, status=400)

    def delete(self, request, product_id):
        try:
            product = Product.objects.get(id=product_id, vendor=request.user.vendor)
            product.delete()
            return Response({'message': 'Product deleted'})
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=404)


class SearchView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        q    = request.query_params.get('q', '').strip()
        town = request.query_params.get('town', '').strip()

        if not q:
            return Response({'shops': [], 'products': []})

        shops = Vendor.objects.filter(status='approved', is_open=True)
        if town:
            shops = shops.filter(town__icontains=town)
        shops     = shops.filter(shop_name__icontains=q)
        shop_data = VendorSerializer(shops, many=True).data

        products = Product.objects.filter(is_available=True)
        if town:
            products = products.filter(vendor__town__icontains=town)
        products = products.filter(name__icontains=q)

        product_data = []
        for p in products:
            product_data.append({
                'id':          str(p.id),
                'name':        p.name,
                'price':       str(p.price),
                'shop_name':   p.vendor.shop_name,
                'shop_id':     str(p.vendor.id),
                'town':        p.vendor.town,
            })

        return Response({'shops': shop_data, 'products': product_data})


class WishlistView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        items = Wishlist.objects.filter(
            user=request.user
        ).select_related('product__vendor')
        data = [{
            'id':           str(w.id),
            'product_id':   str(w.product.id),
            'name':         w.product.name,
            'price':        str(w.product.price),
            'shop_name':    w.product.vendor.shop_name,
            'shop_id':      str(w.product.vendor.id),
            'town':         w.product.vendor.town,
            'is_available': w.product.is_available,
            'added_at':     w.created_at.isoformat(),
        } for w in items]
        return Response({'count': len(data), 'wishlist': data})

    def post(self, request):
        product_id = request.data.get('product_id')
        if not product_id:
            return Response({'error': 'product_id required'}, status=400)
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=404)

        wishlist, created = Wishlist.objects.get_or_create(
            user=request.user, product=product
        )
        if created:
            return Response({'message': 'Added to wishlist', 'wishlisted': True}, status=201)
        else:
            wishlist.delete()
            return Response({'message': 'Removed from wishlist', 'wishlisted': False})
