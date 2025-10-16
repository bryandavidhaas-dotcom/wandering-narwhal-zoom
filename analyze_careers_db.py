import sqlite3
import json
from pathlib import Path

def analyze_careers_database():
    """Comprehensive analysis of the careers.db SQLite database"""
    
    db_path = Path("careers.db")
    
    if not db_path.exists():
        print(f"❌ Database file not found at: {db_path}")
        return
    
    print("🔍 CAREERS DATABASE ANALYSIS")
    print("=" * 50)
    
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            
            # Get database schema
            print("\n📋 DATABASE SCHEMA:")
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            
            if not tables:
                print("❌ No tables found in database")
                return
                
            for table in tables:
                table_name = table[0]
                print(f"\n🗂️  Table: {table_name}")
                
                # Get table schema
                cursor.execute(f"PRAGMA table_info({table_name});")
                columns = cursor.fetchall()
                
                print("   Columns:")
                for col in columns:
                    col_id, name, data_type, not_null, default, pk = col
                    pk_indicator = " (PRIMARY KEY)" if pk else ""
                    null_indicator = " NOT NULL" if not_null else ""
                    default_indicator = f" DEFAULT {default}" if default else ""
                    print(f"     - {name}: {data_type}{pk_indicator}{null_indicator}{default_indicator}")
                
                # Get record count
                cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
                count = cursor.fetchone()[0]
                print(f"   📊 Record Count: {count}")
                
                # Sample a few records if they exist
                if count > 0:
                    cursor.execute(f"SELECT * FROM {table_name} LIMIT 3;")
                    sample_records = cursor.fetchall()
                    
                    print("   📝 Sample Records:")
                    column_names = [desc[0] for desc in cursor.description]
                    
                    for i, record in enumerate(sample_records, 1):
                        print(f"     Record {i}:")
                        for col_name, value in zip(column_names, record):
                            # Truncate long values for readability
                            display_value = str(value)[:100] + "..." if len(str(value)) > 100 else str(value)
                            print(f"       {col_name}: {display_value}")
                        print()
            
            # Analyze data quality for careers table specifically
            if any(table[0] == 'careers' for table in tables):
                print("\n🔍 DATA QUALITY ANALYSIS (careers table):")
                
                # Check for placeholder/generic data
                cursor.execute("SELECT COUNT(*) FROM careers WHERE description LIKE '%brief description%';")
                brief_desc_count = cursor.fetchone()[0]
                print(f"   📝 Records with 'brief description': {brief_desc_count}")
                
                cursor.execute("SELECT COUNT(*) FROM careers WHERE description LIKE '%A brief description%';")
                generic_desc_count = cursor.fetchone()[0]
                print(f"   📝 Records with generic 'A brief description': {generic_desc_count}")
                
                # Check for placeholder technical skills
                cursor.execute("SELECT COUNT(*) FROM careers WHERE requiredTechnicalSkills LIKE '%Technical Skill 1%';")
                placeholder_skills_count = cursor.fetchone()[0]
                print(f"   🛠️  Records with placeholder technical skills: {placeholder_skills_count}")
                
                # Check salary data consistency
                cursor.execute("SELECT COUNT(*) FROM careers WHERE salaryRange = '85000-135000';")
                same_salary_count = cursor.fetchone()[0]
                print(f"   💰 Records with identical salary range (85000-135000): {same_salary_count}")
                
                # Check experience level consistency
                cursor.execute("SELECT experienceLevel, COUNT(*) FROM careers GROUP BY experienceLevel;")
                exp_levels = cursor.fetchall()
                print(f"   📈 Experience Level Distribution:")
                for level, count in exp_levels:
                    print(f"       {level}: {count}")
                
                # Check for missing or empty fields
                cursor.execute("SELECT COUNT(*) FROM careers WHERE description IS NULL OR description = '';")
                empty_desc = cursor.fetchone()[0]
                print(f"   ❌ Records with empty descriptions: {empty_desc}")
                
                cursor.execute("SELECT COUNT(*) FROM careers WHERE companies IS NULL OR companies = '';")
                empty_companies = cursor.fetchone()[0]
                print(f"   🏢 Records with empty companies: {empty_companies}")
                
    except sqlite3.Error as e:
        print(f"❌ SQLite error: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    analyze_careers_database()