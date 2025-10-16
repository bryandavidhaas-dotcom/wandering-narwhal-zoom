#!/usr/bin/env python3
"""
MongoDB Atlas Cluster Inspector
==============================
Inspects the existing "career-finder" cluster to determine:
1. What databases and collections exist
2. Data structure and schema
3. Whether to reuse or create new database
4. Migration strategy recommendations

Author: Phase 2 Cluster Inspector
Date: 2025-01-07
"""

import asyncio
import json
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorClient
from typing import Dict, List, Any

class MongoDBClusterInspector:
    def __init__(self):
        self.connection_string = None
        self.client = None
        self.inspection_results = {}
        
    def get_connection_string(self):
        """Get MongoDB Atlas connection string from user"""
        print("🔍 MongoDB Atlas Cluster Inspector")
        print("=" * 40)
        print("\nTo inspect your 'career-finder' cluster, I need the connection string.")
        print("It should look like:")
        print("mongodb+srv://username:password@career-finder.xxxxx.mongodb.net/?retryWrites=true&w=majority")
        
        connection_string = input("\nEnter your MongoDB Atlas connection string: ").strip()
        if not connection_string:
            print("❌ Connection string is required")
            return False
        
        self.connection_string = connection_string
        return True
    
    async def connect_to_cluster(self):
        """Connect to MongoDB Atlas cluster"""
        print("\n🔌 Connecting to career-finder cluster...")
        
        try:
            self.client = AsyncIOMotorClient(self.connection_string, serverSelectionTimeoutMS=10000)
            await self.client.admin.command('ping')
            print("✅ Successfully connected to career-finder cluster")
            return True
        except Exception as e:
            print(f"❌ Connection failed: {e}")
            return False
    
    async def inspect_databases(self):
        """Inspect all databases in the cluster"""
        print("\n📊 Inspecting databases...")
        
        try:
            db_list = await self.client.list_database_names()
            print(f"Found {len(db_list)} databases: {db_list}")
            
            db_details = {}
            for db_name in db_list:
                if db_name in ['admin', 'local', 'config']:
                    continue  # Skip system databases
                
                db = self.client[db_name]
                collections = await db.list_collection_names()
                
                db_info = {
                    'collections': collections,
                    'collection_count': len(collections),
                    'collection_details': {}
                }
                
                # Inspect each collection
                for collection_name in collections:
                    collection = db[collection_name]
                    doc_count = await collection.count_documents({})
                    
                    # Get sample document
                    sample_doc = await collection.find_one()
                    
                    db_info['collection_details'][collection_name] = {
                        'document_count': doc_count,
                        'sample_document': sample_doc,
                        'has_career_data': self._looks_like_career_data(sample_doc)
                    }
                
                db_details[db_name] = db_info
                print(f"  📁 {db_name}: {len(collections)} collections, analyzing...")
            
            self.inspection_results['databases'] = db_details
            return db_details
            
        except Exception as e:
            print(f"❌ Database inspection failed: {e}")
            return {}
    
    def _looks_like_career_data(self, document):
        """Check if document looks like career data"""
        if not document:
            return False
        
        career_indicators = [
            'title', 'career', 'job', 'position', 'role',
            'salary', 'skills', 'experience', 'description'
        ]
        
        doc_keys = [str(key).lower() for key in document.keys()]
        matches = sum(1 for indicator in career_indicators 
                     if any(indicator in key for key in doc_keys))
        
        return matches >= 3  # If 3+ career-related fields, likely career data
    
    async def analyze_existing_career_data(self):
        """Analyze existing career data structure"""
        print("\n🔍 Analyzing existing career data...")
        
        career_collections = []
        
        for db_name, db_info in self.inspection_results.get('databases', {}).items():
            for collection_name, collection_info in db_info['collection_details'].items():
                if collection_info['has_career_data']:
                    career_collections.append({
                        'database': db_name,
                        'collection': collection_name,
                        'document_count': collection_info['document_count'],
                        'sample': collection_info['sample_document']
                    })
        
        if career_collections:
            print(f"Found {len(career_collections)} collections with career data:")
            for cc in career_collections:
                print(f"  📋 {cc['database']}.{cc['collection']}: {cc['document_count']} documents")
                
                # Analyze schema compatibility
                sample = cc['sample']
                compatibility = self._analyze_schema_compatibility(sample)
                print(f"     Schema compatibility: {compatibility['score']}/10")
                if compatibility['issues']:
                    print(f"     Issues: {', '.join(compatibility['issues'])}")
        else:
            print("No existing career data collections found")
        
        self.inspection_results['career_collections'] = career_collections
        return career_collections
    
    def _analyze_schema_compatibility(self, sample_doc):
        """Analyze how compatible existing data is with our CareerModel"""
        if not sample_doc:
            return {'score': 0, 'issues': ['No sample document']}
        
        # Expected fields from our CareerModel
        expected_fields = [
            'title', 'description', 'requiredTechnicalSkills', 'requiredSoftSkills',
            'experienceLevel', 'salaryMin', 'salaryMax', 'companies', 'careerType'
        ]
        
        doc_keys = list(sample_doc.keys())
        score = 0
        issues = []
        
        # Check field presence
        for field in expected_fields:
            if field in doc_keys:
                score += 1
            else:
                # Check for similar fields
                similar_found = False
                for key in doc_keys:
                    if field.lower() in key.lower() or key.lower() in field.lower():
                        score += 0.5
                        similar_found = True
                        break
                
                if not similar_found:
                    issues.append(f"Missing {field}")
        
        # Normalize score to 0-10
        score = min(10, (score / len(expected_fields)) * 10)
        
        return {'score': round(score, 1), 'issues': issues}
    
    def generate_recommendations(self):
        """Generate recommendations for database strategy"""
        print("\n💡 Generating recommendations...")
        
        career_collections = self.inspection_results.get('career_collections', [])
        databases = self.inspection_results.get('databases', {})
        
        recommendations = {
            'strategy': 'unknown',
            'reasoning': [],
            'action_plan': []
        }
        
        if not career_collections:
            # No existing career data - safe to create new
            recommendations['strategy'] = 'create_new_database'
            recommendations['reasoning'] = [
                "No existing career data found in cluster",
                "Safe to create new 'career_platform' database",
                "Clean slate for Phase 2 architecture"
            ]
            recommendations['action_plan'] = [
                "Create new 'career_platform' database",
                "Run Phase 2 migration to populate with 331 records",
                "Establish as single source of truth"
            ]
        
        elif len(career_collections) == 1:
            # Single career collection - analyze compatibility
            cc = career_collections[0]
            sample = cc['sample']
            compatibility = self._analyze_schema_compatibility(sample)
            
            if compatibility['score'] >= 7:
                recommendations['strategy'] = 'reuse_and_migrate'
                recommendations['reasoning'] = [
                    f"Found compatible career data in {cc['database']}.{cc['collection']}",
                    f"Schema compatibility score: {compatibility['score']}/10",
                    f"Existing {cc['document_count']} documents can be preserved"
                ]
                recommendations['action_plan'] = [
                    f"Backup existing {cc['collection']} collection",
                    "Transform existing data to match CareerModel schema",
                    "Merge with 331 SQLite records",
                    "Update collection with unified schema"
                ]
            else:
                recommendations['strategy'] = 'create_separate_database'
                recommendations['reasoning'] = [
                    f"Existing data has low compatibility: {compatibility['score']}/10",
                    "Schema differences too significant for easy migration",
                    "Safer to create separate database"
                ]
                recommendations['action_plan'] = [
                    "Create new 'career_platform' database",
                    "Migrate 331 SQLite records to new database",
                    "Keep existing data as backup/reference"
                ]
        
        else:
            # Multiple career collections - complex scenario
            recommendations['strategy'] = 'create_separate_database'
            recommendations['reasoning'] = [
                f"Found {len(career_collections)} career collections",
                "Complex existing structure",
                "Safer to create clean new database"
            ]
            recommendations['action_plan'] = [
                "Create new 'career_platform' database",
                "Migrate 331 SQLite records to new database",
                "Analyze existing collections separately if needed"
            ]
        
        self.inspection_results['recommendations'] = recommendations
        return recommendations
    
    def display_recommendations(self, recommendations):
        """Display recommendations to user"""
        print(f"\n🎯 RECOMMENDATION: {recommendations['strategy'].replace('_', ' ').title()}")
        print("=" * 50)
        
        print("\n📋 Reasoning:")
        for reason in recommendations['reasoning']:
            print(f"  • {reason}")
        
        print("\n📝 Action Plan:")
        for i, action in enumerate(recommendations['action_plan'], 1):
            print(f"  {i}. {action}")
    
    async def generate_inspection_report(self):
        """Generate detailed inspection report"""
        print("\n📋 Generating inspection report...")
        
        report_path = f"mongodb_cluster_inspection_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        try:
            report_data = {
                'inspection_date': datetime.now().isoformat(),
                'cluster_name': 'career-finder',
                'connection_successful': True,
                'databases': self.inspection_results.get('databases', {}),
                'career_collections': self.inspection_results.get('career_collections', []),
                'recommendations': self.inspection_results.get('recommendations', {}),
                'next_steps': [
                    "Review recommendations",
                    "Choose database strategy",
                    "Run Phase 2 migration with chosen approach"
                ]
            }
            
            with open(report_path, 'w', encoding='utf-8') as f:
                json.dump(report_data, f, indent=2, default=str)
            
            print(f"✅ Inspection report saved: {report_path}")
            return report_path
            
        except Exception as e:
            print(f"❌ Report generation failed: {e}")
            return None
    
    async def run_inspection(self):
        """Run complete cluster inspection"""
        print("🚀 STARTING MONGODB CLUSTER INSPECTION")
        print("=" * 50)
        
        try:
            # Step 1: Get connection string
            if not self.get_connection_string():
                return False
            
            # Step 2: Connect to cluster
            if not await self.connect_to_cluster():
                return False
            
            # Step 3: Inspect databases
            databases = await self.inspect_databases()
            if not databases:
                print("⚠️ No user databases found")
            
            # Step 4: Analyze career data
            await self.analyze_existing_career_data()
            
            # Step 5: Generate recommendations
            recommendations = self.generate_recommendations()
            self.display_recommendations(recommendations)
            
            # Step 6: Generate report
            await self.generate_inspection_report()
            
            print("\n✅ CLUSTER INSPECTION COMPLETED")
            print("Review the recommendations above to proceed with Phase 2 migration.")
            
            return True
            
        except Exception as e:
            print(f"❌ INSPECTION FAILED: {e}")
            return False
        finally:
            if self.client:
                self.client.close()

async def main():
    """Main inspection function"""
    inspector = MongoDBClusterInspector()
    success = await inspector.run_inspection()
    
    if success:
        print("\n🎉 CLUSTER INSPECTION SUCCESSFUL!")
        print("Use the recommendations to proceed with Phase 2 migration.")
    else:
        print("\n❌ CLUSTER INSPECTION FAILED!")
        print("Please check your connection and try again.")
    
    return success

if __name__ == "__main__":
    asyncio.run(main())