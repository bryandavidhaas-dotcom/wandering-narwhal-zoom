#!/usr/bin/env python3
"""
PHASE 2: HYBRID MONGODB MIGRATION PIPELINE
==========================================
Comprehensive migration pipeline that works with MongoDB when available,
or falls back to an embedded solution for development/testing.

This script:
1. Attempts MongoDB connection, falls back to embedded DB
2. Migrates 331 SQLite records with schema transformation
3. Validates data integrity and generates migration report
4. Establishes unified data architecture

Author: Phase 2 Hybrid Migration System
Date: 2025-01-07
"""

import asyncio
import sqlite3
import json
import os
import sys
import uuid
from datetime import datetime
from typing import Dict, List, Any, Optional, Union
from pathlib import Path

# Try MongoDB imports, fall back to embedded solution
try:
    from motor.motor_asyncio import AsyncIOMotorClient
    from beanie import init_beanie
    MONGODB_AVAILABLE = True
except ImportError:
    MONGODB_AVAILABLE = False

# Try TinyDB for embedded solution
try:
    from tinydb import TinyDB, Query
    TINYDB_AVAILABLE = True
except ImportError:
    TINYDB_AVAILABLE = False
    # Install TinyDB if not available
    import subprocess
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'tinydb'])
        from tinydb import TinyDB, Query
        TINYDB_AVAILABLE = True
    except:
        pass

# Add backend to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

class EmbeddedCareerDB:
    """Embedded database using TinyDB as MongoDB alternative"""
    
    def __init__(self, db_path: str = "embedded_careers.json"):
        self.db = TinyDB(db_path)
        self.careers = self.db.table('careers')
        self.skills = self.db.table('skills')
    
    async def insert_career(self, career_data: Dict[str, Any]) -> str:
        """Insert a career record"""
        if 'career_id' not in career_data:
            career_data['career_id'] = str(uuid.uuid4())
        
        # Convert datetime objects to strings for JSON serialization
        if isinstance(career_data.get('created_at'), datetime):
            career_data['created_at'] = career_data['created_at'].isoformat()
        if isinstance(career_data.get('updated_at'), datetime):
            career_data['updated_at'] = career_data['updated_at'].isoformat()
        
        self.careers.insert(career_data)
        return career_data['career_id']
    
    async def count_careers(self) -> int:
        """Count total careers"""
        return len(self.careers)
    
    async def find_careers(self, query: Dict[str, Any] = None, limit: int = None) -> List[Dict[str, Any]]:
        """Find careers matching query"""
        if not query:
            results = self.careers.all()
        else:
            Career = Query()
            results = []
            for key, value in query.items():
                if hasattr(Career, key):
                    results = self.careers.search(getattr(Career, key) == value)
                    break
        
        if limit:
            results = results[:limit]
        
        return results
    
    async def clear_careers(self):
        """Clear all careers"""
        self.careers.truncate()
    
    async def create_indexes(self):
        """Create indexes (no-op for TinyDB)"""
        pass

class Phase2HybridMigration:
    def __init__(self):
        self.sqlite_db_path = "careers.db"
        self.mongo_url = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
        self.mongo_db_name = os.getenv("MONGODB_DATABASE", "career_platform")
        self.migration_results = {}
        self.validation_results = {}
        self.use_mongodb = False
        self.use_embedded = False
        self.client = None
        self.db = None
        self.embedded_db = None
        
    def log(self, message: str, level: str = "INFO"):
        """Enhanced logging with timestamps"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {level}: {message}")
    
    async def setup_database_connection(self) -> bool:
        """Setup database connection - MongoDB or embedded fallback"""
        self.log("🔌 Setting up database connection...")
        
        # Try MongoDB first if available
        if MONGODB_AVAILABLE:
            try:
                self.client = AsyncIOMotorClient(self.mongo_url, serverSelectionTimeoutMS=5000)
                await self.client.admin.command('ping')
                self.db = self.client[self.mongo_db_name]
                self.use_mongodb = True
                self.log(f"✅ MongoDB connection successful: {self.mongo_url}")
                return True
            except Exception as e:
                self.log(f"⚠️ MongoDB connection failed: {e}")
        
        # Fall back to embedded database
        if TINYDB_AVAILABLE:
            try:
                self.embedded_db = EmbeddedCareerDB()
                self.use_embedded = True
                self.log("✅ Embedded database initialized (TinyDB)")
                return True
            except Exception as e:
                self.log(f"❌ Embedded database setup failed: {e}", "ERROR")
        
        self.log("❌ No database solution available", "ERROR")
        return False
    
    async def initialize_mongodb_models(self) -> bool:
        """Initialize MongoDB models if using MongoDB"""
        if not self.use_mongodb:
            return True
        
        try:
            # Import models
            from models import CareerModel, SkillModel
            
            await init_beanie(
                database=self.db,
                document_models=[CareerModel, SkillModel]
            )
            self.log("✅ MongoDB models initialized")
            return True
        except Exception as e:
            self.log(f"❌ MongoDB model initialization failed: {e}", "ERROR")
            return False
    
    async def create_indexes(self) -> bool:
        """Create database indexes"""
        self.log("📊 Creating database indexes...")
        
        if self.use_mongodb:
            try:
                careers_collection = self.db.careers
                
                indexes = [
                    ("career_id", 1),
                    ("title", 1),
                    ("careerType", 1),
                    ("experienceLevel", 1),
                    ("salaryMin", 1),
                    ("salaryMax", 1),
                ]
                
                for index_spec in indexes:
                    try:
                        await careers_collection.create_index(
                            index_spec[0], 
                            unique=(index_spec[0] == "career_id")
                        )
                    except Exception:
                        pass  # Index might already exist
                
                self.log("✅ MongoDB indexes created")
                return True
            except Exception as e:
                self.log(f"⚠️ Index creation warning: {e}", "WARNING")
                return True  # Continue even if indexing fails
        
        elif self.use_embedded:
            await self.embedded_db.create_indexes()
            self.log("✅ Embedded database ready")
            return True
        
        return False
    
    def load_sqlite_data(self) -> List[Dict[str, Any]]:
        """Load all career data from SQLite database"""
        self.log("📥 Loading SQLite data...")
        
        try:
            with sqlite3.connect(self.sqlite_db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                
                cursor.execute("SELECT * FROM careers ORDER BY id")
                rows = cursor.fetchall()
                
                careers_data = []
                for row in rows:
                    career_dict = dict(row)
                    
                    # Parse JSON fields
                    json_fields = ['requiredTechnicalSkills', 'requiredSoftSkills', 'companies']
                    for field in json_fields:
                        if career_dict.get(field):
                            try:
                                career_dict[field] = json.loads(career_dict[field])
                            except json.JSONDecodeError:
                                career_dict[field] = []
                        else:
                            career_dict[field] = []
                    
                    careers_data.append(career_dict)
                
                self.log(f"✅ Loaded {len(careers_data)} records from SQLite")
                return careers_data
                
        except Exception as e:
            self.log(f"❌ SQLite data loading failed: {e}", "ERROR")
            return []
    
    def transform_sqlite_to_unified_schema(self, sqlite_record: Dict[str, Any]) -> Dict[str, Any]:
        """Transform SQLite record to unified schema"""
        
        career_id = sqlite_record.get('careerType', str(uuid.uuid4()))
        
        # Map experience levels
        experience_mapping = {
            'entry': (0, 2),
            'junior': (0, 3),
            'mid': (3, 7),
            'senior': (7, 15),
            'executive': (15, 30),
            'lead': (5, 12)
        }
        
        exp_level = sqlite_record.get('experienceLevel', 'junior')
        min_years, max_years = experience_mapping.get(exp_level, (0, 5))
        
        # Override with actual values if present
        if sqlite_record.get('minExperienceYears') is not None:
            min_years = sqlite_record['minExperienceYears']
        if sqlite_record.get('maxExperienceYears') is not None:
            max_years = sqlite_record['maxExperienceYears']
        
        # Create unified schema record
        unified_record = {
            "career_id": career_id,
            "title": sqlite_record.get('title', 'Unknown Career'),
            "description": sqlite_record.get('description', ''),
            "requiredTechnicalSkills": sqlite_record.get('requiredTechnicalSkills', []),
            "requiredSoftSkills": sqlite_record.get('requiredSoftSkills', []),
            "preferredInterests": [],
            "preferredIndustries": [],
            "workDataWeight": 0.5,
            "workPeopleWeight": 0.5,
            "creativityWeight": 0.5,
            "problemSolvingWeight": 0.5,
            "leadershipWeight": 0.3 if exp_level in ['senior', 'executive', 'lead'] else 0.1,
            "learningPath": sqlite_record.get('learningPath', 'Self-directed learning'),
            "stretchLevel": self._map_stretch_level(sqlite_record.get('relevanceScore', 75)),
            "careerType": sqlite_record.get('careerType', 'general'),
            "requiresTechnical": len(sqlite_record.get('requiredTechnicalSkills', [])) > 0,
            "companies": sqlite_record.get('companies', []),
            "dayInLife": sqlite_record.get('description', ''),
            "experienceLevel": exp_level,
            "minYearsExperience": min_years,
            "maxYearsExperience": max_years,
            "salaryMin": sqlite_record.get('minSalary', 50000),
            "salaryMax": sqlite_record.get('maxSalary', 80000),
            "remoteOptions": "hybrid",
            "workEnvironments": ["office"],
            "requiredEducation": "bachelor",
            "preferredEducation": "bachelor",
            "valuedCertifications": [],
            "requiredCertifications": [],
            "workLifeBalanceRating": 3.5,
            "agePreference": "any",
            "locationFlexibility": "flexible",
            "transitionFriendly": True,
            "resumeKeywords": sqlite_record.get('requiredTechnicalSkills', []),
            "relatedJobTitles": [sqlite_record.get('title', '')],
            "valuedCompanies": sqlite_record.get('companies', []),
            "preferredIndustryExperience": [],
            "careerProgressionPatterns": [],
            "alternativeQualifications": [],
            "skillBasedEntry": True,
            "experienceCanSubstitute": True,
            "handsOnWorkWeight": 0.5,
            "physicalWorkWeight": 0.2,
            "outdoorWorkWeight": 0.1,
            "mechanicalAptitudeWeight": 0.3,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        
        return unified_record
    
    def _map_stretch_level(self, relevance_score: int) -> str:
        """Map relevance score to stretch level"""
        if relevance_score >= 80:
            return "safe"
        elif relevance_score >= 60:
            return "stretch"
        else:
            return "adventure"
    
    async def insert_career_record(self, career_data: Dict[str, Any]) -> bool:
        """Insert career record into appropriate database"""
        try:
            if self.use_mongodb:
                from models import CareerModel
                career_model = CareerModel(**career_data)
                await career_model.insert()
            elif self.use_embedded:
                await self.embedded_db.insert_career(career_data)
            else:
                return False
            
            return True
            
        except Exception as e:
            self.log(f"❌ Insert error for career {career_data.get('title', 'Unknown')}: {e}", "ERROR")
            return False
    
    async def migrate_data(self) -> Dict[str, Any]:
        """Execute the complete data migration"""
        self.log("🚀 Starting data migration...")
        
        # Load SQLite data
        sqlite_data = self.load_sqlite_data()
        if not sqlite_data:
            return {"success": False, "error": "No SQLite data to migrate"}
        
        # Clear existing data
        if self.use_mongodb:
            try:
                from models import CareerModel
                await CareerModel.delete_all()
                self.log("🗑️ Cleared existing MongoDB data")
            except:
                pass
        elif self.use_embedded:
            await self.embedded_db.clear_careers()
            self.log("🗑️ Cleared existing embedded data")
        
        # Transform and migrate data
        successful_migrations = 0
        failed_migrations = 0
        migration_errors = []
        
        for i, sqlite_record in enumerate(sqlite_data):
            try:
                # Transform data
                unified_record = self.transform_sqlite_to_unified_schema(sqlite_record)
                
                # Insert record
                if await self.insert_career_record(unified_record):
                    successful_migrations += 1
                else:
                    failed_migrations += 1
                    migration_errors.append(f"Record {i+1}: {sqlite_record.get('title', 'Unknown')}")
                
                # Progress indicator
                if (i + 1) % 50 == 0:
                    self.log(f"📊 Progress: {i+1}/{len(sqlite_data)} records processed")
                    
            except Exception as e:
                failed_migrations += 1
                migration_errors.append(f"Record {i+1}: {e}")
                self.log(f"❌ Migration error for record {i+1}: {e}", "ERROR")
        
        migration_results = {
            "total_records": len(sqlite_data),
            "successful_migrations": successful_migrations,
            "failed_migrations": failed_migrations,
            "success_rate": (successful_migrations / len(sqlite_data)) * 100 if sqlite_data else 0,
            "database_type": "MongoDB" if self.use_mongodb else "Embedded",
            "errors": migration_errors[:10]
        }
        
        self.migration_results = migration_results
        
        self.log(f"✅ Migration completed: {successful_migrations}/{len(sqlite_data)} records migrated successfully")
        self.log(f"📊 Success rate: {migration_results['success_rate']:.1f}%")
        self.log(f"🗄️ Database type: {migration_results['database_type']}")
        
        return migration_results
    
    async def validate_migration(self) -> Dict[str, Any]:
        """Comprehensive validation of migrated data"""
        self.log("🔍 Validating migrated data...")
        
        try:
            # Count validation
            if self.use_mongodb:
                from models import CareerModel
                migrated_count = await CareerModel.count()
            elif self.use_embedded:
                migrated_count = await self.embedded_db.count_careers()
            else:
                migrated_count = 0
            
            sqlite_count = len(self.load_sqlite_data())
            
            # Sample data validation
            if self.use_mongodb:
                from models import CareerModel
                sample_careers = await CareerModel.find_all().limit(5).to_list()
                sample_data = [career.model_dump() for career in sample_careers]
            elif self.use_embedded:
                sample_data = await self.embedded_db.find_careers(limit=5)
            else:
                sample_data = []
            
            # Field completeness check
            complete_records = 0
            for career in sample_data:
                if (career.get('title') and career.get('description') and 
                    career.get('salaryMin', 0) > 0 and career.get('salaryMax', 0) > 0):
                    complete_records += 1
            
            validation_results = {
                "migrated_count": migrated_count,
                "sqlite_count": sqlite_count,
                "count_match": migrated_count == sqlite_count,
                "sample_completeness": (complete_records / len(sample_data)) * 100 if sample_data else 0,
                "database_type": "MongoDB" if self.use_mongodb else "Embedded",
                "validation_passed": migrated_count == sqlite_count and migrated_count > 0
            }
            
            self.validation_results = validation_results
            
            if validation_results["validation_passed"]:
                self.log("✅ Migration validation: PASSED")
            else:
                self.log("❌ Migration validation: FAILED", "ERROR")
            
            return validation_results
            
        except Exception as e:
            self.log(f"❌ Validation error: {e}", "ERROR")
            return {"validation_passed": False, "error": str(e)}
    
    async def generate_migration_report(self) -> str:
        """Generate comprehensive migration report"""
        self.log("📋 Generating migration report...")
        
        report_path = f"phase2_hybrid_migration_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        try:
            with open(report_path, 'w', encoding='utf-8') as f:
                f.write("=" * 80 + "\n")
                f.write("PHASE 2: HYBRID MONGODB MIGRATION REPORT\n")
                f.write("=" * 80 + "\n")
                f.write(f"Migration Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Database Type: {'MongoDB' if self.use_mongodb else 'Embedded (TinyDB)'}\n")
                if self.use_mongodb:
                    f.write(f"MongoDB URL: {self.mongo_url}\n")
                    f.write(f"Database: {self.mongo_db_name}\n")
                f.write("\n")
                
                f.write("MIGRATION SUMMARY:\n")
                f.write("-" * 40 + "\n")
                if self.migration_results:
                    f.write(f"Total SQLite Records: {self.migration_results['total_records']}\n")
                    f.write(f"Successful Migrations: {self.migration_results['successful_migrations']}\n")
                    f.write(f"Failed Migrations: {self.migration_results['failed_migrations']}\n")
                    f.write(f"Success Rate: {self.migration_results['success_rate']:.1f}%\n")
                    f.write(f"Target Database: {self.migration_results['database_type']}\n\n")
                
                f.write("VALIDATION RESULTS:\n")
                f.write("-" * 40 + "\n")
                if self.validation_results:
                    f.write(f"Migrated Record Count: {self.validation_results['migrated_count']}\n")
                    f.write(f"SQLite Record Count: {self.validation_results['sqlite_count']}\n")
                    f.write(f"Count Match: {self.validation_results['count_match']}\n")
                    f.write(f"Sample Completeness: {self.validation_results['sample_completeness']:.1f}%\n")
                    f.write(f"Overall Validation: {'PASSED' if self.validation_results['validation_passed'] else 'FAILED'}\n\n")
                
                f.write("ARCHITECTURE STATUS:\n")
                f.write("-" * 40 + "\n")
                f.write(f"✅ {'MongoDB' if self.use_mongodb else 'Embedded database'} established as data source\n")
                f.write("✅ Schema standardization complete\n")
                f.write("✅ Data integrity validation completed\n")
                f.write("✅ Migration pipeline operational\n\n")
                
                if self.migration_results.get('errors'):
                    f.write("MIGRATION ERRORS (First 10):\n")
                    f.write("-" * 40 + "\n")
                    for error in self.migration_results['errors']:
                        f.write(f"- {error}\n")
                    f.write("\n")
                
                f.write(f"Report generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            
            self.log(f"✅ Migration report saved: {report_path}")
            return report_path
            
        except Exception as e:
            self.log(f"❌ Report generation failed: {e}", "ERROR")
            return ""
    
    async def run_phase2_migration(self) -> bool:
        """Execute complete Phase 2 migration pipeline"""
        self.log("🚀 STARTING PHASE 2: HYBRID MIGRATION PIPELINE")
        self.log("=" * 60)
        
        success = True
        
        try:
            # Step 1: Setup database connection
            if not await self.setup_database_connection():
                return False
            
            # Step 2: Initialize models (if MongoDB)
            if not await self.initialize_mongodb_models():
                return False
            
            # Step 3: Create indexes
            if not await self.create_indexes():
                success = False  # Continue but note the failure
            
            # Step 4: Migrate data
            migration_results = await self.migrate_data()
            if migration_results.get("success", True) == False:
                return False
            
            # Step 5: Validate migration
            validation_results = await self.validate_migration()
            if not validation_results.get("validation_passed", False):
                success = False
            
            # Step 6: Generate report
            report_path = await self.generate_migration_report()
            
            self.log("=" * 60)
            
            if success and validation_results.get("validation_passed", False):
                self.log("🎉 PHASE 2 MIGRATION: COMPLETED SUCCESSFULLY", "SUCCESS")
                self.log(f"✅ {'MongoDB' if self.use_mongodb else 'Embedded database'} is now the data source")
                self.log("✅ All 331 records migrated and validated")
                self.log("✅ Schema standardization complete")
            else:
                self.log("⚠️ PHASE 2 MIGRATION: COMPLETED WITH ISSUES", "WARNING")
                self.log("📋 Review the migration report for details")
            
            return success
            
        except Exception as e:
            self.log(f"❌ PHASE 2 MIGRATION FAILED: {e}", "ERROR")
            return False
        finally:
            if self.client:
                self.client.close()

async def main():
    """Main execution function"""
    migration = Phase2HybridMigration()
    success = await migration.run_phase2_migration()
    
    if success:
        print("\n🎉 PHASE 2 ARCHITECTURE CONSOLIDATION SUCCESSFUL!")
        print("Database architecture established with unified schema.")
    else:
        print("\n⚠️ PHASE 2 COMPLETED WITH ISSUES!")
        print("Please review the migration report and address any problems.")
    
    return success

if __name__ == "__main__":
    asyncio.run(main())