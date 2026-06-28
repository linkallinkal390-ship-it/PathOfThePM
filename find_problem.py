import sys
import os

def test_import(module_name):
    try:
        __import__(module_name)
        print(f"✅ {module_name} - OK")
        return True
    except UnicodeDecodeError as e:
        print(f"❌ {module_name} - ERROR: {e}")
        return False
    except Exception as e:
        print(f"⚠️ {module_name} - Other error: {e}")
        return False

# Test imports
test_import('api')
test_import('api.models')
test_import('api.views')
test_import('api.serializers')
test_import('api.urls')
test_import('api.exceptions')
test_import('api.responses')
test_import('api.pagination')
test_import('api.admin')
test_import('api.apps')
test_import('backend.settings')