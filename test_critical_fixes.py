#!/usr/bin/env python3
"""
🚨 CRITICAL FIXES VERIFICATION TEST 🚨

This test file verifies that the critical fixes implemented on 2025-01-21 are still working.
Run this test before and after any changes to the recommendation system.

Usage: python test_critical_fixes.py
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from backend.simple_server import is_safety_critical_career, extract_resume_insights

def test_safety_system_precision():
    """Test that safety system only blocks truly life-critical careers"""
    print("🧪 Testing Safety System Precision...")
    
    # These should NOT be blocked (were incorrectly blocked before fix)
    non_safety_careers = [
        {"title": "Digital Marketing Specialist", "description": "Manages digital marketing campaigns"},
        {"title": "Software Engineer", "description": "Develops software applications"},
        {"title": "Junior UX Designer", "description": "Designs user experiences"},
        {"title": "Marketing Analyst", "description": "Analyzes marketing data"},
        {"title": "Mechanical Engineer", "description": "Designs mechanical systems"},
        {"title": "Civil Engineer", "description": "Designs infrastructure"},
        {"title": "Electrical Engineer", "description": "Designs electrical systems"},
    ]
    
    # These SHOULD be blocked (truly life-critical)
    safety_critical_careers = [
        {"title": "Nurse Anesthetist", "description": "Administers anesthesia"},
        {"title": "Physician", "description": "Provides medical care"},
        {"title": "Surgeon", "description": "Performs surgery"},
        {"title": "Airline Pilot", "description": "Flies commercial aircraft"},
        {"title": "Paramedic", "description": "Provides emergency medical care"},
    ]
    
    # Test non-safety careers (should NOT be blocked)
    failed_tests = []
    for career in non_safety_careers:
        if is_safety_critical_career(career):
            failed_tests.append(f"❌ FAIL: {career['title']} was incorrectly blocked as safety-critical")
        else:
            print(f"✅ PASS: {career['title']} correctly allowed")
    
    # Test safety-critical careers (SHOULD be blocked)
    for career in safety_critical_careers:
        if not is_safety_critical_career(career):
            failed_tests.append(f"❌ FAIL: {career['title']} was incorrectly allowed (should be blocked)")
        else:
            print(f"✅ PASS: {career['title']} correctly blocked")
    
    return failed_tests

def test_communications_detection():
    """Test that communications and creative skills are properly detected"""
    print("\n🧪 Testing Communications/Creative Skills Detection...")
    
    # Test resume with communications skills
    communications_resume = """
    Marketing Manager with 5 years experience in digital marketing, social media management, 
    content creation, and public relations. Managed brand campaigns and community management.
    """
    
    creative_resume = """
    Graphic Designer with expertise in visual design, branding, web design, video editing,
    and photography. Creative director experience with illustration and art direction.
    """
    
    failed_tests = []
    
    # Test communications detection
    comm_insights = extract_resume_insights(communications_resume)
    comm_freq = comm_insights.get("keyword_frequencies", {}).get("communications", 0)
    if comm_freq < 5:  # Should detect multiple communications keywords
        failed_tests.append(f"❌ FAIL: Communications keywords not detected (found {comm_freq}, expected >5)")
    else:
        print(f"✅ PASS: Communications keywords detected ({comm_freq} mentions)")
    
    # Test creative detection
    creative_insights = extract_resume_insights(creative_resume)
    creative_freq = creative_insights.get("keyword_frequencies", {}).get("creative", 0)
    if creative_freq < 5:  # Should detect multiple creative keywords
        failed_tests.append(f"❌ FAIL: Creative keywords not detected (found {creative_freq}, expected >5)")
    else:
        print(f"✅ PASS: Creative keywords detected ({creative_freq} mentions)")
    
    return failed_tests

def test_theme_detection():
    """Test that dominant themes are correctly identified"""
    print("\n🧪 Testing Theme Detection...")
    
    failed_tests = []
    
    # Test communications theme
    comm_insights = extract_resume_insights("marketing social media content digital marketing communications")
    if comm_insights.get("dominant_theme") != "communications":
        failed_tests.append(f"❌ FAIL: Communications theme not detected (got {comm_insights.get('dominant_theme')})")
    else:
        print("✅ PASS: Communications theme correctly detected")
    
    # Test creative theme  
    creative_insights = extract_resume_insights("design creative graphic design visual branding video")
    if creative_insights.get("dominant_theme") != "creative":
        failed_tests.append(f"❌ FAIL: Creative theme not detected (got {creative_insights.get('dominant_theme')})")
    else:
        print("✅ PASS: Creative theme correctly detected")
    
    return failed_tests

def main():
    """Run all critical fix verification tests"""
    print("🚨 CRITICAL FIXES VERIFICATION TEST")
    print("=" * 50)
    
    all_failures = []
    
    # Run all tests
    all_failures.extend(test_safety_system_precision())
    all_failures.extend(test_communications_detection())
    all_failures.extend(test_theme_detection())
    
    # Report results
    print("\n" + "=" * 50)
    if all_failures:
        print("❌ CRITICAL FIXES VERIFICATION FAILED!")
        print(f"Found {len(all_failures)} issues:")
        for failure in all_failures:
            print(f"  {failure}")
        print("\n🚨 WARNING: The critical fixes may have been reverted!")
        print("🚨 Please review CRITICAL_FIXES_DO_NOT_REVERT.md")
        return 1
    else:
        print("✅ ALL CRITICAL FIXES VERIFICATION PASSED!")
        print("✅ The recommendation system is working correctly.")
        return 0

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)