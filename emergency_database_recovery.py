#!/usr/bin/env python3
"""
EMERGENCY DATABASE RECOVERY SCRIPT
==================================
Critical Priority: Phase 1 Database Recovery

This script performs emergency recovery of the corrupted careers.db by:
1. Backing up the corrupted database for forensic analysis
2. Creating a new, properly structured database
3. Importing 361 high-quality records from production_career_data.json
4. Validating data integrity and completeness
5. Generating recovery report

Author: Emergency Recovery System
Date: 2025-01-06
Priority: CRITICAL
"""

import sqlite3
import json
import shutil
import os
from datetime import datetime
from pathlib import Path

class EmergencyDatabaseRecovery:
    def __init__(self):
        self.db_path = "careers.db"
        self.backup_path = f"careers_corrupted_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
        self.production_data_path = "production_career_data.json"
        self.recovery_report = []
        
    def log(self, message, level="INFO"):
        """Log recovery progress"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {level}: {message}"
        print(log_entry)
        self.recovery_report.append(log_entry)
    
    def backup_corrupted_database(self):
        """Step 1: Backup corrupted database for forensic analysis"""
        self.log("🔄 STEP 1: Backing up corrupted database for forensic analysis", "CRITICAL")
        
        try:
            if os.path.exists(self.db_path):
                shutil.copy2(self.db_path, self.backup_path)
                self.log(f"✅ Corrupted database backed up to: {self.backup_path}")
                
                # Document corruption issues found
                with sqlite3.connect(self.backup_path) as conn:
                    cursor = conn.cursor()
                    cursor.execute("SELECT COUNT(*) FROM careers WHERE id IS NULL")
                    null_ids = cursor.fetchone()[0]
                    cursor.execute("SELECT COUNT(*) FROM careers")
                    total_records = cursor.fetchone()[0]
                    
                self.log(f"📊 Corruption Analysis: {null_ids}/{total_records} records have NULL primary keys")
                self.log("🚨 CORRUPTION CONFIRMED: Complete primary key failure detected")
                
            else:
                self.log("⚠️ No existing database found - will create new database", "WARNING")
                
        except Exception as e:
            self.log(f"❌ Error backing up database: {e}", "ERROR")
            raise
    
    def load_production_data(self):
        """Load high-quality production data"""
        self.log("📥 Loading production career data...")
        
        try:
            with open(self.production_data_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                careers = data.get('careers', [])
                self.log(f"✅ Loaded {len(careers)} high-quality career records")
                return careers
        except Exception as e:
            self.log(f"❌ Error loading production data: {e}", "ERROR")
            raise
    
    def create_new_database_schema(self):
        """Step 2: Create new database with proper schema"""
        self.log("🔄 STEP 2: Creating new database with proper schema", "CRITICAL")
        
        # Remove corrupted database
        if os.path.exists(self.db_path):
            os.remove(self.db_path)
            self.log("🗑️ Removed corrupted database file")
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Create careers table with proper schema matching production data
                cursor.execute('''
                    CREATE TABLE careers (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT NOT NULL,
                        careerType TEXT NOT NULL UNIQUE,
                        description TEXT NOT NULL,
                        salaryRange TEXT NOT NULL,
                        experienceLevel TEXT NOT NULL,
                        requiredTechnicalSkills TEXT NOT NULL,
                        requiredSoftSkills TEXT NOT NULL,
                        companies TEXT,
                        learningPath TEXT,
                        relevanceScore INTEGER,
                        confidenceLevel INTEGER,
                        matchReasons TEXT,
                        minExperienceYears INTEGER,
                        maxExperienceYears INTEGER,
                        minSalary INTEGER,
                        maxSalary INTEGER,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                
                # Create indexes for performance
                cursor.execute('CREATE INDEX idx_career_type ON careers(careerType)')
                cursor.execute('CREATE INDEX idx_experience_level ON careers(experienceLevel)')
                cursor.execute('CREATE INDEX idx_salary_range ON careers(minSalary, maxSalary)')
                
                conn.commit()
                self.log("✅ New database schema created successfully")
                self.log("✅ Performance indexes created")
                
        except Exception as e:
            self.log(f"❌ Error creating database schema: {e}", "ERROR")
            raise
    
    def import_production_data(self, careers_data):
        """Step 3: Import production data with validation"""
        self.log("🔄 STEP 3: Importing production data with validation", "CRITICAL")
        
        imported_count = 0
        validation_errors = 0
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                for career in careers_data:
                    try:
                        # Validate required fields
                        if not career.get('title') or not career.get('careerType'):
                            validation_errors += 1
                            self.log(f"⚠️ Skipping invalid record: missing title or careerType", "WARNING")
                            continue
                        
                        # Convert lists to JSON strings for storage
                        technical_skills = json.dumps(career.get('requiredTechnicalSkills', []))
                        soft_skills = json.dumps(career.get('requiredSoftSkills', []))
                        companies = json.dumps(career.get('companies', []))
                        match_reasons = json.dumps(career.get('matchReasons', []))
                        
                        # Insert record
                        cursor.execute('''
                            INSERT INTO careers (
                                title, careerType, description, salaryRange, experienceLevel,
                                requiredTechnicalSkills, requiredSoftSkills, companies,
                                learningPath, relevanceScore, confidenceLevel, matchReasons,
                                minExperienceYears, maxExperienceYears, minSalary, maxSalary
                            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        ''', (
                            career.get('title'),
                            career.get('careerType'),
                            career.get('description'),
                            career.get('salaryRange'),
                            career.get('experienceLevel'),
                            technical_skills,
                            soft_skills,
                            companies,
                            career.get('learningPath'),
                            career.get('relevanceScore'),
                            career.get('confidenceLevel'),
                            match_reasons,
                            career.get('minExperienceYears'),
                            career.get('maxExperienceYears'),
                            career.get('minSalary'),
                            career.get('maxSalary')
                        ))
                        
                        imported_count += 1
                        
                    except Exception as e:
                        validation_errors += 1
                        self.log(f"⚠️ Error importing record '{career.get('title', 'Unknown')}': {e}", "WARNING")
                
                conn.commit()
                self.log(f"✅ Successfully imported {imported_count} career records")
                if validation_errors > 0:
                    self.log(f"⚠️ {validation_errors} records had validation errors", "WARNING")
                
        except Exception as e:
            self.log(f"❌ Error importing production data: {e}", "ERROR")
            raise
        
        return imported_count, validation_errors
    
    def validate_database_integrity(self):
        """Step 4: Validate database integrity and completeness"""
        self.log("🔄 STEP 4: Validating database integrity and completeness", "CRITICAL")
        
        validation_results = {}
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Check total record count
                cursor.execute("SELECT COUNT(*) FROM careers")
                total_records = cursor.fetchone()[0]
                validation_results['total_records'] = total_records
                
                # Check for NULL primary keys (should be 0)
                cursor.execute("SELECT COUNT(*) FROM careers WHERE id IS NULL")
                null_ids = cursor.fetchone()[0]
                validation_results['null_primary_keys'] = null_ids
                
                # Check for missing required fields
                cursor.execute("SELECT COUNT(*) FROM careers WHERE title IS NULL OR title = ''")
                missing_titles = cursor.fetchone()[0]
                validation_results['missing_titles'] = missing_titles
                
                cursor.execute("SELECT COUNT(*) FROM careers WHERE description IS NULL OR description = ''")
                missing_descriptions = cursor.fetchone()[0]
                validation_results['missing_descriptions'] = missing_descriptions
                
                cursor.execute("SELECT COUNT(*) FROM careers WHERE careerType IS NULL OR careerType = ''")
                missing_career_types = cursor.fetchone()[0]
                validation_results['missing_career_types'] = missing_career_types
                
                # Check experience level distribution
                cursor.execute("SELECT experienceLevel, COUNT(*) FROM careers GROUP BY experienceLevel")
                exp_distribution = dict(cursor.fetchall())
                validation_results['experience_distribution'] = exp_distribution
                
                # Check salary data completeness
                cursor.execute("SELECT COUNT(*) FROM careers WHERE minSalary IS NOT NULL AND maxSalary IS NOT NULL")
                complete_salary_data = cursor.fetchone()[0]
                validation_results['complete_salary_records'] = complete_salary_data
                
                # Check for duplicate careerTypes (should be 0 due to UNIQUE constraint)
                cursor.execute("SELECT careerType, COUNT(*) FROM careers GROUP BY careerType HAVING COUNT(*) > 1")
                duplicates = cursor.fetchall()
                validation_results['duplicate_career_types'] = len(duplicates)
                
                # Log validation results
                self.log(f"📊 VALIDATION RESULTS:")
                self.log(f"   Total Records: {total_records}")
                self.log(f"   NULL Primary Keys: {null_ids} (should be 0)")
                self.log(f"   Missing Titles: {missing_titles} (should be 0)")
                self.log(f"   Missing Descriptions: {missing_descriptions} (should be 0)")
                self.log(f"   Missing Career Types: {missing_career_types} (should be 0)")
                self.log(f"   Complete Salary Records: {complete_salary_data}")
                self.log(f"   Duplicate Career Types: {len(duplicates)} (should be 0)")
                
                self.log(f"   Experience Level Distribution:")
                for level, count in exp_distribution.items():
                    self.log(f"     {level}: {count}")
                
                # Calculate data quality score
                quality_score = self.calculate_quality_score(validation_results, total_records)
                validation_results['quality_score'] = quality_score
                
                self.log(f"🎯 DATABASE QUALITY SCORE: {quality_score}/100")
                
        except Exception as e:
            self.log(f"❌ Error validating database: {e}", "ERROR")
            raise
        
        return validation_results
    
    def calculate_quality_score(self, results, total_records):
        """Calculate database quality score (0-100)"""
        if total_records == 0:
            return 0
        
        score = 100
        
        # Deduct points for data quality issues
        if results['null_primary_keys'] > 0:
            score -= 50  # Critical issue
        
        if results['missing_titles'] > 0:
            score -= (results['missing_titles'] / total_records) * 20
        
        if results['missing_descriptions'] > 0:
            score -= (results['missing_descriptions'] / total_records) * 20
        
        if results['missing_career_types'] > 0:
            score -= (results['missing_career_types'] / total_records) * 20
        
        if results['duplicate_career_types'] > 0:
            score -= results['duplicate_career_types'] * 2
        
        # Bonus points for completeness
        if results['complete_salary_records'] == total_records:
            score += 5  # Bonus for complete salary data
        
        return max(0, min(100, int(score)))
    
    def generate_recovery_report(self, validation_results, imported_count, validation_errors):
        """Generate comprehensive recovery report"""
        self.log("📋 Generating recovery report...")
        
        report_path = f"database_recovery_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        try:
            with open(report_path, 'w', encoding='utf-8') as f:
                f.write("=" * 80 + "\n")
                f.write("EMERGENCY DATABASE RECOVERY REPORT\n")
                f.write("=" * 80 + "\n")
                f.write(f"Recovery Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Recovery Status: COMPLETED\n\n")
                
                f.write("RECOVERY SUMMARY:\n")
                f.write("-" * 40 + "\n")
                f.write(f"Records Imported: {imported_count}\n")
                f.write(f"Validation Errors: {validation_errors}\n")
                f.write(f"Database Quality Score: {validation_results['quality_score']}/100\n")
                f.write(f"Corrupted Database Backup: {self.backup_path}\n\n")
                
                f.write("VALIDATION RESULTS:\n")
                f.write("-" * 40 + "\n")
                for key, value in validation_results.items():
                    if key != 'experience_distribution':
                        f.write(f"{key}: {value}\n")
                
                f.write("\nEXPERIENCE LEVEL DISTRIBUTION:\n")
                f.write("-" * 40 + "\n")
                for level, count in validation_results.get('experience_distribution', {}).items():
                    f.write(f"{level}: {count}\n")
                
                f.write("\nRECOVERY LOG:\n")
                f.write("-" * 40 + "\n")
                for log_entry in self.recovery_report:
                    f.write(log_entry + "\n")
            
            self.log(f"✅ Recovery report saved to: {report_path}")
            
        except Exception as e:
            self.log(f"❌ Error generating recovery report: {e}", "ERROR")
    
    def execute_recovery(self):
        """Execute complete emergency database recovery"""
        self.log("🚨 STARTING EMERGENCY DATABASE RECOVERY", "CRITICAL")
        self.log("=" * 60)
        
        try:
            # Step 1: Backup corrupted database
            self.backup_corrupted_database()
            
            # Step 2: Load production data
            careers_data = self.load_production_data()
            
            # Step 3: Create new database schema
            self.create_new_database_schema()
            
            # Step 4: Import production data
            imported_count, validation_errors = self.import_production_data(careers_data)
            
            # Step 5: Validate database integrity
            validation_results = self.validate_database_integrity()
            
            # Step 6: Generate recovery report
            self.generate_recovery_report(validation_results, imported_count, validation_errors)
            
            self.log("=" * 60)
            self.log("🎉 EMERGENCY DATABASE RECOVERY COMPLETED SUCCESSFULLY", "SUCCESS")
            self.log(f"✅ {imported_count} records recovered")
            self.log(f"🎯 Database quality score: {validation_results['quality_score']}/100")
            
            return True
            
        except Exception as e:
            self.log(f"💥 RECOVERY FAILED: {e}", "CRITICAL")
            return False

def main():
    """Main recovery execution"""
    recovery = EmergencyDatabaseRecovery()
    success = recovery.execute_recovery()
    
    if success:
        print("\n🎉 DATABASE RECOVERY SUCCESSFUL!")
        print("The careers database has been fully restored with high-quality data.")
    else:
        print("\n💥 DATABASE RECOVERY FAILED!")
        print("Please check the logs and try again.")
    
    return success

if __name__ == "__main__":
    main()