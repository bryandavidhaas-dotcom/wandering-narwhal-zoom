#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

def check_server_routes():
    try:
        import simple_server
        print(f"✅ Successfully imported simple_server from: {simple_server.__file__}")
        
        app = simple_server.app
        print(f"\nApp routes in simple_server.py:")
        
        for route in app.routes:
            if hasattr(route, 'methods') and hasattr(route, 'path'):
                methods = list(route.methods)
                path = route.path
                summary = getattr(route, 'summary', 'No summary')
                print(f"  {methods} {path} - {summary}")
        
        # Check if DirectRecommendationRequest exists
        if hasattr(simple_server, 'DirectRecommendationRequest'):
            print(f"\n✅ DirectRecommendationRequest model exists")
        else:
            print(f"\n❌ DirectRecommendationRequest model MISSING")
            
        # Check if the enhanced endpoint exists
        api_recommendations_found = False
        for route in app.routes:
            if hasattr(route, 'path') and route.path == '/api/recommendations':
                api_recommendations_found = True
                print(f"✅ /api/recommendations endpoint found")
                break
        
        if not api_recommendations_found:
            print(f"❌ /api/recommendations endpoint MISSING")
            
    except Exception as e:
        print(f"❌ Error importing simple_server: {e}")

if __name__ == "__main__":
    check_server_routes()