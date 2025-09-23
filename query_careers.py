import sqlite3
import json

def query_career_by_title(title):
    db_path = 'careers.db'
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM careers WHERE title LIKE ?", (f'%{title}%',))
        
        rows = cursor.fetchall()
        
        if rows:
            for row in rows:
                print(json.dumps(dict(row), indent=2))
        else:
            print(f"No career found with title: {title}")
            
        conn.close()
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    print("Querying for 'Delivery Driver'...")
    query_career_by_title("Delivery Driver")
    print("\nQuerying for 'Medical Assistant'...")
    query_career_by_title("Medical Assistant")