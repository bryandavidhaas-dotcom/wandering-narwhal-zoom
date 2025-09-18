#!/usr/bin/env python3
"""
Debug script to test Claude API authentication directly.
This will help identify the exact authentication issue.
"""
import asyncio
import anthropic
import os
from datetime import datetime

async def test_claude_api_authentication():
    """Test Claude API authentication with detailed error reporting."""
    
    # Get API key from environment
    api_key = os.getenv("AI_API_KEY", "your_anthropic_api_key_here")
    
    print("🔍 Claude API Authentication Debug Test")
    print("=" * 60)
    print(f"Timestamp: {datetime.now().isoformat()}")
    print(f"API Key: {api_key[:20]}...{api_key[-10:] if len(api_key) > 30 else api_key}")
    print(f"API Key Length: {len(api_key)}")
    print(f"API Key Format: {'✅ Valid sk-ant-api03- format' if api_key.startswith('sk-ant-api03-') else '❌ Invalid format'}")
    
    try:
        # Initialize Anthropic client
        print("\n🔧 Initializing Anthropic client...")
        client = anthropic.Anthropic(api_key=api_key)
        print("✅ Client initialized successfully")
        
        # Test API call
        print("\n📡 Testing API call...")
        response = await asyncio.get_event_loop().run_in_executor(
            None,
            lambda: client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=50,
                temperature=0.1,
                system="You are a helpful assistant.",
                messages=[
                    {"role": "user", "content": "Say 'Hello, API test successful!' and nothing else."}
                ]
            )
        )
        
        print("✅ API call successful!")
        print(f"Response: {response.content[0].text}")
        print(f"Model used: {response.model}")
        print(f"Usage: {response.usage}")
        
        return True, "API authentication successful"
        
    except anthropic.AuthenticationError as e:
        error_msg = f"Authentication failed: {str(e)}"
        print(f"❌ {error_msg}")
        
        # Check specific error details
        if hasattr(e, 'response'):
            print(f"HTTP Status: {e.response.status_code if hasattr(e.response, 'status_code') else 'Unknown'}")
            print(f"Error details: {e.response.text if hasattr(e.response, 'text') else 'No details'}")
        
        return False, error_msg
        
    except anthropic.RateLimitError as e:
        error_msg = f"Rate limit exceeded: {str(e)}"
        print(f"⚠️ {error_msg}")
        return False, error_msg
        
    except anthropic.APIError as e:
        error_msg = f"API error: {str(e)}"
        print(f"❌ {error_msg}")
        return False, error_msg
        
    except Exception as e:
        error_msg = f"Unexpected error: {str(e)}"
        print(f"❌ {error_msg}")
        print(f"Error type: {type(e).__name__}")
        return False, error_msg

async def test_api_key_validation():
    """Test API key validation patterns."""
    print("\n🔍 API Key Validation Tests")
    print("=" * 40)
    
    api_key = os.getenv("AI_API_KEY", "your_anthropic_api_key_here")
    
    # Check key format
    checks = [
        ("Starts with sk-ant-api03-", api_key.startswith("sk-ant-api03-")),
        ("Has correct length (>= 100 chars)", len(api_key) >= 100),
        ("Contains only valid characters", api_key.replace("-", "").replace("_", "").isalnum()),
        ("No whitespace", " " not in api_key and "\n" not in api_key and "\t" not in api_key),
    ]
    
    all_passed = True
    for check_name, passed in checks:
        status = "✅" if passed else "❌"
        print(f"{status} {check_name}")
        if not passed:
            all_passed = False
    
    return all_passed

async def main():
    """Run all debug tests."""
    print("🐛 Claude API Debug Analysis")
    print("=" * 60)
    
    # Test API key format
    key_valid = await test_api_key_validation()
    
    # Test authentication
    auth_success, auth_message = await test_claude_api_authentication()
    
    # Summary
    print("\n📋 Debug Summary")
    print("=" * 30)
    print(f"API Key Format: {'✅ Valid' if key_valid else '❌ Invalid'}")
    print(f"Authentication: {'✅ Success' if auth_success else '❌ Failed'}")
    
    if not auth_success:
        print(f"\n🔍 Root Cause Analysis:")
        print(f"Error: {auth_message}")
        
        if "authentication_error" in auth_message.lower():
            print("\n💡 Likely Issues:")
            print("1. API key is invalid or expired")
            print("2. API key doesn't have sufficient permissions")
            print("3. Account has insufficient credits")
            print("4. API key is for wrong service (OpenAI vs Anthropic)")
        
        print("\n🔧 Recommended Actions:")
        print("1. Verify API key in Anthropic Console")
        print("2. Check account billing and credits")
        print("3. Generate a new API key if needed")
        print("4. Ensure key has proper permissions")
    
    return auth_success

if __name__ == "__main__":
    success = asyncio.run(main())
    exit(0 if success else 1)