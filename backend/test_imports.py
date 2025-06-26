#!/usr/bin/env python3
"""
Test script to diagnose import issues
"""

print("Testing imports step by step...")

try:
    print("1. Testing Flask import...")
    from flask import Flask
    print("✅ Flask imported successfully")
except Exception as e:
    print(f"❌ Flask import failed: {e}")
    exit(1)

try:
    print("2. Testing Flask extensions...")
    from flask_sqlalchemy import SQLAlchemy
    from flask_login import LoginManager
    from flask_cors import CORS
    from flask_jwt_extended import JWTManager
    print("✅ Flask extensions imported successfully")
except Exception as e:
    print(f"❌ Flask extensions import failed: {e}")
    exit(1)

try:
    print("3. Testing models import...")
    import models
    print("✅ Models imported successfully")
except Exception as e:
    print(f"❌ Models import failed: {e}")
    exit(1)

try:
    print("4. Testing routes import...")
    from routes import auth, products, chatbot
    print("✅ Routes imported successfully")
except Exception as e:
    print(f"❌ Routes import failed: {e}")
    exit(1)

try:
    print("5. Testing utils import...")
    from utils import database, chatbot_logic
    print("✅ Utils imported successfully")
except Exception as e:
    print(f"❌ Utils import failed: {e}")
    exit(1)

try:
    print("6. Testing app creation...")
    from app import create_app
    print("✅ create_app imported successfully")
    
    app = create_app()
    print("✅ App created successfully")
    
    with app.app_context():
        print("✅ App context works")
        
except Exception as e:
    print(f"❌ App creation failed: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

print("🎉 All tests passed!")
