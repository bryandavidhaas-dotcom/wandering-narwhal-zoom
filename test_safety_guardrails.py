#!/usr/bin/env python3
"""
Test script to verify the safety guardrails are working correctly.
This tests the backend safety functions to ensure CRNA is blocked for non-medical users.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from backend.simple_server import is_safety_critical_career, has_relevant_background_for_safety_critical

def test_crna_safety_check():
    """Test that CRNA is correctly identified as safety-critical and blocked for non-medical users"""
    
    # Mock CRNA career data
    crna_career = {
        "title": "Nurse Anesthetist (CRNA)",
        "description": "Administers anesthesia and monitors patients during surgical procedures. Requires specialized medical training and certification."
    }
    
    # Mock Product Manager user data (like Bryan)
    product_manager_user = {
        "education_level": "Bachelor's in Business",
        "certifications": ["PMP", "Agile Certified"],
        "technical_skills": ["Product Management", "Analytics", "Roadmapping"],
        "resume_text": "Senior Product Manager with 20+ years experience in product strategy, roadmap development, and team leadership. Led multiple product launches and managed cross-functional teams.",
        "current_role": "Senior Product Manager"
    }
    
    # Mock resume insights for Product Manager
    product_manager_insights = {
        "industry_indicators": ["technology"],
        "roles": ["Product Management"],
        "current_role": "Product Management"
    }
    
    # Mock medical professional user data
    medical_user = {
        "education_level": "Doctor of Nursing Practice",
        "certifications": ["RN", "CRNA"],
        "technical_skills": ["Anesthesia", "Patient Monitoring", "Medical Equipment"],
        "resume_text": "Registered Nurse with 10 years experience in critical care and anesthesia. Completed CRNA program and certified to administer anesthesia.",
        "current_role": "Registered Nurse"
    }
    
    # Mock resume insights for medical professional
    medical_insights = {
        "industry_indicators": ["healthcare"],
        "roles": ["Nursing"],
        "current_role": "Nursing"
    }
    
    print("🧪 Testing Safety Guardrails for CRNA Career")
    print("=" * 50)
    
    # Test 1: Is CRNA identified as safety-critical?
    is_safety_critical = is_safety_critical_career(crna_career)
    print(f"✅ Test 1 - CRNA identified as safety-critical: {is_safety_critical}")
    assert is_safety_critical, "CRNA should be identified as safety-critical"
    
    # Test 2: Product Manager should be blocked from CRNA
    pm_has_background = has_relevant_background_for_safety_critical(crna_career, product_manager_user, product_manager_insights)
    print(f"🚫 Test 2 - Product Manager blocked from CRNA: {not pm_has_background}")
    assert not pm_has_background, "Product Manager should NOT have relevant background for CRNA"
    
    # Test 3: Medical professional should be allowed CRNA
    medical_has_background = has_relevant_background_for_safety_critical(crna_career, medical_user, medical_insights)
    print(f"✅ Test 3 - Medical professional allowed CRNA: {medical_has_background}")
    assert medical_has_background, "Medical professional SHOULD have relevant background for CRNA"
    
    print("\n🎉 ALL SAFETY TESTS PASSED!")
    print("✅ CRNA will be blocked for Product Managers")
    print("✅ CRNA will be allowed for qualified medical professionals")
    print("✅ Safety guardrails are working correctly!")

if __name__ == "__main__":
    test_crna_safety_check()