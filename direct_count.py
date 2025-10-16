import sqlite3
from pathlib import Path

def count_careers_directly():
    db_path = Path("backend/careers.db")
    
    if not db_path.exists():
        print(f"Database file not found at: {db_path}")
        return

    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.execute("SELECT COUNT(*) FROM careers")
            count = cursor.fetchone()
            print(f"Total careers in database: {count}")
            
    except sqlite3.OperationalError as e:
        print(f"An error occurred: {e}")
        print("This might be because the 'careers' table does not exist in the database.")
        
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    count_careers_directly()