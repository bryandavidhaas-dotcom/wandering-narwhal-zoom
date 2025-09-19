#!/usr/bin/env python3
"""
Test script for the new dynamic distribution system based on exploration level.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from simple_server import calculate_dynamic_distribution

def test_dynamic_distribution():
    """Test the dynamic distribution function with all exploration levels"""
    
    print("🧪 Testing Dynamic Distribution System")
    print("=" * 50)
    
    # Test all exploration levels
    expected_distributions = {
        1: (5, 3, 1, 9),   # Conservative: Heavy Safe Zone
        2: (4, 4, 2, 10),  # Cautious: Safe Zone preference  
        3: (3, 4, 4, 11),  # Balanced: Equal focus on Stretch/Adventure
        4: (2, 4, 5, 11),  # Adventurous: Adventure Zone focus
        5: (2, 3, 6, 11)   # Explorer: Maximum Adventure
    }
    
    all_tests_passed = True
    
    for level in range(1, 6):
        print(f"\n🔍 Testing Exploration Level {level}")
        
        safe, stretch, adventure, total = calculate_dynamic_distribution(level)
        expected = expected_distributions[level]
        
        if (safe, stretch, adventure, total) == expected:
            print(f"✅ PASS: Level {level} - Safe:{safe}, Stretch:{stretch}, Adventure:{adventure}, Total:{total}")
        else:
            print(f"❌ FAIL: Level {level}")
            print(f"   Expected: Safe:{expected[0]}, Stretch:{expected[1]}, Adventure:{expected[2]}, Total:{expected[3]}")
            print(f"   Got:      Safe:{safe}, Stretch:{stretch}, Adventure:{adventure}, Total:{total}")
            all_tests_passed = False
    
    # Test edge cases
    print(f"\n🔍 Testing Edge Cases")
    
    # Test None exploration level (should default to 1)
    safe, stretch, adventure, total = calculate_dynamic_distribution(None)
    if (safe, stretch, adventure, total) == expected_distributions[1]:
        print(f"✅ PASS: None exploration level defaults to level 1")
    else:
        print(f"❌ FAIL: None exploration level handling")
        all_tests_passed = False
    
    # Test out-of-range values
    for test_level, expected_level in [(0, 1), (-1, 1), (6, 5), (10, 5)]:
        safe, stretch, adventure, total = calculate_dynamic_distribution(test_level)
        expected = expected_distributions[expected_level]
        if (safe, stretch, adventure, total) == expected:
            print(f"✅ PASS: Level {test_level} clamped to level {expected_level}")
        else:
            print(f"❌ FAIL: Level {test_level} clamping")
            all_tests_passed = False
    
    # Verify total recommendations are within 9-12 range
    print(f"\n🔍 Verifying Total Range (9-12 recommendations)")
    for level in range(1, 6):
        _, _, _, total = calculate_dynamic_distribution(level)
        if 9 <= total <= 12:
            print(f"✅ PASS: Level {level} total ({total}) within range")
        else:
            print(f"❌ FAIL: Level {level} total ({total}) outside 9-12 range")
            all_tests_passed = False
    
    print(f"\n" + "=" * 50)
    if all_tests_passed:
        print("🎉 ALL TESTS PASSED! Dynamic distribution system working correctly.")
    else:
        print("❌ SOME TESTS FAILED! Please check the implementation.")
    
    return all_tests_passed

def test_distribution_characteristics():
    """Test that the distribution characteristics match exploration behavior"""
    
    print(f"\n🧪 Testing Distribution Characteristics")
    print("=" * 50)
    
    distributions = {}
    for level in range(1, 6):
        safe, stretch, adventure, total = calculate_dynamic_distribution(level)
        distributions[level] = {
            'safe': safe,
            'stretch': stretch, 
            'adventure': adventure,
            'total': total,
            'safe_pct': round(safe/total * 100, 1),
            'stretch_pct': round(stretch/total * 100, 1),
            'adventure_pct': round(adventure/total * 100, 1)
        }
    
    print("Distribution Analysis:")
    print("Level | Safe | Stretch | Adventure | Total | Safe% | Stretch% | Adventure%")
    print("-" * 75)
    
    for level in range(1, 6):
        d = distributions[level]
        print(f"  {level}   |  {d['safe']}   |    {d['stretch']}    |     {d['adventure']}     |  {d['total']}   | {d['safe_pct']:4.1f}% |  {d['stretch_pct']:4.1f}%  |   {d['adventure_pct']:4.1f}%")
    
    # Verify characteristics
    print(f"\n🔍 Verifying Exploration Characteristics:")
    
    # Safe zone should decrease as exploration increases
    safe_decreasing = all(distributions[i]['safe'] >= distributions[i+1]['safe'] for i in range(1, 5))
    print(f"✅ Safe zone decreases with exploration: {safe_decreasing}")
    
    # Adventure zone should increase as exploration increases  
    adventure_increasing = all(distributions[i]['adventure'] <= distributions[i+1]['adventure'] for i in range(1, 5))
    print(f"✅ Adventure zone increases with exploration: {adventure_increasing}")
    
    # Level 1 should be most conservative (highest safe %)
    most_conservative = distributions[1]['safe_pct'] == max(d['safe_pct'] for d in distributions.values())
    print(f"✅ Level 1 is most conservative: {most_conservative}")
    
    # Level 5 should be most adventurous (highest adventure %)
    most_adventurous = distributions[5]['adventure_pct'] == max(d['adventure_pct'] for d in distributions.values())
    print(f"✅ Level 5 is most adventurous: {most_adventurous}")
    
    return safe_decreasing and adventure_increasing and most_conservative and most_adventurous

if __name__ == "__main__":
    print("🚀 Starting Dynamic Distribution Tests")
    
    basic_tests = test_dynamic_distribution()
    characteristic_tests = test_distribution_characteristics()
    
    print(f"\n" + "=" * 60)
    if basic_tests and characteristic_tests:
        print("🎉 ALL TESTS PASSED! The dynamic distribution system is working correctly.")
        print("✅ Ready for production use!")
    else:
        print("❌ TESTS FAILED! Please review the implementation.")
        sys.exit(1)