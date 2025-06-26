#!/usr/bin/env python3
"""
Debug script for chatbot API
"""

import requests
import json

BASE_URL = "http://localhost:5000"

# First, login to get a token
print("🔐 Getting authentication token...")
login_data = {"username": "demo_user", "password": "demo123"}
response = requests.post(f"{BASE_URL}/api/auth/login", json=login_data)

if response.status_code != 200:
    print(f"❌ Login failed: {response.status_code}")
    print(f"Response: {response.text}")
    exit(1)

data = response.json()
token = data['access_token']
print(f"✅ Got token: {token[:50]}...")

# Now test the chatbot endpoint
print("\n🤖 Testing chatbot endpoint...")
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {token}"
}

message_data = {"message": "Hello, show me laptops"}

try:
    response = requests.post(f"{BASE_URL}/api/chatbot/message", json=message_data, headers=headers)
    print(f"Response status: {response.status_code}")
    print(f"Response headers: {dict(response.headers)}")
    
    if response.status_code == 200:
        data = response.json()
        print("✅ Chatbot response received!")
        print(f"Bot response: {data.get('bot_response', 'No response')}")
    else:
        print(f"❌ Error: {response.status_code}")
        print(f"Response: {response.text}")
        
except Exception as e:
    print(f"❌ Exception: {e}")
