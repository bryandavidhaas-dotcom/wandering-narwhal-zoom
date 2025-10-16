import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from backend.recommendation_engine.unified_api import UnifiedRecommendationAPI

def get_career_stats():
    try:
        # The database is expected to be in the backend directory
        api = UnifiedRecommendationAPI(career_db_path="backend/careers.db")
        stats = api.get_database_statistics()
        if stats and stats.get('total_careers') is not None:
            print(f"Database statistics: {stats}")
        else:
            print("Could not retrieve statistics. The database might be empty or uninitialized.")
            
    except Exception as e:
        print(f"An error occurred: {e}")
        print("This might be because the database file 'backend/careers.db' does not exist or is corrupted.")
        print("Please ensure the database is properly initialized before running this script.")

if __name__ == "__main__":
    get_career_stats()