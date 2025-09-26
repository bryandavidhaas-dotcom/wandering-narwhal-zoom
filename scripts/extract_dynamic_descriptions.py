import re
import json
from pathlib import Path

def extract_day_in_life_from_file(file_path: Path) -> dict:
    """Extracts career-specific 'day in life' content from a TypeScript file."""
    if not file_path.exists():
        print(f"File not found: {file_path}")
        return {}
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    descriptions = {}
    
    # Regex to find if-blocks with career title checks and return the description
    pattern = re.compile(
        r'if\s*\((.*?)\)\s*\{.*?return\s*`([^`]*)`',
        re.DOTALL
    )
    
    matches = pattern.finditer(content)
    
    for match in matches:
        condition = match.group(1)
        description = match.group(2).strip()
        
        # Extract career titles from the condition
        titles = re.findall(r'title\.includes\([\'"](.*?)[\'"]\)', condition)
        
        for title in titles:
            if title not in descriptions:
                descriptions[title] = description
    
    # Extract fallback descriptions
    fallback_pattern = re.compile(
        r'return\s*`As a \$\{careerTitle\},([^`]*)`',
        re.DOTALL
    )
    fallback_match = fallback_pattern.search(content)
    if fallback_match:
        descriptions['default'] = fallback_match.group(1).strip()
            
    return descriptions

def main():
    """Main function to extract and save the descriptions."""
    project_root = Path(__file__).parent.parent
    frontend_pages = project_root / "frontend" / "src" / "pages"
    
    files_to_scan = [
        frontend_pages / "Dashboard.tsx",
        frontend_pages / "CareerDetail.tsx"
    ]
    
    all_descriptions = {}
    
    for file_path in files_to_scan:
        print(f"Scanning {file_path.name}...")
        descriptions = extract_day_in_life_from_file(file_path)
        all_descriptions.update(descriptions)
        
    output_file = project_root / "scripts" / "dynamic_descriptions.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_descriptions, f, indent=2, ensure_ascii=False)
        
    print(f"Successfully extracted {len(all_descriptions)} dynamic descriptions to {output_file}")

if __name__ == "__main__":
    main()