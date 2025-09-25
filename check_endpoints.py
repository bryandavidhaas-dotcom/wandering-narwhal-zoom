#!/usr/bin/env python3

import requests
import json

def check_server_endpoints():
    """Check what endpoints are available on the server"""
    
    try:
        # Get the OpenAPI spec
        response = requests.get("http://localhost:8001/openapi.json", timeout=5)
        if response.status_code == 200:
            spec = response.json()
            paths = spec.get("paths", {})
            
            print("Available endpoints on port 8001:")
            for path, methods in paths.items():
                for method, details in methods.items():
                    summary = details.get("summary", "No summary")
                    print(f"  {method.upper()} {path} - {summary}")
            
            # Check if /api/recommendations exists
            if "/api/recommendations" in paths:
                print("\n✅ /api/recommendations endpoint EXISTS")
                api_details = paths["/api/recommendations"]
                if "post" in api_details:
                    print("✅ POST method available")
                    request_body = api_details["post"].get("requestBody", {})
                    print(f"Request body schema: {json.dumps(request_body, indent=2)}")
                else:
                    print("❌ POST method not available")
            else:
                print("\n❌ /api/recommendations endpoint MISSING")
                
            # Check if /recommendations exists
            if "/recommendations" in paths:
                print("\n✅ /recommendations endpoint EXISTS")
            else:
                print("\n❌ /recommendations endpoint MISSING")
                
        else:
            print(f"Failed to get OpenAPI spec: {response.status_code}")
            
    except Exception as e:
        print(f"Error checking endpoints: {e}")

if __name__ == "__main__":
    check_server_endpoints()