#!/usr/bin/env python3
"""
Script to explain what "skill-career connections" means with concrete examples
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from comprehensive_careers import COMPREHENSIVE_CAREERS

def explain_skill_career_connections():
    """Explain what skill-career connections means with examples"""
    
    print("=== WHAT ARE SKILL-CAREER CONNECTIONS? ===\n")
    
    print("A 'skill-career connection' is each individual link between a specific skill and a specific career.")
    print("For example, if 'Python' is required for 50 different careers, that creates 50 skill-career connections.\n")
    
    # Show some concrete examples
    print("CONCRETE EXAMPLES:\n")
    
    # Example 1: Show a specific career and its connections
    data_scientist = next((c for c in COMPREHENSIVE_CAREERS if c['title'] == 'Data Scientist'), None)
    if data_scientist:
        tech_skills = data_scientist.get('requiredTechnicalSkills', [])
        soft_skills = data_scientist.get('requiredSoftSkills', [])
        total_connections = len(tech_skills) + len(soft_skills)
        
        print(f"Career: {data_scientist['title']}")
        print(f"Technical Skills: {tech_skills}")
        print(f"Soft Skills: {soft_skills}")
        print(f"Total skill-career connections for this career: {total_connections}")
        print("(Each skill listed above creates 1 connection to this career)\n")
    
    # Example 2: Show how a popular skill connects to multiple careers
    communication_careers = []
    python_careers = []
    
    for career in COMPREHENSIVE_CAREERS:
        all_skills = career.get('requiredTechnicalSkills', []) + career.get('requiredSoftSkills', [])
        if 'Communication' in all_skills:
            communication_careers.append(career['title'])
        if 'Python' in all_skills:
            python_careers.append(career['title'])
    
    print(f"Example: The skill 'Communication' is required for {len(communication_careers)} careers:")
    for i, career in enumerate(communication_careers[:5]):  # Show first 5
        print(f"  {i+1}. {career}")
    if len(communication_careers) > 5:
        print(f"  ... and {len(communication_careers) - 5} more careers")
    print(f"This creates {len(communication_careers)} skill-career connections just for 'Communication'\n")
    
    print(f"Example: The skill 'Python' is required for {len(python_careers)} careers:")
    for i, career in enumerate(python_careers[:5]):  # Show first 5
        print(f"  {i+1}. {career}")
    if len(python_careers) > 5:
        print(f"  ... and {len(python_careers) - 5} more careers")
    print(f"This creates {len(python_careers)} skill-career connections just for 'Python'\n")
    
    # Calculate total connections
    total_connections = 0
    for career in COMPREHENSIVE_CAREERS:
        tech_skills = career.get('requiredTechnicalSkills', [])
        soft_skills = career.get('requiredSoftSkills', [])
        total_connections += len(tech_skills) + len(soft_skills)
    
    print("=== TOTAL CALCULATION ===")
    print(f"Total careers: {len(COMPREHENSIVE_CAREERS)}")
    print(f"Average skills per career: {total_connections / len(COMPREHENSIVE_CAREERS):.1f}")
    print(f"Total skill-career connections: {total_connections}")
    print("\nThis means our AI analyzes 3,251 individual relationships between specific skills and specific careers")
    print("to understand which skills are needed for which career paths.\n")
    
    print("=== WHY THIS MATTERS FOR USERS ===")
    print("When you take the assessment, the AI:")
    print("1. Identifies your skills and interests")
    print("2. Compares them against all 3,251 skill-career connections")
    print("3. Finds careers where your skills match the requirements")
    print("4. Recommends careers based on the strength of these connections")
    
    return total_connections

if __name__ == "__main__":
    explain_skill_career_connections()