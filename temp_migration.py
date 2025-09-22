import sys
from pathlib import Path
import json

# Add the project root to the Python path
project_root = Path(__file__).parent.resolve()
sys.path.append(str(project_root))

from recommendation_engine.career_database import migrate_frontend_careers_to_database, CareerDatabase

try:
    # Load the career types from the JSON file
    with open(project_root / 'all_career_types.json', 'r') as f:
        all_career_types = json.load(f)

    # Initialize the database and run the migration
    db = CareerDatabase(str(project_root / 'careers.db'))
    migrated_count = migrate_frontend_careers_to_database(db, all_career_types)
    print(f'Successfully migrated {migrated_count} careers.')

except FileNotFoundError:
    print("Error: 'all_career_types.json' not found. Make sure the file exists in the project root.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")