#!/usr/bin/env python3
"""
Integration test script for E-commerce Sales Chatbot
Tests key API endpoints and functionality
"""

import requests
import json
import time

BASE_URL = "http://localhost:5000"

def test_api():
    print("🧪 Starting E-commerce Chatbot Integration Tests")
    print("=" * 50)
    
    # Test 1: Check server health
    print("1. Testing server health...")
    try:
        response = requests.get(f"{BASE_URL}/api/products/")
        assert response.status_code == 200
        print("✅ Server is running and responding")
    except Exception as e:
        print(f"❌ Server health check failed: {e}")
        return False
    
    # Test 2: User Registration
    print("\n2. Testing user registration...")
    try:
        user_data = {
            "username": f"testuser_{int(time.time())}",
            "email": f"test_{int(time.time())}@example.com",
            "password": "testpass123"
        }
        response = requests.post(f"{BASE_URL}/api/auth/register", json=user_data)
        assert response.status_code == 201
        data = response.json()
        auth_token = data['access_token']
        print("✅ User registration successful")
    except Exception as e:
        print(f"❌ User registration failed: {e}")
        return False
    
    # Test 3: User Login
    print("\n3. Testing user login...")
    try:
        login_data = {"username": "demo_user", "password": "demo123"}
        response = requests.post(f"{BASE_URL}/api/auth/login", json=login_data)
        assert response.status_code == 200
        data = response.json()
        demo_token = data['access_token']
        print("✅ User login successful")
    except Exception as e:
        print(f"❌ User login failed: {e}")
        return False
    
    # Test 4: Products API
    print("\n4. Testing products API...")
    try:
        response = requests.get(f"{BASE_URL}/api/products/")
        assert response.status_code == 200
        data = response.json()
        assert 'products' in data
        assert len(data['products']) > 0
        print(f"✅ Products API working - {data['pagination']['total']} products found")
    except Exception as e:
        print(f"❌ Products API test failed: {e}")
        return False
    
    # Test 5: Product Search
    print("\n5. Testing product search...")
    try:
        response = requests.get(f"{BASE_URL}/api/products/?search=laptop")
        assert response.status_code == 200
        data = response.json()
        assert 'products' in data
        print(f"✅ Product search working - found {len(data['products'])} laptop results")
    except Exception as e:
        print(f"❌ Product search test failed: {e}")
        return False
    
    # Test 6: Categories API
    print("\n6. Testing categories API...")
    try:
        response = requests.get(f"{BASE_URL}/api/products/categories")
        assert response.status_code == 200
        data = response.json()
        assert 'categories' in data
        assert len(data['categories']) > 0
        print(f"✅ Categories API working - {len(data['categories'])} categories found")
    except Exception as e:
        print(f"❌ Categories API test failed: {e}")
        return False
    
    # Test 7: Chatbot API (authenticated)
    print("\n7. Testing chatbot API...")
    try:
        headers = {"Authorization": f"Bearer {demo_token}"}
        message_data = {"message": "Hi, I'm looking for electronics"}
        response = requests.post(f"{BASE_URL}/api/chatbot/message", json=message_data, headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert 'response' in data
        print("✅ Chatbot API working")
        print(f"   Bot response: {data['response'][:100]}...")
    except Exception as e:
        print(f"❌ Chatbot API test failed: {e}")
        return False
    
    # Test 8: Chat History
    print("\n8. Testing chat history...")
    try:
        headers = {"Authorization": f"Bearer {demo_token}"}
        response = requests.get(f"{BASE_URL}/api/chatbot/history", headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert 'messages' in data
        print(f"✅ Chat history working - {len(data['messages'])} messages found")
    except Exception as e:
        print(f"❌ Chat history test failed: {e}")
        return False
    
    print("\n" + "=" * 50)
    print("🎉 All integration tests passed successfully!")
    print("🚀 The E-commerce Sales Chatbot is fully functional!")
    return True

if __name__ == "__main__":
    test_api()
