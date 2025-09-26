#!/usr/bin/env python3
"""
Extract all career templates from frontend files
"""
import os
import re
import json
from pathlib import Path

def extract_careers_from_file(file_path: Path) -> list:
    """Extract career objects from a TypeScript file."""
    if not file_path.exists():
        print(f"File not found: {file_path}")
        return []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        careers = []
        
        # Look for career objects (they have title, salaryRange, description)
        career_pattern = r'\{\s*title:\s*["\'][^"\']+["\'][^}]*salaryRange:[^}]*description:[^}]*?\}'
        
        # Find all potential career objects
        matches = re.finditer(career_pattern, content, re.DOTALL)
        
        for match in matches:
            try:
                # Extract the full object by finding matching braces
                start_pos = match.start()
                obj_content = extract_full_object(content, start_pos)
                
                if obj_content:
                    career = parse_career_object(obj_content)
                    if career and career.get('title'):
                        careers.append(career)
                        
            except Exception as e:
                print(f"Error parsing career object: {e}")
                continue
        
        return careers
        
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return []

def extract_full_object(content: str, start_pos: int) -> str:
    """Extract a complete object from { to matching }."""
    brace_count = 0
    pos = start_pos
    
    while pos < len(content):
        char = content[pos]
        if char == '{':
            brace_count += 1
        elif char == '}':
            brace_count -= 1
            if brace_count == 0:
                return content[start_pos:pos + 1]
        pos += 1
    
    return ""

def parse_career_object(obj_str: str) -> dict:
    """Parse a TypeScript career object into a Python dict."""
    career = {}
    
    # Extract key-value pairs
    patterns = [
        (r'title:\s*["\']([^"\']*)["\']', 'title'),
        (r'salaryRange:\s*["\']([^"\']*)["\']', 'salaryRange'),
        (r'description:\s*["\']([^"\']*)["\']', 'description'),
        (r'careerType:\s*["\']([^"\']*)["\']', 'careerType'),
        (r'experienceLevel:\s*["\']([^"\']*)["\']', 'experienceLevel'),
        (r'learningPath:\s*["\']([^"\']*)["\']', 'learningPath'),
        (r'stretchLevel:\s*["\']([^"\']*)["\']', 'stretchLevel'),
        (r'dayInLife:\s*["\']([^"\']*)["\']', 'dayInLife'),
        (r'remoteOptions:\s*["\']([^"\']*)["\']', 'remoteOptions'),
        (r'requiredEducation:\s*["\']([^"\']*)["\']', 'requiredEducation'),
        (r'preferredEducation:\s*["\']([^"\']*)["\']', 'preferredEducation'),
        (r'agePreference:\s*["\']([^"\']*)["\']', 'agePreference'),
        (r'locationFlexibility:\s*["\']([^"\']*)["\']', 'locationFlexibility'),
    ]
    
    for pattern, key in patterns:
        match = re.search(pattern, obj_str)
        if match:
            career[key] = match.group(1)
    
    # Extract numeric fields
    numeric_patterns = [
        (r'workDataWeight:\s*(\d+)', 'workDataWeight'),
        (r'workPeopleWeight:\s*(\d+)', 'workPeopleWeight'),
        (r'creativityWeight:\s*(\d+)', 'creativityWeight'),
        (r'problemSolvingWeight:\s*(\d+)', 'problemSolvingWeight'),
        (r'leadershipWeight:\s*(\d+)', 'leadershipWeight'),
        (r'handsOnWorkWeight:\s*(\d+)', 'handsOnWorkWeight'),
        (r'physicalWorkWeight:\s*(\d+)', 'physicalWorkWeight'),
        (r'outdoorWorkWeight:\s*(\d+)', 'outdoorWorkWeight'),
        (r'mechanicalAptitudeWeight:\s*(\d+)', 'mechanicalAptitudeWeight'),
        (r'workLifeBalanceRating:\s*(\d+)', 'workLifeBalanceRating'),
        (r'minYearsExperience:\s*(\d+)', 'minYearsExperience'),
        (r'maxYearsExperience:\s*(\d+)', 'maxYearsExperience'),
        (r'salaryMin:\s*(\d+)', 'salaryMin'),
        (r'salaryMax:\s*(\d+)', 'salaryMax'),
    ]
    
    for pattern, key in numeric_patterns:
        match = re.search(pattern, obj_str)
        if match:
            career[key] = int(match.group(1))
    
    # Extract boolean fields
    boolean_patterns = [
        (r'requiresTechnical:\s*(true|false)', 'requiresTechnical'),
        (r'transitionFriendly:\s*(true|false)', 'transitionFriendly'),
        (r'skillBasedEntry:\s*(true|false)', 'skillBasedEntry'),
        (r'experienceCanSubstitute:\s*(true|false)', 'experienceCanSubstitute'),
    ]
    
    for pattern, key in boolean_patterns:
        match = re.search(pattern, obj_str)
        if match:
            career[key] = match.group(1) == 'true'
    
    # Extract array fields
    array_patterns = [
        (r'requiredTechnicalSkills:\s*\[(.*?)\]', 'requiredTechnicalSkills'),
        (r'requiredSoftSkills:\s*\[(.*?)\]', 'requiredSoftSkills'),
        (r'preferredInterests:\s*\[(.*?)\]', 'preferredInterests'),
        (r'preferredIndustries:\s*\[(.*?)\]', 'preferredIndustries'),
        (r'companies:\s*\[(.*?)\]', 'companies'),
        (r'workEnvironments:\s*\[(.*?)\]', 'workEnvironments'),
        (r'valuedCertifications:\s*\[(.*?)\]', 'valuedCertifications'),
        (r'requiredCertifications:\s*\[(.*?)\]', 'requiredCertifications'),
        (r'resumeKeywords:\s*\[(.*?)\]', 'resumeKeywords'),
        (r'relatedJobTitles:\s*\[(.*?)\]', 'relatedJobTitles'),
        (r'valuedCompanies:\s*\[(.*?)\]', 'valuedCompanies'),
        (r'preferredIndustryExperience:\s*\[(.*?)\]', 'preferredIndustryExperience'),
        (r'careerProgressionPatterns:\s*\[(.*?)\]', 'careerProgressionPatterns'),
        (r'alternativeQualifications:\s*\[(.*?)\]', 'alternativeQualifications'),
    ]
    
    for pattern, key in array_patterns:
        match = re.search(pattern, obj_str, re.DOTALL)
        if match:
            array_content = match.group(1)
            # Parse array items
            items = []
            if array_content.strip():
                # Split by comma and clean up
                raw_items = re.findall(r'["\']([^"\']*)["\']', array_content)
                items = [item.strip() for item in raw_items if item.strip()]
            career[key] = items
    
    return career

def main():
    """Extract all careers from frontend files."""
    project_root = Path(__file__).parent.parent
    frontend_utils = project_root / "frontend" / "src" / "utils"
    
    all_careers = []
    
    # Files to check
    files_to_check = [
        frontend_utils / "careerMatching.ts",
        frontend_utils / "tradesCareerTemplates.ts",
        frontend_utils / "placeholder_templates.ts"
    ]
    
    for file_path in files_to_check:
        print(f"Extracting careers from: {file_path}")
        careers = extract_careers_from_file(file_path)
        print(f"Found {len(careers)} careers in {file_path.name}")
        all_careers.extend(careers)
    
    # Remove duplicates based on careerType
    unique_careers = {}
    for career in all_careers:
        career_type = career.get('careerType', career.get('title', '').lower().replace(' ', '-'))
        if career_type not in unique_careers:
            unique_careers[career_type] = career
    
    final_careers = list(unique_careers.values())
    
    print(f"\nTotal unique careers found: {len(final_careers)}")
    
    # Save to JSON file for the migration script to use
    output_file = project_root / "scripts" / "extracted_careers.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(final_careers, f, indent=2, ensure_ascii=False)
    
    print(f"Careers saved to: {output_file}")
    
    # Show sample
    if final_careers:
        print(f"\nSample career: {final_careers[0].get('title', 'Unknown')}")

if __name__ == "__main__":
    main()