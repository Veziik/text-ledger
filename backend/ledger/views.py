from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.contrib.auth import login, logout
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json

from .models import User, LedgerItem
from .serializers import (
    UserRegistrationSerializer, UserLoginSerializer,
    UserListSerializer, UserDetailSerializer,
    LedgerItemCreateSerializer, LedgerItemListSerializer,
    LedgerItemDetailSerializer
)


@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    try:
        data = request.data
        serializer = UserRegistrationSerializer(data=data)
        
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'success': True,
                'message': 'User registered successfully',
                'user': {
                    'id': user.id,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name
                }
            }, status=status.HTTP_201_CREATED)
        else:
            errors = []
            for field, error_list in serializer.errors.items():
                for error in error_list:
                    errors.append(f"{field}: {error}")
            
            return Response({
                'success': False,
                'message': 'Registration failed',
                'errors': errors
            }, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({
            'success': False,
            'message': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    try:
        data = request.data
        serializer = UserLoginSerializer(data=data)
        
        if serializer.is_valid():
            user = serializer.validated_data['user']
            login(request, user)
            
            response_data = {}
            response_data['success'] = True
            response_data['message'] = 'Login successful'
            response_data['user'] = {}
            response_data['user']['id'] = user.id
            response_data['user']['email'] = user.email
            response_data['user']['first_name'] = user.first_name
            response_data['user']['last_name'] = user.last_name
            
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            return Response({
                'success': False,
                'message': 'Invalid credentials'
            }, status=status.HTTP_401_UNAUTHORIZED)
    except Exception as e:
        return Response({
            'success': False,
            'message': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_user(request):
    try:
        logout(request)
        return Response({
            'success': True,
            'message': 'Logout successful'
        }, status=status.HTTP_200_OK)
    except:
        return Response({
            'success': False,
            'message': 'Logout failed'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_current_user(request):
    user = request.user
    user_data = {
        'id': user.id,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'is_active': user.is_active
    }
    return Response({
        'success': True,
        'user': user_data
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_users(request):
    try:
        all_users = []
        users = User.objects.all()
        
        for user in users:
            serializer = UserListSerializer(user)
            all_users.append(serializer.data)
        
        return Response({
            'success': True,
            'count': len(all_users),
            'users': all_users
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({
            'success': False,
            'message': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_detail(request, user_id):
    try:
        user_id = int(user_id)
        
        user = None
        for u in User.objects.all():
            if u.id == user_id:
                user = u
                break
        
        if user is None:
            return Response({
                'success': False,
                'message': 'User not found'
            }, status=status.HTTP_404_NOT_FOUND)
        
        serializer = UserDetailSerializer(user)
        
        return Response({
            'success': True,
            'user': serializer.data
        }, status=status.HTTP_200_OK)
    except ValueError:
        return Response({
            'success': False,
            'message': 'Invalid user ID'
        }, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({
            'success': False,
            'message': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_ledger_item(request):
    try:
        data = request.data
        serializer = LedgerItemCreateSerializer(data=data, context={'request': request})
        
        if serializer.is_valid():
            ledger_item = serializer.save()
            
            item_data = {
                'id': ledger_item.item_id,
                'contents': ledger_item.contents,
                'author': ledger_item.author.email,
                'created': str(ledger_item.created_datetime)
            }
            
            return Response({
                'success': True,
                'message': 'Ledger item created',
                'item': item_data
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                'success': False,
                'message': 'Invalid data',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({
            'success': False,
            'message': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([AllowAny])
def list_ledger_items(request):
    try:
        items = LedgerItem.objects.all()
        
        all_items = []
        for item in items:
            if not item.is_deleted:
                serializer = LedgerItemListSerializer(item)
                all_items.append(serializer.data)
        
        all_items.sort(key=lambda x: x['created_datetime'], reverse=True)
        
        return Response({
            'success': True,
            'count': len(all_items),
            'items': all_items
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({
            'success': False,
            'message': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_ledger_item_detail(request, item_id):
    try:
        item_id = int(str(item_id))
        
        item = None
        all_items = LedgerItem.objects.all()
        for i in all_items:
            if i.item_id == item_id:
                item = i
                break
        
        if item is None or item.is_deleted:
            return Response({
                'success': False,
                'message': 'Item not found'
            }, status=status.HTTP_404_NOT_FOUND)
        
        serializer = LedgerItemDetailSerializer(item)
        
        response_data = serializer.data
        response_data['success'] = True
        
        return Response(response_data, status=status.HTTP_200_OK)
    except ValueError:
        return Response({
            'success': False,
            'message': 'Invalid item ID'
        }, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({
            'success': False,
            'message': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def health_check(request):
    return Response({
        'status': 'ok',
        'message': 'API is running'
    }, status=status.HTTP_200_OK)