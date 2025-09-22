#!/usr/bin/env python3
"""
Script to count careers by category for accurate frontend display
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from comprehensive_careers import COMPREHENSIVE_CAREERS
    from healthcare_careers import HEALTHCARE_CAREERS
    from skilled_trades_careers import SKILLED_TRADES_CAREERS
    from education_careers import EDUCATION_CAREERS
    from business_finance_careers import BUSINESS_FINANCE_CAREERS
    from legal_law_careers import LEGAL_LAW_CAREERS
    from creative_arts_careers import CREATIVE_ARTS_CAREERS
    from public_service_careers import PUBLIC_SERVICE_CAREERS
    from hospitality_service_careers import HOSPITALITY_SERVICE_CAREERS
    from manufacturing_industrial_careers import MANUFACTURING_INDUSTRIAL_CAREERS
    from agriculture_environment_careers import AGRICULTURE_ENVIRONMENT_CAREERS
    
    print("Career counts by source module:")
    print(f"Healthcare: {len(HEALTHCARE_CAREERS)}")
    print(f"Skilled Trades: {len(SKILLED_TRADES_CAREERS)}")
    print(f"Education: {len(EDUCATION_CAREERS)}")
    print(f"Business & Finance: {len(BUSINESS_FINANCE_CAREERS)}")
    print(f"Legal & Law: {len(LEGAL_LAW_CAREERS)}")
    print(f"Creative & Arts: {len(CREATIVE_ARTS_CAREERS)}")
    print(f"Public Service: {len(PUBLIC_SERVICE_CAREERS)}")
    print(f"Hospitality & Service: {len(HOSPITALITY_SERVICE_CAREERS)}")
    print(f"Manufacturing & Industrial: {len(MANUFACTURING_INDUSTRIAL_CAREERS)}")
    print(f"Agriculture & Environment: {len(AGRICULTURE_ENVIRONMENT_CAREERS)}")
    
    # Count technology/engineering careers (those in main comprehensive_careers.py file)
    module_careers_count = (len(HEALTHCARE_CAREERS) + len(SKILLED_TRADES_CAREERS) + len(EDUCATION_CAREERS) +
                           len(BUSINESS_FINANCE_CAREERS) + len(LEGAL_LAW_CAREERS) + len(CREATIVE_ARTS_CAREERS) +
                           len(PUBLIC_SERVICE_CAREERS) + len(HOSPITALITY_SERVICE_CAREERS) +
                           len(MANUFACTURING_INDUSTRIAL_CAREERS) + len(AGRICULTURE_ENVIRONMENT_CAREERS))
    main_careers = len(COMPREHENSIVE_CAREERS) - module_careers_count
    print(f"Technology & Engineering (main file): {main_careers}")
    
    total_from_modules = module_careers_count + main_careers
    print(f"\nTotal from modules: {total_from_modules}")
    print(f"Total in comprehensive: {len(COMPREHENSIVE_CAREERS)}")
    
    # Count Product Management careers specifically
    product_careers = [c for c in COMPREHENSIVE_CAREERS if 'product' in c.get('title', '').lower()]
    print(f"Product Management careers: {len(product_careers)}")
    
except ImportError as e:
    print(f"Import error: {e}")
except Exception as e:
    print(f"Error: {e}")