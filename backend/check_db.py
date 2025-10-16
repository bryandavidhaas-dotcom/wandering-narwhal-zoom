import sqlite3
import os

# Check if careers.db exists and examine its structure
if os.path.exists('careers.db'):
    conn = sqlite3.connect('careers.db')
    cursor = conn.cursor()
    
    # Get all table names
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print('Tables in careers.db:')
    for table in tables:
        print(f'  - {table[0]}')
    
    # Check if there's a users table
    if any('user' in table[0].lower() for table in tables):
        for table in tables:
            if 'user' in table[0].lower():
                print(f'\nExamining {table[0]} table:')
                cursor.execute(f'PRAGMA table_info({table[0]})')
                columns = cursor.fetchall()
                for col in columns:
                    print(f'  Column: {col[1]} ({col[2]})')
                
                # Check for the specific user
                cursor.execute(f"SELECT * FROM {table[0]} WHERE email LIKE '%bryandavidhaas@gmail.com%'")
                user_data = cursor.fetchall()
                if user_data:
                    print(f'Found user data: {user_data}')
                else:
                    print('No user found with email bryandavidhaas@gmail.com')
                
                # Show all users
                cursor.execute(f'SELECT email FROM {table[0]} LIMIT 10')
                all_users = cursor.fetchall()
                print(f'Sample users in database: {all_users}')
    else:
        print('No users table found in careers.db')
    
    conn.close()
else:
    print('careers.db file not found')