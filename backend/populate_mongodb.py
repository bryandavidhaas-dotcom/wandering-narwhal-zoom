#!/usr/bin/env python3
"""
Script to populate MongoDB with comprehensive career data.
This script converts the comprehensive career data to MongoDB format and populates the database.
"""

import asyncio
import os
import sys
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from datetime import datetime
import uuid

# Add the backend directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models import CareerModel, SkillModel
from comprehensive_careers import COMPREHENSIVE_CAREERS

# Load environment variables
load_dotenv()

async def init_database():
    """Initialize database connection"""
    mongo_url = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
    db_name = os.getenv("MONGODB_DATABASE", "career_platform")
    
    print(f"Connecting to MongoDB: {mongo_url}")
    print(f"Database: {db_name}")
    
    client = AsyncIOMotorClient(mongo_url)
    
    await init_beanie(
        database=client[db_name],
        document_models=[CareerModel, SkillModel]
    )
    
    print("✅ Connected to MongoDB successfully")
    return client[db_name]

def convert_career_to_mongodb_format(career_data):
    """Convert comprehensive career data to MongoDB CareerModel format"""
    
    # Extract salary range
    salary_range = career_data.get("salaryRange", "$50,000 - $80,000")
    min_salary = career_data.get("minSalary", 50000)
    max_salary = career_data.get("maxSalary", 80000)
    
    # Map experience levels
    experience_level = career_data.get("experienceLevel", "junior")
    min_years = career_data.get("minExperienceYears", 0)
    max_years = career_data.get("maxExperienceYears", 5)
    
    # Create MongoDB-compatible career document
    mongodb_career = {
        "career_id": career_data.get("careerType", str(uuid.uuid4())),
        "title": career_data.get("title", "Unknown Career"),
        "description": career_data.get("description", ""),
        "requiredTechnicalSkills": career_data.get("requiredTechnicalSkills", []),
        "requiredSoftSkills": career_data.get("requiredSoftSkills", []),
        "preferredInterests": [],
        "preferredIndustries": [],
        "workDataWeight": 0.5,
        "workPeopleWeight": 0.5,
        "creativityWeight": 0.5,
        "problemSolvingWeight": 0.5,
        "leadershipWeight": 0.5,
        "learningPath": career_data.get("learningPath", "Self-directed learning"),
        "stretchLevel": career_data.get("zone", "safe"),
        "careerType": career_data.get("careerType", "general"),
        "requiresTechnical": len(career_data.get("requiredTechnicalSkills", [])) > 0,
        "companies": career_data.get("companies", []),
        "dayInLife": career_data.get("description", ""),
        "experienceLevel": experience_level,
        "minYearsExperience": min_years,
        "maxYearsExperience": max_years,
        "salaryMin": min_salary,
        "salaryMax": max_salary,
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
        "resumeKeywords": career_data.get("requiredTechnicalSkills", []),
        "relatedJobTitles": [career_data.get("title", "")],
        "valuedCompanies": career_data.get("companies", []),
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
    
    return mongodb_career

async def populate_skills():
    """Populate skills collection"""
    print("🔧 Populating skills...")
    
    # Extract unique skills from all careers
    all_skills = set()
    for career in COMPREHENSIVE_CAREERS:
        all_skills.update(career.get("requiredTechnicalSkills", []))
        all_skills.update(career.get("requiredSoftSkills", []))
    
    # Check if skills already exist
    existing_count = await SkillModel.count()
    if existing_count > 0:
        print(f"⚠️ Skills collection already has {existing_count} documents. Skipping...")
        return
    
    skills_to_insert = []
    for skill_name in all_skills:
        if skill_name:  # Skip empty strings
            skill_doc = SkillModel(
                skill_id=skill_name.lower().replace(" ", "_").replace("/", "_"),
                name=skill_name,
                category="general",
                related_skills=[],
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            skills_to_insert.append(skill_doc)
    
    if skills_to_insert:
        await SkillModel.insert_many(skills_to_insert)
        print(f"✅ Inserted {len(skills_to_insert)} skills")
    else:
        print("⚠️ No skills to insert")

async def populate_careers():
    """Populate careers collection"""
    print("🚀 Populating careers...")
    
    # Check if careers already exist
    existing_count = await CareerModel.count()
    if existing_count > 0:
        print(f"⚠️ Careers collection already has {existing_count} documents. Skipping...")
        return
    
    careers_to_insert = []
    for career_data in COMPREHENSIVE_CAREERS:
        try:
            mongodb_career_data = convert_career_to_mongodb_format(career_data)
            career_doc = CareerModel(**mongodb_career_data)
            careers_to_insert.append(career_doc)
        except Exception as e:
            print(f"❌ Error converting career {career_data.get('title', 'Unknown')}: {e}")
            continue
    
    if careers_to_insert:
        await CareerModel.insert_many(careers_to_insert)
        print(f"✅ Inserted {len(careers_to_insert)} careers")
    else:
        print("⚠️ No careers to insert")

async def verify_data():
    """Verify the populated data"""
    print("🔍 Verifying populated data...")
    
    skill_count = await SkillModel.count()
    career_count = await CareerModel.count()
    
    print(f"📊 Database Statistics:")
    print(f"   Skills: {skill_count}")
    print(f"   Careers: {career_count}")
    
    # Show sample careers
    sample_careers = await CareerModel.find_all().limit(3).to_list()
    print(f"\n📋 Sample careers:")
    for career in sample_careers:
        print(f"   - {career.title} ({career.experienceLevel}): ${career.salaryMin:,} - ${career.salaryMax:,}")

async def main():
    """Main function to populate MongoDB"""
    print("🚀 Starting MongoDB population...")
    
    try:
        # Initialize database
        db = await init_database()
        
        # Populate collections
        await populate_skills()
        await populate_careers()
        
        # Verify data
        await verify_data()
        
        print("\n✅ MongoDB population completed successfully!")
        
    except Exception as e:
        print(f"❌ Error during population: {e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())