#!/usr/bin/env python3
"""
Test script to verify Creative & Arts careers are loaded properly
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
        from comprehensive_careers import COMPREHENSIVE_CAREERS
        
        # Count total careers
        total_careers = len(COMPREHENSIVE_CAREERS)
        print(f"Total careers loaded: {total_careers}")
        
        # Find creative careers
        creative_careers = []
        for career in COMPREHENSIVE_CAREERS:
            title = career.get('title', '').lower()
            if any(keyword in title for keyword in ['creative', 'designer', 'artist', 'graphic', 'ux', 'ui', 'motion', 'brand', 'video', 'photo', 'illustrator', 'animator', 'art']):
                creative_careers.append(career['title'])
        
        print(f"\nCreative & Arts careers found: {len(creative_careers)}")
        print("Creative careers:")
        for i, career in enumerate(creative_careers[:15], 1):  # Show first 15
            print(f"{i:2d}. {career}")
        
        if len(creative_careers) > 15:
            print(f"... and {len(creative_careers) - 15} more")
        
except ImportError as e:
    print(f"Import error: {e}")
except Exception as e:
    print(f"Error: {e}")