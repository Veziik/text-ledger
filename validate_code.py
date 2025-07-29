#!/usr/bin/env python3
"""
Code validation script to check for syntax errors and basic issues
"""

import os
import ast
import json
import re

def check_python_syntax(filepath):
    """Check if Python file has valid syntax"""
    try:
        with open(filepath, 'r') as f:
            content = f.read()
        ast.parse(content)
        return True, "OK"
    except SyntaxError as e:
        return False, f"Syntax error at line {e.lineno}: {e.msg}"
    except Exception as e:
        return False, str(e)

def check_json_syntax(filepath):
    """Check if JSON file has valid syntax"""
    try:
        with open(filepath, 'r') as f:
            json.load(f)
        return True, "OK"
    except json.JSONDecodeError as e:
        return False, f"JSON error at line {e.lineno}: {e.msg}"
    except Exception as e:
        return False, str(e)

def check_vue_syntax(filepath):
    """Basic check for Vue file structure"""
    try:
        with open(filepath, 'r') as f:
            content = f.read()
        
        # Check for basic Vue structure
        has_template = '<template>' in content and '</template>' in content
        has_script = '<script>' in content and '</script>' in content
        
        if not has_template:
            return False, "Missing <template> section"
        if not has_script:
            return False, "Missing <script> section"
            
        # Extract and check JavaScript syntax
        script_match = re.search(r'<script>(.*?)</script>', content, re.DOTALL)
        if script_match:
            js_content = script_match.group(1)
            # Basic JS syntax check (not comprehensive)
            if js_content.count('{') != js_content.count('}'):
                return False, "Mismatched braces in script section"
            if js_content.count('(') != js_content.count(')'):
                return False, "Mismatched parentheses in script section"
                
        return True, "OK"
    except Exception as e:
        return False, str(e)

def validate_project():
    """Validate all project files"""
    print("Validating Text Ledger Application Code...")
    print("=" * 50)
    
    # Python files to check
    python_files = [
        'backend/manage.py',
        'backend/backend/__init__.py',
        'backend/backend/settings.py',
        'backend/backend/urls.py',
        'backend/backend/wsgi.py',
        'backend/backend/asgi.py',
        'backend/ledger/__init__.py',
        'backend/ledger/models.py',
        'backend/ledger/serializers.py',
        'backend/ledger/views.py',
        'backend/ledger/urls.py',
        'backend/ledger/admin.py',
    ]
    
    print("\nChecking Python files:")
    errors = []
    for filepath in python_files:
        full_path = os.path.join('/workspace/text-ledger-app', filepath)
        if os.path.exists(full_path):
            valid, message = check_python_syntax(full_path)
            status = "✓" if valid else "✗"
            print(f"  {status} {filepath}: {message}")
            if not valid:
                errors.append(f"{filepath}: {message}")
        else:
            print(f"  ✗ {filepath}: File not found")
            errors.append(f"{filepath}: File not found")
    
    # JSON files to check
    json_files = [
        'frontend/package.json',
        'frontend/babel.config.js',  # Actually JS but can be validated
    ]
    
    print("\nChecking JSON/Config files:")
    for filepath in json_files:
        full_path = os.path.join('/workspace/text-ledger-app', filepath)
        if os.path.exists(full_path):
            if filepath.endswith('.json'):
                valid, message = check_json_syntax(full_path)
            else:
                valid, message = True, "OK"  # Skip JS config files
            status = "✓" if valid else "✗"
            print(f"  {status} {filepath}: {message}")
            if not valid:
                errors.append(f"{filepath}: {message}")
        else:
            print(f"  ✗ {filepath}: File not found")
            errors.append(f"{filepath}: File not found")
    
    # Vue files to check
    vue_files = [
        'frontend/src/App.vue',
        'frontend/src/views/Login.vue',
        'frontend/src/views/Register.vue',
        'frontend/src/views/LedgerList.vue',
        'frontend/src/views/LedgerDetail.vue',
        'frontend/src/views/UserList.vue',
        'frontend/src/views/UserDetail.vue',
    ]
    
    print("\nChecking Vue files:")
    for filepath in vue_files:
        full_path = os.path.join('/workspace/text-ledger-app', filepath)
        if os.path.exists(full_path):
            valid, message = check_vue_syntax(full_path)
            status = "✓" if valid else "✗"
            print(f"  {status} {filepath}: {message}")
            if not valid:
                errors.append(f"{filepath}: {message}")
        else:
            print(f"  ✗ {filepath}: File not found")
            errors.append(f"{filepath}: File not found")
    
    # JavaScript files to check
    js_files = [
        'frontend/src/main.js',
        'frontend/src/router/index.js',
    ]
    
    print("\nChecking JavaScript files:")
    for filepath in js_files:
        full_path = os.path.join('/workspace/text-ledger-app', filepath)
        if os.path.exists(full_path):
            # Basic syntax check
            try:
                with open(full_path, 'r') as f:
                    content = f.read()
                # Very basic checks
                if content.count('{') != content.count('}'):
                    valid, message = False, "Mismatched braces"
                elif content.count('(') != content.count(')'):
                    valid, message = False, "Mismatched parentheses"
                else:
                    valid, message = True, "OK"
            except Exception as e:
                valid, message = False, str(e)
                
            status = "✓" if valid else "✗"
            print(f"  {status} {filepath}: {message}")
            if not valid:
                errors.append(f"{filepath}: {message}")
        else:
            print(f"  ✗ {filepath}: File not found")
            errors.append(f"{filepath}: File not found")
    
    print("\n" + "=" * 50)
    if errors:
        print(f"\n❌ Found {len(errors)} error(s):")
        for error in errors:
            print(f"   - {error}")
    else:
        print("\n✅ All files validated successfully!")
        print("\nTo run the application:")
        print("1. Backend: cd backend && python manage.py migrate && python manage.py runserver")
        print("2. Frontend: cd frontend && npm install && npm run serve")
    
if __name__ == "__main__":
    validate_project()