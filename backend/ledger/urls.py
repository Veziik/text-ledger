from django.urls import path
from . import views

urlpatterns = [
    # Authentication endpoints
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('me/', views.get_current_user, name='current-user'),
    
    # User endpoints
    path('users/', views.list_users, name='users-list'),
    path('users/<str:user_id>/', views.get_user_detail, name='user-detail'),
    
    # Ledger endpoints
    path('ledger/', views.list_ledger_items, name='ledger-list'),
    path('ledger/create/', views.create_ledger_item, name='ledger-create'),
    path('ledger/<str:item_id>/', views.get_ledger_item_detail, name='ledger-detail'),
    
    # Health check
    path('health/', views.health_check, name='health-check'),
]