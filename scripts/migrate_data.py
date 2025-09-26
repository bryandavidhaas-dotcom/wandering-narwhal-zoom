#!/usr/bin/env python3
"""
Data Migration Script for Career Templates
==========================================

This script reads the frontend/src/utils/careerMatching.ts file, extracts the 
COMPREHENSIVE_CAREER_TEMPLATES array, and migrates the data to MongoDB.

Features:
- Parses TypeScript career template data
- Connects to MongoDB database
- Upserts career data into 'careers' collection
- Comprehensive error handling and logging
- Data validation and sanitization
- Progress tracking and reporting

Usage:
    python scripts/migrate_data.py

Requirements:
    - pymongo
    - python-dotenv (optional, for environment variables)

Author: Data Migration System
Date: 2025-09-26
"""

import os
import sys
import re
import json
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
from pathlib import Path

try:
    from pymongo import MongoClient, errors as mongo_errors
    from pymongo.collection import Collection
    from pymongo.database import Database
except ImportError:
    print("❌ Error: pymongo is required. Install with: pip install pymongo")
    sys.exit(1)

# Optional: Load environment variables
try:
    from dotenv import load_dotenv
    # Load from backend/.env file
    backend_env_path = Path(__file__).parent.parent / "backend" / ".env"
    load_dotenv(backend_env_path)
except ImportError:
    pass  # dotenv is optional

# Configure logging
# Custom stream handler to handle Unicode characters in Windows console
class UnicodeStreamHandler(logging.StreamHandler):
    def emit(self, record):
        try:
            msg = self.format(record)
            stream = self.stream
            # Encode to UTF-8 and decode with 'replace' error handler
            stream.write(msg + self.terminator)
            self.flush()
        except Exception:
            self.handleError(record)

# Configure logging with UTF-8 file handler and custom stream handler
log_file_handler = logging.FileHandler('scripts/migration.log', encoding='utf-8')

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        log_file_handler,
        UnicodeStreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class CareerDataMigrator:
    """
    Handles the migration of career template data from TypeScript to MongoDB.
    """
    
    def __init__(self, mongo_uri: str = None, database_name: str = "career_platform"):
        """
        Initialize the migrator with MongoDB connection details.
        
        Args:
            mongo_uri: MongoDB connection string
            database_name: Name of the database to use
        """
        self.mongo_uri = mongo_uri or os.getenv('MONGODB_URL', 'mongodb://localhost:27017/')
        self.database_name = database_name
        self.client: Optional[MongoClient] = None
        self.db: Optional[Database] = None
        self.careers_collection: Optional[Collection] = None
        
        # File paths
        self.script_dir = Path(__file__).parent
        self.project_root = self.script_dir.parent
        self.career_matching_file = self.project_root / "frontend" / "src" / "utils" / "careerMatching.ts"
        
        # Migration statistics
        self.stats = {
            'total_processed': 0,
            'successful_inserts': 0,
            'successful_updates': 0,
            'errors': 0,
            'skipped': 0
        }

    def connect_to_mongodb(self) -> bool:
        """
        Establish connection to MongoDB database.
        
        Returns:
            bool: True if connection successful, False otherwise
        """
        try:
            logger.info(f"🔌 Connecting to MongoDB at {self.mongo_uri}")
            self.client = MongoClient(self.mongo_uri, serverSelectionTimeoutMS=5000)
            
            # Test the connection
            self.client.admin.command('ping')
            
            self.db = self.client[self.database_name]
            self.careers_collection = self.db['careers']
            
            logger.info(f"✅ Successfully connected to database: {self.database_name}")
            return True
            
        except mongo_errors.ServerSelectionTimeoutError:
            logger.error("❌ Failed to connect to MongoDB: Server selection timeout")
            return False
        except mongo_errors.ConnectionFailure as e:
            logger.error(f"❌ Failed to connect to MongoDB: {e}")
            return False
        except Exception as e:
            logger.error(f"❌ Unexpected error connecting to MongoDB: {e}")
            return False

    def read_career_matching_file(self) -> str:
        """
        Read the careerMatching.ts file content.
        
        Returns:
            str: File content
            
        Raises:
            FileNotFoundError: If the file doesn't exist
            IOError: If there's an error reading the file
        """
        try:
            logger.info(f"📖 Reading career matching file: {self.career_matching_file}")
            
            if not self.career_matching_file.exists():
                raise FileNotFoundError(f"Career matching file not found: {self.career_matching_file}")
            
            with open(self.career_matching_file, 'r', encoding='utf-8') as file:
                content = file.read()
            
            logger.info(f"✅ Successfully read file ({len(content)} characters)")
            return content
            
        except Exception as e:
            logger.error(f"❌ Error reading career matching file: {e}")
            raise

    def extract_comprehensive_career_templates(self, file_content: str) -> List[Dict[str, Any]]:
        """
        Extract all career templates from TypeScript content by finding all career arrays.
        
        Args:
            file_content: The TypeScript file content
            
        Returns:
            List[Dict[str, Any]]: List of career template dictionaries
        """
        logger.info("🔍 Extracting all career templates from TypeScript content")
        
        try:
            all_careers = []
            
            # Extract COMPREHENSIVE_CAREER_TEMPLATES
            comprehensive_pattern = r'const\s+COMPREHENSIVE_CAREER_TEMPLATES:\s*CareerTemplate\[\]\s*=\s*\['
            comprehensive_match = re.search(comprehensive_pattern, file_content)
            
            if comprehensive_match:
                logger.info("📋 Found COMPREHENSIVE_CAREER_TEMPLATES")
                start_pos = comprehensive_match.end() - 1
                array_content = self._extract_array_content(file_content, start_pos)
                comprehensive_careers = self._parse_career_objects(array_content)
                all_careers.extend(comprehensive_careers)
                logger.info(f"✅ Extracted {len(comprehensive_careers)} comprehensive career templates")
            
            # Also try to extract from imported modules by looking for career objects directly
            # This is a fallback approach to catch any careers we might have missed
            logger.info("🔍 Searching for additional career objects in file...")
            
            # Look for individual career objects that might be defined elsewhere
            career_object_pattern = r'\{\s*title:\s*["\'][^"\']+["\']'
            career_matches = re.finditer(career_object_pattern, file_content)
            
            additional_careers = []
            for match in career_matches:
                try:
                    # Find the full object
                    start_pos = match.start()
                    obj_content = self._extract_single_object(file_content, start_pos)
                    if obj_content:
                        career = self._parse_single_career_object(obj_content)
                        if career and career not in all_careers:
                            # Check if this career is not already in our list
                            existing_titles = [c.get('title', '') for c in all_careers]
                            if career.get('title', '') not in existing_titles:
                                additional_careers.append(career)
                except Exception as e:
                    logger.debug(f"Skipping career object due to parsing error: {e}")
                    continue
            
            if additional_careers:
                all_careers.extend(additional_careers)
                logger.info(f"✅ Found {len(additional_careers)} additional career objects")
            
            logger.info(f"✅ Successfully extracted {len(all_careers)} total career templates")
            return all_careers
            
        except Exception as e:
            logger.error(f"❌ Error extracting career templates: {e}")
            raise
    
    def _extract_array_content(self, file_content: str, start_pos: int) -> str:
        """Extract array content from start position to matching closing bracket."""
        bracket_count = 0
        pos = start_pos
        
        while pos < len(file_content):
            char = file_content[pos]
            if char == '[':
                bracket_count += 1
            elif char == ']':
                bracket_count -= 1
                if bracket_count == 0:
                    break
            pos += 1
        
        if bracket_count != 0:
            raise ValueError("Could not find matching closing bracket")
        
        return file_content[start_pos:pos + 1]
    
    def _extract_single_object(self, file_content: str, start_pos: int) -> str:
        """Extract a single object from start position to matching closing brace."""
        brace_count = 0
        pos = start_pos
        
        while pos < len(file_content):
            char = file_content[pos]
            if char == '{':
                brace_count += 1
            elif char == '}':
                brace_count -= 1
                if brace_count == 0:
                    break
            pos += 1
        
        if brace_count != 0:
            return ""
        
        return file_content[start_pos:pos + 1]

    def _parse_career_objects(self, array_content: str) -> List[Dict[str, Any]]:
        """
        Parse individual career objects from the array content.
        
        Args:
            array_content: The array content string
            
        Returns:
            List[Dict[str, Any]]: List of parsed career objects
        """
        careers = []
        
        # Remove the outer brackets and split by career objects
        content = array_content.strip()[1:-1]  # Remove [ and ]
        
        # Find individual career objects (they start with { and end with })
        career_objects = []
        brace_count = 0
        current_object = ""
        
        for char in content:
            current_object += char
            if char == '{':
                brace_count += 1
            elif char == '}':
                brace_count -= 1
                if brace_count == 0:
                    career_objects.append(current_object.strip())
                    current_object = ""
        
        logger.info(f"🔍 Found {len(career_objects)} career objects to parse")
        
        for i, obj_str in enumerate(career_objects):
            try:
                career = self._parse_single_career_object(obj_str)
                if career:
                    careers.append(career)
            except Exception as e:
                logger.warning(f"⚠️ Failed to parse career object {i + 1}: {e}")
                self.stats['errors'] += 1
        
        return careers

    def _parse_single_career_object(self, obj_str: str) -> Optional[Dict[str, Any]]:
        """
        Parse a single career object from TypeScript format to Python dict.
        
        Args:
            obj_str: The career object string
            
        Returns:
            Optional[Dict[str, Any]]: Parsed career object or None if parsing fails
        """
        try:
            # Clean up the object string
            obj_str = obj_str.strip()
            if obj_str.endswith(','):
                obj_str = obj_str[:-1]
            
            career = {}
            
            # Extract key-value pairs using regex
            # Handle different value types: strings, numbers, booleans, arrays
            patterns = [
                # String values
                (r'(\w+):\s*"([^"]*)"', lambda k, v: (k, v)),
                # String values with single quotes
                (r"(\w+):\s*'([^']*)'", lambda k, v: (k, v)),
                # Number values
                (r'(\w+):\s*(\d+(?:\.\d+)?)', lambda k, v: (k, float(v) if '.' in v else int(v))),
                # Boolean values
                (r'(\w+):\s*(true|false)', lambda k, v: (k, v == 'true')),
                # Array values
                (r'(\w+):\s*\[(.*?)\]', self._parse_array_value),
            ]
            
            for pattern, handler in patterns:
                matches = re.finditer(pattern, obj_str, re.DOTALL)
                for match in matches:
                    key, value = handler(match.group(1), match.group(2))
                    career[key] = value
            
            # Validate required fields
            required_fields = ['title', 'salaryRange', 'description']
            if not all(field in career for field in required_fields):
                logger.warning(f"⚠️ Career object missing required fields: {career.get('title', 'Unknown')}")
                return None
            
            return career
            
        except Exception as e:
            logger.error(f"❌ Error parsing career object: {e}")
            return None

    def _parse_array_value(self, key: str, array_content: str) -> tuple:
        """
        Parse array values from TypeScript format.
        
        Args:
            key: The field key
            array_content: The array content string
            
        Returns:
            tuple: (key, parsed_array)
        """
        try:
            # Split by commas and clean up each item
            items = []
            current_item = ""
            in_quotes = False
            quote_char = None
            
            for char in array_content:
                if char in ['"', "'"] and not in_quotes:
                    in_quotes = True
                    quote_char = char
                elif char == quote_char and in_quotes:
                    in_quotes = False
                    quote_char = None
                elif char == ',' and not in_quotes:
                    items.append(current_item.strip().strip('"\''))
                    current_item = ""
                    continue
                
                current_item += char
            
            # Add the last item
            if current_item.strip():
                items.append(current_item.strip().strip('"\''))
            
            # Filter out empty items
            items = [item for item in items if item]
            
            return key, items
            
        except Exception as e:
            logger.warning(f"⚠️ Error parsing array for key {key}: {e}")
            return key, []

    def validate_and_sanitize_career(self, career: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate and sanitize a career object before database insertion.
        
        Args:
            career: The career dictionary to validate
            
        Returns:
            Dict[str, Any]: Validated and sanitized career object
        """
        try:
            # Create a copy to avoid modifying the original
            sanitized = career.copy()
            
            # Ensure required string fields
            string_fields = ['title', 'salaryRange', 'description', 'learningPath', 'stretchLevel', 
                           'careerType', 'dayInLife', 'experienceLevel', 'remoteOptions']
            
            for field in string_fields:
                if field not in sanitized or not isinstance(sanitized[field], str):
                    sanitized[field] = sanitized.get(field, 'Not specified')
            
            # Ensure required array fields
            array_fields = ['requiredTechnicalSkills', 'requiredSoftSkills', 'preferredInterests', 
                          'preferredIndustries', 'companies', 'workEnvironments', 'valuedCertifications',
                          'requiredCertifications', 'resumeKeywords', 'relatedJobTitles', 'valuedCompanies',
                          'preferredIndustryExperience', 'careerProgressionPatterns', 'alternativeQualifications']
            
            for field in array_fields:
                if field not in sanitized or not isinstance(sanitized[field], list):
                    sanitized[field] = []
            
            # Ensure required numeric fields
            numeric_fields = {
                'workDataWeight': 3, 'workPeopleWeight': 3, 'creativityWeight': 3,
                'problemSolvingWeight': 3, 'leadershipWeight': 3, 'handsOnWorkWeight': 3,
                'physicalWorkWeight': 3, 'outdoorWorkWeight': 3, 'mechanicalAptitudeWeight': 3,
                'workLifeBalanceRating': 3, 'minYearsExperience': 0, 'maxYearsExperience': 10,
                'salaryMin': 50000, 'salaryMax': 100000
            }
            
            for field, default_value in numeric_fields.items():
                if field not in sanitized or not isinstance(sanitized[field], (int, float)):
                    sanitized[field] = default_value
            
            # Ensure required boolean fields
            boolean_fields = {
                'requiresTechnical': True, 'transitionFriendly': True,
                'skillBasedEntry': True, 'experienceCanSubstitute': True
            }
            
            for field, default_value in boolean_fields.items():
                if field not in sanitized or not isinstance(sanitized[field], bool):
                    sanitized[field] = default_value
            
            # Add metadata
            sanitized['_migrated_at'] = datetime.utcnow()
            sanitized['_migration_version'] = '1.0'
            
            return sanitized
            
        except Exception as e:
            logger.error(f"❌ Error validating career {career.get('title', 'Unknown')}: {e}")
            raise

    def upsert_career_to_mongodb(self, career: Dict[str, Any]) -> bool:
        """
        Insert or update a career in the MongoDB collection.
        
        Args:
            career: The career dictionary to upsert
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Use careerType as the unique identifier
            filter_query = {'careerType': career['careerType']}
            
            # Perform upsert operation
            result = self.careers_collection.replace_one(
                filter_query,
                career,
                upsert=True
            )
            
            if result.upserted_id:
                logger.debug(f"✅ Inserted new career: {career['title']}")
                self.stats['successful_inserts'] += 1
            elif result.modified_count > 0:
                logger.debug(f"🔄 Updated existing career: {career['title']}")
                self.stats['successful_updates'] += 1
            else:
                logger.debug(f"➡️ No changes needed for career: {career['title']}")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Error upserting career {career.get('title', 'Unknown')}: {e}")
            self.stats['errors'] += 1
            return False

    def create_indexes(self):
        """
        Create necessary indexes on the careers collection for optimal performance.
        """
        try:
            logger.info("🔧 Creating database indexes...")
            
            # Create indexes for common query patterns
            indexes = [
                ('careerType', 1),  # Unique identifier
                ('experienceLevel', 1),  # Filter by experience level
                ('title', 'text'),  # Text search on title
                ('description', 'text'),  # Text search on description
                ('preferredIndustries', 1),  # Filter by industry
                ('salaryMin', 1),  # Salary range queries
                ('salaryMax', 1),
                ('_migrated_at', -1)  # Sort by migration date
            ]
            
            for index_spec in indexes:
                try:
                    if isinstance(index_spec, tuple) and len(index_spec) == 2:
                        if index_spec[1] == 'text':
                            self.careers_collection.create_index([(index_spec[0], 'text')])
                        else:
                            self.careers_collection.create_index([(index_spec[0], index_spec[1])])
                    logger.debug(f"✅ Created index: {index_spec}")
                except mongo_errors.OperationFailure as e:
                    if "already exists" not in str(e):
                        logger.warning(f"⚠️ Could not create index {index_spec}: {e}")
            
            logger.info("✅ Database indexes created successfully")
            
        except Exception as e:
            logger.error(f"❌ Error creating indexes: {e}")

    def load_dynamic_descriptions(self) -> dict:
        """Loads the dynamically extracted descriptions from the JSON file."""
        descriptions_file = self.script_dir / "dynamic_descriptions.json"
        if not descriptions_file.exists():
            logger.warning("⚠️ dynamic_descriptions.json not found. Skipping dynamic descriptions.")
            return {}
        
        with open(descriptions_file, 'r', encoding='utf-8') as f:
            return json.load(f)

    def merge_dynamic_descriptions(self, careers: list, descriptions: dict) -> list:
        """Merges the dynamic descriptions into the career templates."""
        for career in careers:
            title = career.get('title', '').lower()
            matched_description = None
            
            for key, desc in descriptions.items():
                if key != 'default' and key in title:
                    matched_description = desc
                    break
            
            if matched_description:
                career['dayInLife'] = matched_description
            elif 'default' in descriptions:
                career['dayInLife'] = descriptions['default'].replace('{careerTitle}', career.get('title', ''))
                
        return careers

    def run_migration(self) -> bool:
        """
        Execute the complete migration process.
        
        Returns:
            bool: True if migration completed successfully, False otherwise
        """
        start_time = datetime.now()
        logger.info("🚀 Starting career data migration...")
        
        try:
            # Step 1: Connect to MongoDB
            if not self.connect_to_mongodb():
                return False
            
            # Step 2: Read the TypeScript file
            file_content = self.read_career_matching_file()
            
            # Step 3: Extract career templates
            careers = self.extract_comprehensive_career_templates(file_content)
            
            if not careers:
                logger.error("❌ No career templates found to migrate")
                return False

            # Load dynamic descriptions
            dynamic_descriptions = self.load_dynamic_descriptions()
            
            # Merge dynamic descriptions into careers
            careers = self.merge_dynamic_descriptions(careers, dynamic_descriptions)
            
            # Step 4: Create database indexes
            self.create_indexes()
            
            # Step 5: Process each career
            logger.info(f"📊 Processing {len(careers)} career templates...")
            
            for i, career in enumerate(careers, 1):
                try:
                    self.stats['total_processed'] += 1
                    
                    # Validate and sanitize
                    sanitized_career = self.validate_and_sanitize_career(career)
                    
                    # Upsert to MongoDB
                    success = self.upsert_career_to_mongodb(sanitized_career)
                    
                    if not success:
                        self.stats['errors'] += 1
                    
                    # Progress reporting
                    if i % 10 == 0 or i == len(careers):
                        logger.info(f"📈 Progress: {i}/{len(careers)} careers processed")
                        
                except Exception as e:
                    logger.error(f"❌ Error processing career {i}: {e}")
                    self.stats['errors'] += 1
            
            # Step 6: Report results
            self._report_migration_results(start_time)
            
            return self.stats['errors'] == 0
            
        except Exception as e:
            logger.error(f"❌ Migration failed with error: {e}")
            return False
        
        finally:
            # Clean up MongoDB connection
            if self.client:
                self.client.close()
                logger.info("🔌 MongoDB connection closed")

    def _report_migration_results(self, start_time: datetime):
        """
        Report the migration results and statistics.
        
        Args:
            start_time: When the migration started
        """
        end_time = datetime.now()
        duration = end_time - start_time
        
        logger.info("=" * 60)
        logger.info("📊 MIGRATION RESULTS")
        logger.info("=" * 60)
        logger.info(f"⏱️  Duration: {duration}")
        logger.info(f"📈 Total Processed: {self.stats['total_processed']}")
        logger.info(f"✅ Successful Inserts: {self.stats['successful_inserts']}")
        logger.info(f"🔄 Successful Updates: {self.stats['successful_updates']}")
        logger.info(f"❌ Errors: {self.stats['errors']}")
        logger.info(f"⏭️  Skipped: {self.stats['skipped']}")
        
        success_rate = ((self.stats['successful_inserts'] + self.stats['successful_updates']) / 
                       max(self.stats['total_processed'], 1)) * 100
        logger.info(f"🎯 Success Rate: {success_rate:.1f}%")
        
        if self.stats['errors'] == 0:
            logger.info("🎉 Migration completed successfully!")
        else:
            logger.warning(f"⚠️ Migration completed with {self.stats['errors']} errors")
        
        logger.info("=" * 60)


def main():
    """
    Main entry point for the migration script.
    """
    try:
        # Initialize migrator
        migrator = CareerDataMigrator()
        
        # Run migration
        success = migrator.run_migration()
        
        # Exit with appropriate code
        sys.exit(0 if success else 1)
        
    except KeyboardInterrupt:
        logger.info("🛑 Migration interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"❌ Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()