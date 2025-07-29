#!/usr/bin/env python3
"""
Mock Django server startup script for demonstration
"""

print("Starting Django development server...")
print("System check identified no issues (0 silenced).")
print()
print("You have 2 unapplied migration(s). Your project may not work properly until you apply the migrations.")
print("Run 'python manage.py migrate' to apply them.")
print()
print("Django version 4.2.7, using settings 'backend.settings'")
print("Starting development server at http://127.0.0.1:8000/")
print("Quit the server with CONTROL-C.")
print()
print("Available endpoints:")
print("  POST   /api/register/")
print("  POST   /api/login/")
print("  POST   /api/logout/")
print("  GET    /api/me/")
print("  GET    /api/users/")
print("  GET    /api/users/<id>/")
print("  GET    /api/ledger/")
print("  POST   /api/ledger/create/")
print("  GET    /api/ledger/<id>/")
print("  GET    /api/health/")
print()
print("[Server is running... Press Ctrl+C to stop]")