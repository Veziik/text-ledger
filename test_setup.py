#!/usr/bin/env python3
import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Try to import Django
try:
    import django
    print(f"Django {django.__version__} is installed")
except ImportError:
    print("Django is not installed")
    
# Try to import other dependencies
try:
    import rest_framework
    print("Django REST Framework is installed")
except ImportError:
    print("Django REST Framework is not installed")
    
try:
    import corsheaders
    print("Django CORS Headers is installed")
except ImportError:
    print("Django CORS Headers is not installed")