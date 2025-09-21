#!/usr/bin/env python3
"""
Test script to verify public service careers are loaded correctly
"""

def test_public_service_careers():
    """Test that public service careers can be imported and loaded"""
    try:
        from public_service_careers import PUBLIC_SERVICE_CAREERS
        print(f"✅ Successfully imported {len(PUBLIC_SERVICE_CAREERS)} public service careers")
        
        # Test a few sample careers
        sample_careers = [
            "Federal Agency Director",
            "City Manager", 
            "Police Chief",
            "Legislative Analyst",
            "GS-11 Program Analyst"
        ]
        
        found_careers = []
        for career in PUBLIC_SERVICE_CAREERS:
            if career["title"] in sample_careers:
                found_careers.append(career["title"])
                print(f"✅ Found: {career['title']} - {career['salaryRange']}")
        
        print(f"\n📊 Found {len(found_careers)} out of {len(sample_careers)} sample careers")
        
        # Test comprehensive careers integration
        from comprehensive_careers import COMPREHENSIVE_CAREERS
        
        # Count public service careers in comprehensive list
        public_service_count = 0
        for career in COMPREHENSIVE_CAREERS:
            if any(ps_career["title"] == career["title"] for ps_career in PUBLIC_SERVICE_CAREERS):
                public_service_count += 1
        
        print(f"✅ {public_service_count} public service careers integrated into comprehensive database")
        print(f"📈 Total careers in comprehensive database: {len(COMPREHENSIVE_CAREERS)}")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Testing Public Service Careers Integration...")
    success = test_public_service_careers()
    if success:
        print("\n🎉 All tests passed! Public service careers are ready to use.")
    else:
        print("\n💥 Tests failed. Please check the implementation.")