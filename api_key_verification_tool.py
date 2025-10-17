#!/usr/bin/env python3
"""
Claude API Key Verification and Resolution Tool
This tool helps verify, test, and update Claude API keys for the application.
"""
import asyncio
import anthropic
import os
import sys
from datetime import datetime
from pathlib import Path

class APIKeyManager:
    def __init__(self):
        self.env_files = [
            ".env",
            "backend/.env",
            "config/.env"
        ]
        self.current_key = None
        self.load_current_key()
    
    def load_current_key(self):
        """Load the current API key from environment files."""
        # Check environment variable first
        self.current_key = os.getenv("AI_API_KEY")
        
        if not self.current_key:
            # Check .env files
            for env_file in self.env_files:
                if os.path.exists(env_file):
                    with open(env_file, 'r') as f:
                        for line in f:
                            if line.startswith('AI_API_KEY='):
                                self.current_key = line.split('=', 1)[1].strip()
                                break
                    if self.current_key:
                        break
    
    def validate_key_format(self, api_key):
        """Validate API key format."""
        if not api_key:
            return False, "API key is empty"
        
        if not api_key.startswith("sk-ant-api03-"):
            return False, "API key must start with 'sk-ant-api03-'"
        
        if len(api_key) < 100:
            return False, "API key is too short (should be ~106 characters)"
        
        if " " in api_key or "\n" in api_key or "\t" in api_key:
            return False, "API key contains whitespace"
        
        return True, "API key format is valid"
    
    async def test_api_key(self, api_key):
        """Test API key against Anthropic's API."""
        try:
            client = anthropic.Anthropic(api_key=api_key)
            
            # Make a minimal test call
            response = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: client.messages.create(
                    model="claude-3-sonnet-20240229",
                    max_tokens=10,
                    temperature=0,
                    messages=[{"role": "user", "content": "Test"}]
                )
            )
            
            return True, f"API key is valid. Response: {response.content[0].text}"
            
        except anthropic.AuthenticationError as e:
            return False, f"Authentication failed: {str(e)}"
        except anthropic.RateLimitError as e:
            return False, f"Rate limit exceeded: {str(e)}"
        except anthropic.APIError as e:
            return False, f"API error: {str(e)}"
        except Exception as e:
            return False, f"Unexpected error: {str(e)}"
    
    def update_env_files(self, new_api_key):
        """Update API key in all environment files."""
        updated_files = []
        
        for env_file in self.env_files:
            if os.path.exists(env_file):
                # Read current content
                with open(env_file, 'r') as f:
                    lines = f.readlines()
                
                # Update or add API key line
                updated = False
                for i, line in enumerate(lines):
                    if line.startswith('AI_API_KEY='):
                        lines[i] = f'AI_API_KEY={new_api_key}\n'
                        updated = True
                        break
                
                if not updated:
                    # Add the API key if not found
                    lines.append(f'AI_API_KEY={new_api_key}\n')
                
                # Write back to file
                with open(env_file, 'w') as f:
                    f.writelines(lines)
                
                updated_files.append(env_file)
        
        return updated_files
    
    def print_instructions(self):
        """Print step-by-step instructions for getting a new API key."""
        print("\n" + "="*80)
        print("🔧 HOW TO GET A NEW CLAUDE API KEY")
        print("="*80)
        print()
        print("1. 🌐 Go to the Anthropic Console:")
        print("   https://console.anthropic.com/")
        print()
        print("2. 🔐 Sign in to your account")
        print("   (If you don't have an account, create one)")
        print()
        print("3. 💳 Check your billing and credits:")
        print("   - Click on 'Billing' in the left sidebar")
        print("   - Ensure you have available credits")
        print("   - Add payment method if needed")
        print()
        print("4. 🔑 Generate a new API key:")
        print("   - Click on 'API Keys' in the left sidebar")
        print("   - Click 'Create Key' button")
        print("   - Give it a descriptive name (e.g., 'Career Platform')")
        print("   - Copy the generated key immediately (you won't see it again)")
        print()
        print("5. ✅ The key should look like:")
        print("   sk-ant-api03-[long string of characters]")
        print()
        print("6. 🔄 Use this tool to test and update your key:")
        print("   python api_key_verification_tool.py --update YOUR_NEW_KEY")
        print()
        print("="*80)

async def main():
    """Main function to run the API key verification tool."""
    manager = APIKeyManager()
    
    print("🔍 Claude API Key Verification Tool")
    print("="*60)
    print(f"Timestamp: {datetime.now().isoformat()}")
    
    # Check command line arguments
    if len(sys.argv) > 1:
        if sys.argv[1] == "--update" and len(sys.argv) > 2:
            new_key = sys.argv[2]
            print(f"\n🔄 Testing new API key...")
            
            # Validate format
            format_valid, format_msg = manager.validate_key_format(new_key)
            print(f"Format validation: {'✅' if format_valid else '❌'} {format_msg}")
            
            if format_valid:
                # Test the key
                key_valid, test_msg = await manager.test_api_key(new_key)
                print(f"API test: {'✅' if key_valid else '❌'} {test_msg}")
                
                if key_valid:
                    # Update environment files
                    updated_files = manager.update_env_files(new_key)
                    print(f"\n✅ API key updated in files: {', '.join(updated_files)}")
                    print("🎉 API key verification and update completed successfully!")
                    return True
                else:
                    print("\n❌ New API key is not valid. Please check the key and try again.")
                    return False
            else:
                print("\n❌ New API key format is invalid.")
                return False
        
        elif sys.argv[1] == "--help":
            manager.print_instructions()
            return True
    
    # Default behavior - test current key
    print(f"\n🔍 Current API key: {manager.current_key[:20] + '...' + manager.current_key[-10:] if manager.current_key and len(manager.current_key) > 30 else manager.current_key}")
    
    if not manager.current_key:
        print("❌ No API key found in environment files")
        manager.print_instructions()
        return False
    
    # Validate current key format
    format_valid, format_msg = manager.validate_key_format(manager.current_key)
    print(f"Format validation: {'✅' if format_valid else '❌'} {format_msg}")
    
    if format_valid:
        # Test current key
        key_valid, test_msg = await manager.test_api_key(manager.current_key)
        print(f"API test: {'✅' if key_valid else '❌'} {test_msg}")
        
        if key_valid:
            print("\n🎉 Current API key is working correctly!")
            return True
        else:
            print("\n❌ Current API key is invalid or expired.")
            manager.print_instructions()
            return False
    else:
        print("\n❌ Current API key format is invalid.")
        manager.print_instructions()
        return False

if __name__ == "__main__":
    print("Usage:")
    print("  python api_key_verification_tool.py                    # Test current key")
    print("  python api_key_verification_tool.py --update NEW_KEY   # Update with new key")
    print("  python api_key_verification_tool.py --help             # Show instructions")
    print()
    
    success = asyncio.run(main())
    sys.exit(0 if success else 1)