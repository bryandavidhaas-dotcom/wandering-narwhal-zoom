import json
import re
import sys
import os
from pymongo import MongoClient

# Add the root directory to the Python path to allow for correct module imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.models import CareerModel

def migrate_career_data():
    """
    Migrates career data from frontend/src/utils/careerMatching.ts to the backend MongoDB database.
    """
    # Connect to MongoDB
    client = MongoClient('mongodb://localhost:27017/')
    db = client['career_db']
    careers_collection = db['careers']

    # Load the frontend career data
    try:
        with open('frontend/src/utils/careerMatching.ts', 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print("Error: careerMatching.ts not found. Make sure the frontend directory is in the correct location.")
        return

    # Extract the COMPREHENSIVE_CAREER_TEMPLATES array
    start = content.find('const COMPREHENSIVE_CAREER_TEMPLATES: CareerTemplate[] = [')
    end = content.find('];', start)
    
    if start == -1 or end == -1:
        print("Error: Could not find the COMPREHENSIVE_CAREER_TEMPLATES array in the file.")
        return

    career_data_str = content[start + len('const COMPREHENSIVE_CAREER_TEMPLATES: CareerTemplate[] = '):end+1]
    
    # A more robust way to handle the conversion from TS to JSON
    # This is still not a perfect solution, but it's better than the previous one
    # Add quotes around keys
    json_str = re.sub(r'(\w+):', r'"\1":', career_data_str)
    # Replace single quotes with double quotes
    json_str = json_str.replace("'", '"')
    # Remove trailing commas
    json_str = re.sub(r',\s*([}\]])', r'\1', json_str)
    
    try:
        careers = json.loads(json_str)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return

    # Insert the data into the MongoDB collection
    for career in careers:
        try:
            career_model = CareerModel(**career)
            careers_collection.update_one({'careerType': career_model.careerType}, {'$set': career_model.dict()}, upsert=True)
        except Exception as e:
            print(f"Error processing career: {career.get('title', 'N/A')}. Error: {e}")


    print(f"Successfully migrated {len(careers)} careers to the database.")

if __name__ == "__main__":
    migrate_career_data()