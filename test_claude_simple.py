#!/usr/bin/env python3
"""
Simple test script to verify Claude API is working with the new key.
"""
import asyncio
import anthropic

async def test_claude_direct():
    """Test Claude API directly with the new key."""
    
    # Use the Claude API key directly
    claude_key = "your_anthropic_api_key_here"
    
    print(f"Testing Claude API with key: {claude_key[:20]}...")
    
    try:
        # Initialize the Anthropic client
        client = anthropic.Anthropic(api_key=claude_key)
        
        print("\n=== Testing Claude API directly ===")
        
        # Run the synchronous call in a thread pool
        response = await asyncio.get_event_loop().run_in_executor(
            None,
            lambda: client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=100,
                temperature=0.7,
                system="You are a helpful assistant.",
                messages=[
                    {"role": "user", "content": "Say hello and confirm you are Claude."}
                ]
            )
        )
        
        print(f"✅ Claude API test successful!")
        print(f"Response: {response.content[0].text}")
        return True
        
    except Exception as e:
        print(f"❌ Claude API test failed: {e}")
        return False

if __name__ == "__main__":
    print("🔧 Testing Claude API Direct Connection")
    print("=" * 50)
    
    # Run the async test
    success = asyncio.run(test_claude_direct())
    
    if success:
        print("\n✅ Claude API is working correctly!")
    else:
        print("\n❌ Claude API test failed!")