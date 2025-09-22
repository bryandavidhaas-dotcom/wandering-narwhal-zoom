#!/usr/bin/env python3
"""
Script to calculate the actual number of skill combinations across all careers
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from comprehensive_careers import COMPREHENSIVE_CAREERS

def calculate_skill_combinations():
    """Calculate unique skill combinations across all careers"""
    
    # Collect all unique skills from all careers
    all_technical_skills = set()
    all_soft_skills = set()
    
    for career in COMPREHENSIVE_CAREERS:
        # Add technical skills
        if 'requiredTechnicalSkills' in career:
            for skill in career['requiredTechnicalSkills']:
                all_technical_skills.add(skill.strip())
        
        # Add soft skills
        if 'requiredSoftSkills' in career:
            for skill in career['requiredSoftSkills']:
                all_soft_skills.add(skill.strip())
    
    print(f"Total careers: {len(COMPREHENSIVE_CAREERS)}")
    print(f"Unique technical skills: {len(all_technical_skills)}")
    print(f"Unique soft skills: {len(all_soft_skills)}")
    print(f"Total unique skills: {len(all_technical_skills) + len(all_soft_skills)}")
    
    # Calculate skill combinations per career
    total_skill_combinations = 0
    career_skill_combinations = []
    
    for career in COMPREHENSIVE_CAREERS:
        tech_skills = career.get('requiredTechnicalSkills', [])
        soft_skills = career.get('requiredSoftSkills', [])
        total_skills_for_career = len(tech_skills) + len(soft_skills)
        
        # Each career represents a unique combination of its skills
        if total_skills_for_career > 0:
            total_skill_combinations += 1
            career_skill_combinations.append({
                'title': career['title'],
                'tech_skills': len(tech_skills),
                'soft_skills': len(soft_skills),
                'total_skills': total_skills_for_career
            })
    
    print(f"\nSkill combination analysis:")
    print(f"Careers with skill requirements: {len(career_skill_combinations)}")
    print(f"Total unique skill combinations (one per career): {total_skill_combinations}")
    
    # Alternative calculation: unique skill sets
    unique_skill_sets = set()
    for career in COMPREHENSIVE_CAREERS:
        tech_skills = tuple(sorted(career.get('requiredTechnicalSkills', [])))
        soft_skills = tuple(sorted(career.get('requiredSoftSkills', [])))
        skill_combination = (tech_skills, soft_skills)
        unique_skill_sets.add(skill_combination)
    
    print(f"Unique skill set combinations: {len(unique_skill_sets)}")
    
    # Calculate average skills per career
    avg_tech_skills = sum(len(c.get('requiredTechnicalSkills', [])) for c in COMPREHENSIVE_CAREERS) / len(COMPREHENSIVE_CAREERS)
    avg_soft_skills = sum(len(c.get('requiredSoftSkills', [])) for c in COMPREHENSIVE_CAREERS) / len(COMPREHENSIVE_CAREERS)
    
    print(f"\nAverage skills per career:")
    print(f"Technical skills: {avg_tech_skills:.1f}")
    print(f"Soft skills: {avg_soft_skills:.1f}")
    print(f"Total skills: {avg_tech_skills + avg_soft_skills:.1f}")
    
    # Calculate potential skill combinations (mathematical approach)
    # If we consider each career as having a unique combination of skills
    # and each skill can be present or absent, we could calculate combinations
    
    # Simple approach: each career represents a unique skill combination
    # More complex: calculate all possible combinations of skills
    
    # Let's try a different approach: count skill-career mappings
    skill_career_mappings = 0
    for career in COMPREHENSIVE_CAREERS:
        tech_skills = career.get('requiredTechnicalSkills', [])
        soft_skills = career.get('requiredSoftSkills', [])
        skill_career_mappings += len(tech_skills) + len(soft_skills)
    
    print(f"\nTotal skill-career mappings: {skill_career_mappings}")
    
    # Another approach: calculate based on skill frequency
    skill_frequency = {}
    for career in COMPREHENSIVE_CAREERS:
        all_skills = career.get('requiredTechnicalSkills', []) + career.get('requiredSoftSkills', [])
        for skill in all_skills:
            skill_frequency[skill] = skill_frequency.get(skill, 0) + 1
    
    print(f"Most common skills:")
    sorted_skills = sorted(skill_frequency.items(), key=lambda x: x[1], reverse=True)
    for skill, count in sorted_skills[:10]:
        print(f"  {skill}: {count} careers")
    
    # Calculate a more meaningful "skill combinations" metric
    # This could be the number of unique ways skills are combined across careers
    print(f"\n=== SUMMARY ===")
    print(f"Total careers: {len(COMPREHENSIVE_CAREERS)}")
    print(f"Unique skill combinations (one per career): {total_skill_combinations}")
    print(f"Total skill-career connections: {skill_career_mappings}")
    print(f"Unique skill sets: {len(unique_skill_sets)}")
    
    return {
        'total_careers': len(COMPREHENSIVE_CAREERS),
        'unique_skill_combinations': total_skill_combinations,
        'skill_career_mappings': skill_career_mappings,
        'unique_skill_sets': len(unique_skill_sets),
        'total_unique_skills': len(all_technical_skills) + len(all_soft_skills)
    }

if __name__ == "__main__":
    calculate_skill_combinations()