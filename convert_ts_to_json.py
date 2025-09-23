import json
import re

def convert_ts_to_json():
    """
    Converts the TypeScript career templates file to a JSON file.
    """
    try:
        with open('frontend/src/utils/tradesCareerTemplates.ts', 'r', encoding='utf-8') as f:
            ts_content = f.read()
    except FileNotFoundError:
        print("Error: frontend/src/utils/tradesCareerTemplates.ts not found.")
        return

    # A more robust regex to find the array, ignoring comments
    match = re.search(r'export const TRADES_CAREER_TEMPLATES: CareerTemplate\[\] = (\[.*?\]);', ts_content, re.DOTALL)
    if not match:
        print("Error: Could not find TRADES_CAREER_TEMPLATES array in the TypeScript file.")
        return
    
    array_str = match.group(1)

    # This is a simplified parser and may need to be more robust
    # Remove comments
    array_str = re.sub(r'//.*?\n', '', array_str)
    # Convert JS object keys to JSON strings
    array_str = re.sub(r'(\s*)(\w+):', r'\1"\2":', array_str)
    # Convert single quotes to double quotes
    array_str = array_str.replace("'", '"')
    # Remove trailing commas
    array_str = re.sub(r',\s*([\}\]])', r'\1', array_str)

    try:
        trades_careers = json.loads(array_str)
        with open('trades_careers.json', 'w', encoding='utf-8') as f:
            json.dump(trades_careers, f, indent=2)
        print(f"Successfully converted {len(trades_careers)} careers to trades_careers.json")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from TypeScript file: {e}")

if __name__ == "__main__":
    convert_ts_to_json()