#!/usr/bin/env python3
"""
Simple test to verify frontend-backend integration
"""

import requests
import json

BASE_URL = "http://localhost:5000"

print("🔧 Testing E-commerce Chatbot - Quick Integration Check")
print("=" * 55)

# Test 1: Get a fresh token
print("1. Getting authentication token...")
try:
    login_data = {"username": "demo_user", "password": "demo123"}
    response = requests.post(f"{BASE_URL}/api/auth/login", json=login_data)
    if response.status_code == 200:
        data = response.json()
        token = data['access_token']
        print(f"✅ Token received: {token[:50]}...")
    else:
        print(f"❌ Login failed: {response.status_code}")
        exit(1)
except Exception as e:
    print(f"❌ Login error: {e}")
    exit(1)

# Test 2: Test chatbot with proper token
print("\n2. Testing chatbot interaction...")
try:
    headers = {"Authorization": f"Bearer {token}"}
    message_data = {"message": "Hi! I'm looking for laptops under $800"}
    
    response = requests.post(f"{BASE_URL}/api/chatbot/message", json=message_data, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        print("✅ Chatbot response received!")
        print(f"   User: {message_data['message']}")
        print(f"   Bot: {data['response']}")
        
        if 'products' in data and data['products']:
            print(f"   📦 Found {len(data['products'])} products")
    else:
        print(f"❌ Chatbot request failed: {response.status_code}")
        print(f"   Response: {response.text}")
        
except Exception as e:
    print(f"❌ Chatbot error: {e}")

# Test 3: Test product search
print("\n3. Testing product search...")
try:
    response = requests.get(f"{BASE_URL}/api/products/?search=electronics&max_price=500")
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Found {data['pagination']['total']} electronics under $500")
    else:
        print(f"❌ Product search failed: {response.status_code}")
except Exception as e:
    print(f"❌ Product search error: {e}")

print("\n" + "=" * 55)
print("✅ Integration test complete!")
print("🌐 Frontend should be accessible at: file:///c:/Users/abhik/Downloads/Development%20of%20an%20E-commerce%20Sales/frontend/index.html")
print("🚀 Backend API running at: http://localhost:5000")
