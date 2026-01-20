#!/usr/bin/env python3
"""
Simple test script to verify the API is working
Run this after starting the backend server
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_health():
    """Test health endpoint"""
    print("Testing health endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            data = response.json()
            print("✅ Health check passed!")
            print(f"   Services: {json.dumps(data, indent=2)}")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        print("   Make sure the backend server is running!")
        return False

def test_text_processing():
    """Test text processing endpoint"""
    print("\nTesting text processing...")
    try:
        data = {"text": "Hello, how are you?"}
        response = requests.post(
            f"{BASE_URL}/api/text/process",
            json=data,
            headers={"Content-Type": "application/json"}
        )
        if response.status_code == 200:
            result = response.json()
            print("✅ Text processing successful!")
            print(f"   Input: {result.get('text')}")
            print(f"   Intent: {result.get('intent')}")
            print(f"   Response: {result.get('response')}")
            return True
        else:
            print(f"❌ Text processing failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    print("🧪 Voice Assistant API Test")
    print("=" * 40)
    
    # Test health
    if not test_health():
        print("\n⚠️  Backend may not be ready yet. Wait a few minutes for models to load.")
        return
    
    # Test text processing
    test_text_processing()
    
    print("\n" + "=" * 40)
    print("✅ Basic tests completed!")
    print("\nNote: Voice processing requires an audio file upload.")
    print("Use the Flutter app or Postman to test voice input.")

if __name__ == "__main__":
    main()


