#!/usr/bin/env python
"""
Initialize test data for the application
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from ledger.models import User, LedgerItem

def create_test_data():
    print("Creating test data...")
    
    # Create test users
    if not User.objects.filter(email='test@example.com').exists():
        user1 = User.objects.create_user(
            email='test@example.com',
            password='password123',
            first_name='Test',
            last_name='User'
        )
        print(f"Created user: {user1.email}")
    
    if not User.objects.filter(email='demo@example.com').exists():
        user2 = User.objects.create_user(
            email='demo@example.com',
            password='demo123',
            first_name='Demo',
            last_name='Account'
        )
        print(f"Created user: {user2.email}")
    
    # Create some ledger entries
    user1 = User.objects.get(email='test@example.com')
    if not LedgerItem.objects.filter(author=user1).exists():
        LedgerItem.objects.create(
            author=user1,
            contents="This is my first ledger entry!"
        )
        LedgerItem.objects.create(
            author=user1,
            contents="Another important note to remember."
        )
        print("Created sample ledger entries")
    
    print("Test data initialization complete!")
    print("\nYou can login with:")
    print("  Email: test@example.com")
    print("  Password: password123")
    print("\nOr:")
    print("  Email: demo@example.com")
    print("  Password: demo123")

if __name__ == '__main__':
    create_test_data()