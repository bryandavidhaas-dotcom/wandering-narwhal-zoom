"""
Career database schema and management for the recommendation engine.

This module provides the database schema and management functions for storing
career data centrally, replacing the hardcoded career templates in the frontend.
"""

from typing import List, Dict, Optional, Any
from dataclasses import dataclass, field
from enum import Enum
import json
import sqlite3
from pathlib import Path


class ExperienceLevel(Enum):
    """Experience level enumeration."""
    ENTRY = "entry"
    JUNIOR = "junior"
    MID = "mid"
    SENIOR = "senior"
    EXECUTIVE = "executive"


class CareerField(Enum):
    """Career field enumeration."""
    TECHNOLOGY = "technology"
    BUSINESS_FINANCE = "business_finance"
    EXECUTIVE_LEADERSHIP = "executive_leadership"
    SALES_MARKETING = "sales_marketing"
    HEALTHCARE = "healthcare"
    EDUCATION = "education"
    SKILLED_TRADES = "skilled_trades"
    GOVERNMENT_PUBLIC_SERVICE = "government_public_service"
    LEGAL_LAW = "legal_law"
    CREATIVE_ARTS = "creative_arts"
    HOSPITALITY_SERVICE = "hospitality_service"
    AGRICULTURE_ENVIRONMENT = "agriculture_environment"
    MANUFACTURING_INDUSTRIAL = "manufacturing_industrial"
    OTHER = "other"


@dataclass
class CareerData:
    """
    Comprehensive career data structure.
    
    This replaces the hardcoded CareerTemplate from the frontend.
    """
    # Basic Information
    career_id: str
    title: str
    description: str
    career_field: CareerField
    experience_level: ExperienceLevel
    
    # Salary Information
    salary_min: int
    salary_max: int
    salary_currency: str = "USD"
    
    # Skills and Requirements
    required_technical_skills: List[str] = field(default_factory=list)
    required_soft_skills: List[str] = field(default_factory=list)
    preferred_skills: List[str] = field(default_factory=list)
    required_certifications: List[str] = field(default_factory=list)
    valued_certifications: List[str] = field(default_factory=list)
    
    # Education Requirements
    required_education: str = "high-school"  # high-school, associates, bachelors, masters, doctorate
    preferred_education: str = "bachelors"
    alternative_qualifications: List[str] = field(default_factory=list)
    
    # Experience Requirements
    min_years_experience: int = 0
    max_years_experience: int = 50
    experience_can_substitute: bool = True
    skill_based_entry: bool = True
    
    # Work Preferences and Environment
    work_data_weight: int = 3  # 1-5 scale
    work_people_weight: int = 3
    creativity_weight: int = 3
    problem_solving_weight: int = 3
    leadership_weight: int = 3
    hands_on_work_weight: int = 3
    physical_work_weight: int = 3
    outdoor_work_weight: int = 3
    mechanical_aptitude_weight: int = 3
    
    # Industry and Company Information
    preferred_industries: List[str] = field(default_factory=list)
    preferred_interests: List[str] = field(default_factory=list)
    companies: List[str] = field(default_factory=list)
    valued_companies: List[str] = field(default_factory=list)
    
    # Work Environment
    work_environments: List[str] = field(default_factory=lambda: ["office"])
    remote_options: str = "Available"
    location_flexibility: str = "flexible"
    
    # Career Development
    learning_path: str = ""
    career_progression_patterns: List[str] = field(default_factory=list)
    related_job_titles: List[str] = field(default_factory=list)
    
    # Additional Metadata
    transition_friendly: bool = True
    work_life_balance_rating: int = 3  # 1-5 scale
    age_preference: str = "25-45"
    day_in_life: str = ""
    resume_keywords: List[str] = field(default_factory=list)
    
    # Market Information
    demand_level: str = "medium"  # low, medium, high, very_high
    growth_outlook: str = "stable"  # declining, stable, growing, high_growth
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for database storage."""
        data = {}
        for key, value in self.__dict__.items():
            if isinstance(value, Enum):
                data[key] = value.value
            elif isinstance(value, list):
                data[key] = json.dumps(value)
            else:
                data[key] = value
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'CareerData':
        """Create from dictionary loaded from database."""
        # Remove database-only fields that aren't in the dataclass
        db_only_fields = ['created_at', 'updated_at']
        for field in db_only_fields:
            data.pop(field, None)
        
        # Convert enum fields
        if 'career_field' in data:
            data['career_field'] = CareerField(data['career_field'])
        if 'experience_level' in data:
            data['experience_level'] = ExperienceLevel(data['experience_level'])
        
        # Convert JSON list fields
        list_fields = [
            'required_technical_skills', 'required_soft_skills', 'preferred_skills',
            'required_certifications', 'valued_certifications', 'alternative_qualifications',
            'preferred_industries', 'preferred_interests', 'companies', 'valued_companies',
            'work_environments', 'career_progression_patterns', 'related_job_titles',
            'resume_keywords'
        ]
        
        for field_name in list_fields:
            if field_name in data and isinstance(data[field_name], str):
                try:
                    data[field_name] = json.loads(data[field_name])
                except json.JSONDecodeError:
                    data[field_name] = []
        
        return cls(**data)


import re


def normalize_career_title(title: str) -> str:
    """
    Normalize the career title for consistent storage and lookup.
    
    - Converts to lowercase
    - Removes common prepositions
    - Replaces spaces and special characters with hyphens
    - Removes duplicate hyphens
    """
    # Lowercase
    title = title.lower()
    
    # Remove prepositions
    prepositions = ["of", "and", "the"]
    title = ' '.join([word for word in title.split() if word not in prepositions])
    
    # Replace spaces and special characters with hyphens
    title = re.sub(r'[^a-z0-9]+', '-', title)
    
    # Remove leading/trailing hyphens
    title = title.strip('-')
    
    # Remove duplicate hyphens
    title = re.sub(r'-+', '-', title)
    
    return title


class CareerDatabase:
    """
    Career database management class.
    
    Provides methods to store, retrieve, and manage career data.
    """
    
    def __init__(self, db_path: str = "careers.db"):
        """
        Initialize the career database.
        
        Args:
            db_path: Path to the SQLite database file
        """
        self.db_path = db_path
        self._init_database()
    
    def _init_database(self):
        """Initialize the database schema."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS careers (
                    career_id TEXT PRIMARY KEY,
                    title TEXT NOT NULL,
                    description TEXT NOT NULL,
                    career_field TEXT NOT NULL,
                    experience_level TEXT NOT NULL,
                    salary_min INTEGER NOT NULL,
                    salary_max INTEGER NOT NULL,
                    salary_currency TEXT DEFAULT 'USD',
                    required_technical_skills TEXT DEFAULT '[]',
                    required_soft_skills TEXT DEFAULT '[]',
                    preferred_skills TEXT DEFAULT '[]',
                    required_certifications TEXT DEFAULT '[]',
                    valued_certifications TEXT DEFAULT '[]',
                    required_education TEXT DEFAULT 'high-school',
                    preferred_education TEXT DEFAULT 'bachelors',
                    alternative_qualifications TEXT DEFAULT '[]',
                    min_years_experience INTEGER DEFAULT 0,
                    max_years_experience INTEGER DEFAULT 50,
                    experience_can_substitute BOOLEAN DEFAULT 1,
                    skill_based_entry BOOLEAN DEFAULT 1,
                    work_data_weight INTEGER DEFAULT 3,
                    work_people_weight INTEGER DEFAULT 3,
                    creativity_weight INTEGER DEFAULT 3,
                    problem_solving_weight INTEGER DEFAULT 3,
                    leadership_weight INTEGER DEFAULT 3,
                    hands_on_work_weight INTEGER DEFAULT 3,
                    physical_work_weight INTEGER DEFAULT 3,
                    outdoor_work_weight INTEGER DEFAULT 3,
                    mechanical_aptitude_weight INTEGER DEFAULT 3,
                    preferred_industries TEXT DEFAULT '[]',
                    preferred_interests TEXT DEFAULT '[]',
                    companies TEXT DEFAULT '[]',
                    valued_companies TEXT DEFAULT '[]',
                    work_environments TEXT DEFAULT '["office"]',
                    remote_options TEXT DEFAULT 'Available',
                    location_flexibility TEXT DEFAULT 'flexible',
                    learning_path TEXT DEFAULT '',
                    career_progression_patterns TEXT DEFAULT '[]',
                    related_job_titles TEXT DEFAULT '[]',
                    transition_friendly BOOLEAN DEFAULT 1,
                    work_life_balance_rating INTEGER DEFAULT 3,
                    age_preference TEXT DEFAULT '25-45',
                    day_in_life TEXT DEFAULT '',
                    resume_keywords TEXT DEFAULT '[]',
                    demand_level TEXT DEFAULT 'medium',
                    growth_outlook TEXT DEFAULT 'stable',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Create indexes for common queries
            conn.execute("CREATE INDEX IF NOT EXISTS idx_career_field ON careers(career_field)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_experience_level ON careers(experience_level)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_salary_range ON careers(salary_min, salary_max)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_title ON careers(title)")
    
    def add_career(self, career: CareerData) -> bool:
        """
        Add a career to the database.
        
        Args:
            career: CareerData object to add
            
        Returns:
            True if successful, False otherwise
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                data = career.to_dict()
                columns = ', '.join(data.keys())
                placeholders = ', '.join(['?' for _ in data])
                
                conn.execute(
                    f"INSERT OR REPLACE INTO careers ({columns}) VALUES ({placeholders})",
                    list(data.values())
                )
                return True
        except Exception as e:
            print(f"Error adding career: {e}")
            return False
    
    def get_career(self, career_id: str) -> Optional[CareerData]:
        """
        Get a career by ID.
        
        Args:
            career_id: Career ID to retrieve
            
        Returns:
            CareerData object if found, None otherwise
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.execute("SELECT * FROM careers WHERE career_id = ?", (career_id,))
                row = cursor.fetchone()
                
                if row:
                    return CareerData.from_dict(dict(row))
                return None
        except Exception as e:
            print(f"Error getting career: {e}")
            return None
    
    def get_careers_by_field(self, career_field: CareerField) -> List[CareerData]:
        """
        Get all careers in a specific field.
        
        Args:
            career_field: Career field to filter by
            
        Returns:
            List of CareerData objects
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.execute(
                    "SELECT * FROM careers WHERE career_field = ?", 
                    (career_field.value,)
                )
                
                careers = []
                for row in cursor.fetchall():
                    careers.append(CareerData.from_dict(dict(row)))
                return careers
        except Exception as e:
            print(f"Error getting careers by field: {e}")
            return []
    
    def get_careers_by_experience_level(self, experience_level: ExperienceLevel) -> List[CareerData]:
        """
        Get all careers for a specific experience level.
        
        Args:
            experience_level: Experience level to filter by
            
        Returns:
            List of CareerData objects
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.execute(
                    "SELECT * FROM careers WHERE experience_level = ?", 
                    (experience_level.value,)
                )
                
                careers = []
                for row in cursor.fetchall():
                    careers.append(CareerData.from_dict(dict(row)))
                return careers
        except Exception as e:
            print(f"Error getting careers by experience level: {e}")
            return []
    
    def search_careers(
        self, 
        title_query: Optional[str] = None,
        career_fields: Optional[List[CareerField]] = None,
        experience_levels: Optional[List[ExperienceLevel]] = None,
        salary_min: Optional[int] = None,
        salary_max: Optional[int] = None,
        limit: int = 100
    ) -> List[CareerData]:
        """
        Search careers with multiple filters.
        
        Args:
            title_query: Search term for career title
            career_fields: List of career fields to include
            experience_levels: List of experience levels to include
            salary_min: Minimum salary requirement
            salary_max: Maximum salary requirement
            limit: Maximum number of results
            
        Returns:
            List of matching CareerData objects
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                
                query = "SELECT * FROM careers WHERE 1=1"
                params = []
                
                if title_query:
                    query += " AND title LIKE ?"
                    params.append(f"%{title_query}%")
                
                if career_fields:
                    field_placeholders = ','.join(['?' for _ in career_fields])
                    query += f" AND career_field IN ({field_placeholders})"
                    params.extend([field.value for field in career_fields])
                
                if experience_levels:
                    level_placeholders = ','.join(['?' for _ in experience_levels])
                    query += f" AND experience_level IN ({level_placeholders})"
                    params.extend([level.value for level in experience_levels])
                
                if salary_min is not None:
                    query += " AND salary_max >= ?"
                    params.append(salary_min)
                
                if salary_max is not None:
                    query += " AND salary_min <= ?"
                    params.append(salary_max)
                
                query += f" ORDER BY title LIMIT ?"
                params.append(limit)
                
                cursor = conn.execute(query, params)
                
                careers = []
                for row in cursor.fetchall():
                    careers.append(CareerData.from_dict(dict(row)))
                return careers
        except Exception as e:
            print(f"Error searching careers: {e}")
            return []
    
    def get_all_careers(self, limit: Optional[int] = None) -> List[CareerData]:
        """
        Get all careers from the database.
        
        Args:
            limit: Optional limit on number of results
            
        Returns:
            List of all CareerData objects
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                
                query = "SELECT * FROM careers ORDER BY title"
                if limit:
                    query += f" LIMIT {limit}"
                
                cursor = conn.execute(query)
                
                careers = []
                for row in cursor.fetchall():
                    careers.append(CareerData.from_dict(dict(row)))
                return careers
        except Exception as e:
            print(f"Error getting all careers: {e}")
            return []
    
    def update_career(self, career: CareerData) -> bool:
        """
        Update an existing career.
        
        Args:
            career: Updated CareerData object
            
        Returns:
            True if successful, False otherwise
        """
        return self.add_career(career)  # INSERT OR REPLACE handles updates
    
    def delete_career(self, career_id: str) -> bool:
        """
        Delete a career from the database.
        
        Args:
            career_id: Career ID to delete
            
        Returns:
            True if successful, False otherwise
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute("DELETE FROM careers WHERE career_id = ?", (career_id,))
                return cursor.rowcount > 0
        except Exception as e:
            print(f"Error deleting career: {e}")
            return False
    
    def get_career_statistics(self) -> Dict[str, Any]:
        """
        Get statistics about the career database.
        
        Returns:
            Dictionary with database statistics
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                # Total careers
                total_careers = conn.execute("SELECT COUNT(*) FROM careers").fetchone()[0]
                
                # Careers by field
                field_counts = {}
                cursor = conn.execute("SELECT career_field, COUNT(*) FROM careers GROUP BY career_field")
                for field, count in cursor.fetchall():
                    field_counts[field] = count
                
                # Careers by experience level
                level_counts = {}
                cursor = conn.execute("SELECT experience_level, COUNT(*) FROM careers GROUP BY experience_level")
                for level, count in cursor.fetchall():
                    level_counts[level] = count
                
                # Salary statistics
                salary_stats = conn.execute("""
                    SELECT 
                        AVG(salary_min) as avg_min_salary,
                        AVG(salary_max) as avg_max_salary,
                        MIN(salary_min) as min_salary,
                        MAX(salary_max) as max_salary
                    FROM careers
                """).fetchone()
                
                return {
                    "total_careers": total_careers,
                    "careers_by_field": field_counts,
                    "careers_by_experience_level": level_counts,
                    "salary_statistics": {
                        "average_min_salary": salary_stats[0],
                        "average_max_salary": salary_stats[1],
                        "lowest_salary": salary_stats[2],
                        "highest_salary": salary_stats[3]
                    }
                }
        except Exception as e:
            print(f"Error getting statistics: {e}")
            return {}


def migrate_frontend_careers_to_database(db: CareerDatabase, frontend_careers: List[Dict]) -> int:
    """
    Migrate career data from frontend hardcoded templates to database.
    
    Args:
        db: CareerDatabase instance
        frontend_careers: List of career dictionaries from frontend
        
    Returns:
        Number of careers successfully migrated
    """
    migrated_count = 0
    
    for i, career_dict in enumerate(frontend_careers):
        try:
            # Generate career ID if not present
            career_id = career_dict.get('careerType', f'career_{i:04d}')
            
            # Map frontend fields to database fields
            career_data = CareerData(
                career_id=career_id,
                title=normalize_career_title(career_dict.get('title', 'Unknown Career')),
                description=career_dict.get('description', ''),
                career_field=CareerField.OTHER,  # Will be determined by enhanced categorization
                experience_level=ExperienceLevel(career_dict.get('experienceLevel', 'mid')),
                salary_min=career_dict.get('salaryMin', 50000),
                salary_max=career_dict.get('salaryMax', 100000),
                required_technical_skills=career_dict.get('requiredTechnicalSkills', []),
                required_soft_skills=career_dict.get('requiredSoftSkills', []),
                preferred_skills=career_dict.get('preferredSkills', []),
                required_certifications=career_dict.get('requiredCertifications', []),
                valued_certifications=career_dict.get('valuedCertifications', []),
                required_education=career_dict.get('requiredEducation', 'high-school'),
                preferred_education=career_dict.get('preferredEducation', 'bachelors'),
                min_years_experience=career_dict.get('minYearsExperience', 0),
                max_years_experience=career_dict.get('maxYearsExperience', 50),
                work_data_weight=career_dict.get('workDataWeight', 3),
                work_people_weight=career_dict.get('workPeopleWeight', 3),
                creativity_weight=career_dict.get('creativityWeight', 3),
                problem_solving_weight=career_dict.get('problemSolvingWeight', 3),
                leadership_weight=career_dict.get('leadershipWeight', 3),
                hands_on_work_weight=career_dict.get('handsOnWorkWeight', 3),
                physical_work_weight=career_dict.get('physicalWorkWeight', 3),
                outdoor_work_weight=career_dict.get('outdoorWorkWeight', 3),
                mechanical_aptitude_weight=career_dict.get('mechanicalAptitudeWeight', 3),
                preferred_industries=career_dict.get('preferredIndustries', []),
                preferred_interests=career_dict.get('preferredInterests', []),
                companies=career_dict.get('companies', []),
                work_environments=career_dict.get('workEnvironments', ['office']),
                remote_options=career_dict.get('remoteOptions', 'Available'),
                learning_path=career_dict.get('learningPath', ''),
                transition_friendly=career_dict.get('transitionFriendly', True),
                day_in_life=career_dict.get('dayInLife', ''),
                resume_keywords=career_dict.get('resumeKeywords', [])
            )
            
            if db.add_career(career_data):
                migrated_count += 1
                
        except Exception as e:
            print(f"Error migrating career {i}: {e}")
            continue
    
    return migrated_count


if __name__ == "__main__":
    # Example usage
    db = CareerDatabase("test_careers.db")
    
    # Add a sample career
    sample_career = CareerData(
        career_id="software_engineer_001",
        title="Software Engineer",
        description="Design and develop software applications",
        career_field=CareerField.TECHNOLOGY,
        experience_level=ExperienceLevel.MID,
        salary_min=85000,
        salary_max=120000,
        required_technical_skills=["Python", "JavaScript", "SQL"],
        required_soft_skills=["Problem Solving", "Communication"],
        learning_path="Software Engineering Bootcamp (3-6 months)"
    )
    
    db.add_career(sample_career)
    
    # Test retrieval
    retrieved = db.get_career("software_engineer_001")
    print(f"Retrieved career: {retrieved.title if retrieved else 'Not found'}")
    
    # Get statistics
    stats = db.get_career_statistics()
    print(f"Database statistics: {stats}")