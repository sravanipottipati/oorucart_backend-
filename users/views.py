from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .serializers import RegisterSerializer, UserSerializer
from .models import User, Address


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access':  str(refresh.access_token),
    }


class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user   = serializer.save()
            tokens = get_tokens_for_user(user)
            return Response({
                'message': 'Registration successful',
                'user':    UserSerializer(user).data,
                'tokens':  tokens
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        phone_number = request.data.get('phone_number')
        password     = request.data.get('password')
        user         = authenticate(request, phone_number=phone_number, password=password)
        if user:
            tokens = get_tokens_for_user(user)
            return Response({
                'message': 'Login successful',
                'user':    UserSerializer(user).data,
                'tokens':  tokens
            }, status=status.HTTP_200_OK)
        return Response(
            {'error': 'Invalid phone number or password'},
            status=status.HTTP_401_UNAUTHORIZED
        )


class ProfileView(APIView):
    def get(self, request):
        if not request.user.is_authenticated:
            return Response({'error': 'Not authenticated'}, status=401)
        return Response(UserSerializer(request.user).data)

    def patch(self, request):
        if not request.user.is_authenticated:
            return Response({'error': 'Not authenticated'}, status=401)
        user = request.user
        user.full_name = request.data.get('full_name', user.full_name)
        user.email     = request.data.get('email', user.email)
        user.town      = request.data.get('town', user.town)
        user.save()
        return Response({
            'message': 'Profile updated successfully',
            'user':    UserSerializer(user).data,
        })


# ─── ADDRESS VIEWS ────────────────────────────────────────────────────────────

class AddressListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        addresses = Address.objects.filter(user=request.user).order_by('-is_default', '-created_at')
        data = [{
            'id':           str(a.id),
            'label':        a.label,
            'full_address': a.full_address,
            'town':         a.town,
            'pincode':      a.pincode or '',
            'is_default':   a.is_default,
        } for a in addresses]
        return Response(data)

    def post(self, request):
        label        = request.data.get('label', 'Home')
        full_address = request.data.get('full_address', '').strip()
        town         = request.data.get('town', '').strip()
        pincode      = request.data.get('pincode', '')
        is_default   = request.data.get('is_default', False)

        if not full_address:
            return Response({'error': 'Address is required'}, status=400)
        if not town:
            return Response({'error': 'Town is required'}, status=400)

        if not Address.objects.filter(user=request.user).exists():
            is_default = True

        address = Address.objects.create(
            user=request.user,
            label=label,
            full_address=full_address,
            town=town,
            pincode=pincode,
            is_default=is_default,
        )
        return Response({
            'message': 'Address added successfully',
            'address': {
                'id':           str(address.id),
                'label':        address.label,
                'full_address': address.full_address,
                'town':         address.town,
                'pincode':      address.pincode or '',
                'is_default':   address.is_default,
            }
        }, status=201)


class AddressDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, address_id):
        try:
            address = Address.objects.get(id=address_id, user=request.user)
        except Address.DoesNotExist:
            return Response({'error': 'Address not found'}, status=404)

        address.label        = request.data.get('label', address.label)
        address.full_address = request.data.get('full_address', address.full_address)
        address.town         = request.data.get('town', address.town)
        address.pincode      = request.data.get('pincode', address.pincode)
        address.is_default   = request.data.get('is_default', address.is_default)
        address.save()
        return Response({'message': 'Address updated successfully'})

    def delete(self, request, address_id):
        try:
            address = Address.objects.get(id=address_id, user=request.user)
            address.delete()
            remaining = Address.objects.filter(user=request.user).first()
            if remaining:
                remaining.is_default = True
                remaining.save()
            return Response({'message': 'Address deleted'})
        except Address.DoesNotExist:
            return Response({'error': 'Address not found'}, status=404)


class SetDefaultAddressView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, address_id):
        try:
            address            = Address.objects.get(id=address_id, user=request.user)
            address.is_default = True
            address.save()
            return Response({'message': 'Default address updated'})
        except Address.DoesNotExist:
            return Response({'error': 'Address not found'}, status=404)
