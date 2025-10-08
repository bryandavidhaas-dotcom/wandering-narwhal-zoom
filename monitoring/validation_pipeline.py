#!/usr/bin/env python3
"""
Automated Validation Pipeline for Career Platform
Phase 3: Deploy Quality Monitoring System

This module provides continuous validation checks against the CareerModel schema,
detects placeholder content patterns, monitors for duplicates and data inconsistencies,
and generates automated quality reports.
"""

import asyncio
import json
import logging
import re
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from pathlib import Path
from enum import Enum

from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from pydantic import ValidationError
import jsonschema
from jsonschema import validate, ValidationError as JsonSchemaValidationError

# Import models
import sys
sys.path.append(str(Path(__file__).parent.parent))
from backend.models import CareerModel, SkillModel

class ValidationLevel(str, Enum):
    """Validation severity levels"""
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"

@dataclass
class ValidationResult:
    """Individual validation result"""
    record_id: str
    field: str
    validation_type: str
    level: ValidationLevel
    message: str
    current_value: Any
    expected_value: Optional[Any] = None
    timestamp: datetime = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.utcnow()

@dataclass
class ValidationReport:
    """Comprehensive validation report"""
    timestamp: datetime
    total_records: int
    records_validated: int
    validation_results: List[ValidationResult]
    summary: Dict[str, int]
    schema_compliance_rate: float
    placeholder_detection_rate: float
    duplicate_detection_rate: float
    overall_validation_score: float

class SchemaValidator:
    """Schema validation against CareerModel"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.career_schema = self._generate_career_schema()
    
    def _generate_career_schema(self) -> Dict[str, Any]:
        """Generate JSON schema from CareerModel"""
        return {
            "type": "object",
            "properties": {
                "title": {"type": "string", "minLength": 1},
                "description": {"type": "string", "minLength": 10},
                "requiredTechnicalSkills": {
                    "type": "array",
                    "items": {"type": "string"},
                    "minItems": 1
                },
                "requiredSoftSkills": {
                    "type": "array", 
                    "items": {"type": "string"},
                    "minItems": 1
                },
                "experienceLevel": {
                    "type": "string",
                    "enum": ["Entry Level", "Mid Level", "Senior Level", "Executive"]
                },
                "salaryMin": {"type": "integer", "minimum": 0},
                "salaryMax": {"type": "integer", "minimum": 0},
                "careerType": {"type": "string", "minLength": 1},
                "minYearsExperience": {"type": "integer", "minimum": 0},
                "maxYearsExperience": {"type": "integer", "minimum": 0},
                "stretchLevel": {
                    "type": "string",
                    "enum": ["safe_zone", "stretch_zone", "adventure_zone"]
                }
            },
            "required": [
                "title", "description", "requiredTechnicalSkills", 
                "requiredSoftSkills", "experienceLevel", "salaryMin", 
                "salaryMax", "careerType"
            ]
        }
    
    async def validate_career_record(self, career: CareerModel) -> List[ValidationResult]:
        """Validate a single career record against schema"""
        results = []
        career_dict = career.dict()
        
        try:
            # JSON Schema validation
            validate(instance=career_dict, schema=self.career_schema)
            
        except JsonSchemaValidationError as e:
            results.append(ValidationResult(
                record_id=str(career.id),
                field=e.path[-1] if e.path else "unknown",
                validation_type="schema_validation",
                level=ValidationLevel.ERROR,
                message=f"Schema validation failed: {e.message}",
                current_value=e.instance if hasattr(e, 'instance') else None
            ))
        
        # Additional business logic validations
        results.extend(await self._validate_business_rules(career))
        
        return results
    
    async def _validate_business_rules(self, career: CareerModel) -> List[ValidationResult]:
        """Validate business-specific rules"""
        results = []
        
        # Salary range validation
        if career.salaryMin and career.salaryMax:
            if career.salaryMin > career.salaryMax:
                results.append(ValidationResult(
                    record_id=str(career.id),
                    field="salary_range",
                    validation_type="business_rule",
                    level=ValidationLevel.ERROR,
                    message="Minimum salary cannot be greater than maximum salary",
                    current_value=f"Min: {career.salaryMin}, Max: {career.salaryMax}"
                ))
            
            # Unrealistic salary ranges
            if career.salaryMax > 1000000:
                results.append(ValidationResult(
                    record_id=str(career.id),
                    field="salaryMax",
                    validation_type="business_rule",
                    level=ValidationLevel.WARNING,
                    message="Maximum salary seems unrealistically high",
                    current_value=career.salaryMax
                ))
        
        # Experience years validation
        if career.minYearsExperience and career.maxYearsExperience:
            if career.minYearsExperience > career.maxYearsExperience:
                results.append(ValidationResult(
                    record_id=str(career.id),
                    field="experience_years",
                    validation_type="business_rule",
                    level=ValidationLevel.ERROR,
                    message="Minimum experience years cannot be greater than maximum",
                    current_value=f"Min: {career.minYearsExperience}, Max: {career.maxYearsExperience}"
                ))
        
        # Skills validation
        if not career.requiredTechnicalSkills:
            results.append(ValidationResult(
                record_id=str(career.id),
                field="requiredTechnicalSkills",
                validation_type="business_rule",
                level=ValidationLevel.WARNING,
                message="No technical skills specified",
                current_value=career.requiredTechnicalSkills
            ))
        
        if not career.requiredSoftSkills:
            results.append(ValidationResult(
                record_id=str(career.id),
                field="requiredSoftSkills",
                validation_type="business_rule",
                level=ValidationLevel.WARNING,
                message="No soft skills specified",
                current_value=career.requiredSoftSkills
            ))
        
        return results

class PlaceholderDetector:
    """Detects placeholder content patterns"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.placeholder_patterns = [
            r'A brief description of the .+ role',
            r'Technical Skill \d+',
            r'Skill \d+',
            r'Brief description',
            r'Description of .+',
            r'Sample .+',
            r'Example .+',
            r'TODO',
            r'TBD',
            r'To be determined',
            r'Placeholder',
            r'Lorem ipsum',
            r'Test data',
            r'Default .+',
            r'Generic .+',
            r'INSERT .+ HERE',
            r'REPLACE WITH .+',
            r'XXX',
            r'YYY',
            r'ZZZ'
        ]
    
    async def detect_placeholders(self, career: CareerModel) -> List[ValidationResult]:
        """Detect placeholder patterns in career data"""
        results = []
        
        # Check description
        if career.description:
            placeholder_found = self._check_text_for_placeholders(career.description)
            if placeholder_found:
                results.append(ValidationResult(
                    record_id=str(career.id),
                    field="description",
                    validation_type="placeholder_detection",
                    level=ValidationLevel.CRITICAL,
                    message=f"Placeholder content detected: {placeholder_found}",
                    current_value=career.description[:100] + "..." if len(career.description) > 100 else career.description
                ))
        
        # Check technical skills
        if career.requiredTechnicalSkills:
            for i, skill in enumerate(career.requiredTechnicalSkills):
                placeholder_found = self._check_text_for_placeholders(skill)
                if placeholder_found:
                    results.append(ValidationResult(
                        record_id=str(career.id),
                        field=f"requiredTechnicalSkills[{i}]",
                        validation_type="placeholder_detection",
                        level=ValidationLevel.CRITICAL,
                        message=f"Placeholder skill detected: {placeholder_found}",
                        current_value=skill
                    ))
        
        # Check soft skills
        if career.requiredSoftSkills:
            for i, skill in enumerate(career.requiredSoftSkills):
                placeholder_found = self._check_text_for_placeholders(skill)
                if placeholder_found:
                    results.append(ValidationResult(
                        record_id=str(career.id),
                        field=f"requiredSoftSkills[{i}]",
                        validation_type="placeholder_detection",
                        level=ValidationLevel.CRITICAL,
                        message=f"Placeholder skill detected: {placeholder_found}",
                        current_value=skill
                    ))
        
        # Check title
        if career.title:
            placeholder_found = self._check_text_for_placeholders(career.title)
            if placeholder_found:
                results.append(ValidationResult(
                    record_id=str(career.id),
                    field="title",
                    validation_type="placeholder_detection",
                    level=ValidationLevel.CRITICAL,
                    message=f"Placeholder title detected: {placeholder_found}",
                    current_value=career.title
                ))
        
        return results
    
    def _check_text_for_placeholders(self, text: str) -> Optional[str]:
        """Check if text contains placeholder patterns"""
        for pattern in self.placeholder_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return pattern
        return None

class DuplicateDetector:
    """Detects duplicate records and data inconsistencies"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    async def detect_duplicates(self, careers: List[CareerModel]) -> List[ValidationResult]:
        """Detect duplicate records"""
        results = []
        
        # Group by title for duplicate detection
        title_groups = {}
        for career in careers:
            if career.title:
                title_lower = career.title.lower().strip()
                if title_lower not in title_groups:
                    title_groups[title_lower] = []
                title_groups[title_lower].append(career)
        
        # Find duplicates
        for title, career_list in title_groups.items():
            if len(career_list) > 1:
                for career in career_list:
                    results.append(ValidationResult(
                        record_id=str(career.id),
                        field="title",
                        validation_type="duplicate_detection",
                        level=ValidationLevel.WARNING,
                        message=f"Duplicate title found: '{career.title}' ({len(career_list)} occurrences)",
                        current_value=career.title
                    ))
        
        # Check for near-duplicates (similar descriptions)
        results.extend(await self._detect_similar_descriptions(careers))
        
        return results
    
    async def _detect_similar_descriptions(self, careers: List[CareerModel]) -> List[ValidationResult]:
        """Detect careers with very similar descriptions"""
        results = []
        
        # Simple similarity check based on first 100 characters
        description_groups = {}
        for career in careers:
            if career.description and len(career.description) > 50:
                desc_key = career.description[:100].lower().strip()
                if desc_key not in description_groups:
                    description_groups[desc_key] = []
                description_groups[desc_key].append(career)
        
        for desc_key, career_list in description_groups.items():
            if len(career_list) > 1:
                for career in career_list:
                    results.append(ValidationResult(
                        record_id=str(career.id),
                        field="description",
                        validation_type="similarity_detection",
                        level=ValidationLevel.INFO,
                        message=f"Similar description found ({len(career_list)} careers with similar descriptions)",
                        current_value=career.description[:100] + "..."
                    ))
        
        return results

class ValidationPipeline:
    """Main validation pipeline orchestrator"""
    
    def __init__(self, mongo_url: str = "mongodb://localhost:27017", db_name: str = "career_platform"):
        self.mongo_url = mongo_url
        self.db_name = db_name
        self.client = None
        self.db = None
        
        # Initialize validators
        self.schema_validator = SchemaValidator()
        self.placeholder_detector = PlaceholderDetector()
        self.duplicate_detector = DuplicateDetector()
        
        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('monitoring/validation_pipeline.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    async def connect_database(self) -> bool:
        """Initialize database connection"""
        try:
            self.client = AsyncIOMotorClient(self.mongo_url)
            self.db = self.client[self.db_name]
            
            # Test connection
            await self.client.admin.command('ping')
            
            # Initialize Beanie
            await init_beanie(database=self.db, document_models=[CareerModel, SkillModel])
            
            self.logger.info("✅ Database connection established")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Database connection failed: {e}")
            return False
    
    async def run_validation(self) -> ValidationReport:
        """Run comprehensive validation pipeline"""
        self.logger.info("🔍 Starting validation pipeline...")
        
        try:
            # Fetch all career records
            careers = await CareerModel.find_all().to_list()
            total_records = len(careers)
            
            if total_records == 0:
                self.logger.warning("No career records found in database")
                return ValidationReport(
                    timestamp=datetime.utcnow(),
                    total_records=0,
                    records_validated=0,
                    validation_results=[],
                    summary={},
                    schema_compliance_rate=100.0,
                    placeholder_detection_rate=0.0,
                    duplicate_detection_rate=0.0,
                    overall_validation_score=100.0
                )
            
            self.logger.info(f"📊 Validating {total_records} career records...")
            
            all_results = []
            records_validated = 0
            
            # Run schema validation
            self.logger.info("🔧 Running schema validation...")
            for career in careers:
                try:
                    schema_results = await self.schema_validator.validate_career_record(career)
                    all_results.extend(schema_results)
                    records_validated += 1
                except Exception as e:
                    self.logger.error(f"Error validating career {career.id}: {e}")
                    all_results.append(ValidationResult(
                        record_id=str(career.id),
                        field="validation_error",
                        validation_type="system_error",
                        level=ValidationLevel.ERROR,
                        message=f"Validation system error: {str(e)}",
                        current_value=None
                    ))
            
            # Run placeholder detection
            self.logger.info("🎭 Running placeholder detection...")
            for career in careers:
                try:
                    placeholder_results = await self.placeholder_detector.detect_placeholders(career)
                    all_results.extend(placeholder_results)
                except Exception as e:
                    self.logger.error(f"Error detecting placeholders in career {career.id}: {e}")
            
            # Run duplicate detection
            self.logger.info("🔍 Running duplicate detection...")
            try:
                duplicate_results = await self.duplicate_detector.detect_duplicates(careers)
                all_results.extend(duplicate_results)
            except Exception as e:
                self.logger.error(f"Error detecting duplicates: {e}")
            
            # Generate summary
            summary = self._generate_summary(all_results)
            
            # Calculate rates
            schema_compliance_rate = self._calculate_schema_compliance_rate(all_results, total_records)
            placeholder_detection_rate = self._calculate_placeholder_detection_rate(all_results, total_records)
            duplicate_detection_rate = self._calculate_duplicate_detection_rate(all_results, total_records)
            overall_score = self._calculate_overall_validation_score(all_results, total_records)
            
            report = ValidationReport(
                timestamp=datetime.utcnow(),
                total_records=total_records,
                records_validated=records_validated,
                validation_results=all_results,
                summary=summary,
                schema_compliance_rate=schema_compliance_rate,
                placeholder_detection_rate=placeholder_detection_rate,
                duplicate_detection_rate=duplicate_detection_rate,
                overall_validation_score=overall_score
            )
            
            self.logger.info(f"✅ Validation completed - Overall Score: {overall_score:.1f}%")
            return report
            
        except Exception as e:
            self.logger.error(f"❌ Validation pipeline failed: {e}")
            raise
    
    def _generate_summary(self, results: List[ValidationResult]) -> Dict[str, int]:
        """Generate validation results summary"""
        summary = {
            'total_issues': len(results),
            'critical': 0,
            'error': 0,
            'warning': 0,
            'info': 0,
            'schema_violations': 0,
            'placeholder_detections': 0,
            'duplicate_detections': 0,
            'business_rule_violations': 0
        }
        
        for result in results:
            # Count by level
            summary[result.level.value.lower()] += 1
            
            # Count by type
            if result.validation_type == 'schema_validation':
                summary['schema_violations'] += 1
            elif result.validation_type == 'placeholder_detection':
                summary['placeholder_detections'] += 1
            elif result.validation_type in ['duplicate_detection', 'similarity_detection']:
                summary['duplicate_detections'] += 1
            elif result.validation_type == 'business_rule':
                summary['business_rule_violations'] += 1
        
        return summary
    
    def _calculate_schema_compliance_rate(self, results: List[ValidationResult], total_records: int) -> float:
        """Calculate schema compliance rate"""
        if total_records == 0:
            return 100.0
        
        schema_violations = sum(1 for r in results if r.validation_type == 'schema_validation')
        compliance_rate = max(0, 100 - (schema_violations / total_records * 100))
        return compliance_rate
    
    def _calculate_placeholder_detection_rate(self, results: List[ValidationResult], total_records: int) -> float:
        """Calculate placeholder detection rate"""
        if total_records == 0:
            return 0.0
        
        placeholder_records = len(set(r.record_id for r in results if r.validation_type == 'placeholder_detection'))
        detection_rate = (placeholder_records / total_records) * 100
        return detection_rate
    
    def _calculate_duplicate_detection_rate(self, results: List[ValidationResult], total_records: int) -> float:
        """Calculate duplicate detection rate"""
        if total_records == 0:
            return 0.0
        
        duplicate_records = len(set(r.record_id for r in results if r.validation_type in ['duplicate_detection', 'similarity_detection']))
        detection_rate = (duplicate_records / total_records) * 100
        return detection_rate
    
    def _calculate_overall_validation_score(self, results: List[ValidationResult], total_records: int) -> float:
        """Calculate overall validation score"""
        if total_records == 0:
            return 100.0
        
        # Weight different issue types
        weights = {
            ValidationLevel.CRITICAL: 10,
            ValidationLevel.ERROR: 5,
            ValidationLevel.WARNING: 2,
            ValidationLevel.INFO: 1
        }
        
        total_penalty = 0
        for result in results:
            total_penalty += weights.get(result.level, 1)
        
        # Calculate score (max penalty per record is 20)
        max_possible_penalty = total_records * 20
        score = max(0, 100 - (total_penalty / max_possible_penalty * 100))
        
        return score
    
    async def save_validation_report(self, report: ValidationReport, filepath: str = "monitoring/validation_report.json"):
        """Save validation report to file"""
        try:
            Path(filepath).parent.mkdir(parents=True, exist_ok=True)
            
            # Convert report to dict
            report_dict = asdict(report)
            report_dict['timestamp'] = report.timestamp.isoformat()
            
            # Convert ValidationResult timestamps
            for result in report_dict['validation_results']:
                if result['timestamp']:
                    result['timestamp'] = result['timestamp'].isoformat() if isinstance(result['timestamp'], datetime) else result['timestamp']
            
            # Save to file
            with open(filepath, 'w') as f:
                json.dump(report_dict, f, indent=2, default=str)
            
            self.logger.info(f"📄 Validation report saved to {filepath}")
            
        except Exception as e:
            self.logger.error(f"Error saving validation report: {e}")
    
    async def generate_validation_summary_report(self, report: ValidationReport) -> str:
        """Generate human-readable validation summary"""
        summary_report = f"""
# Validation Pipeline Report
Generated: {report.timestamp.strftime('%Y-%m-%d %H:%M:%S UTC')}

## Summary
- **Total Records**: {report.total_records:,}
- **Records Validated**: {report.records_validated:,}
- **Overall Validation Score**: {report.overall_validation_score:.1f}%

## Compliance Rates
- **Schema Compliance**: {report.schema_compliance_rate:.1f}%
- **Placeholder Detection**: {report.placeholder_detection_rate:.1f}%
- **Duplicate Detection**: {report.duplicate_detection_rate:.1f}%

## Issue Summary
- **Total Issues**: {report.summary.get('total_issues', 0):,}
- **Critical**: {report.summary.get('critical', 0):,}
- **Errors**: {report.summary.get('error', 0):,}
- **Warnings**: {report.summary.get('warning', 0):,}
- **Info**: {report.summary.get('info', 0):,}

## Issue Breakdown
- **Schema Violations**: {report.summary.get('schema_violations', 0):,}
- **Placeholder Content**: {report.summary.get('placeholder_detections', 0):,}
- **Duplicate Records**: {report.summary.get('duplicate_detections', 0):,}
- **Business Rule Violations**: {report.summary.get('business_rule_violations', 0):,}

## Recommendations
"""
        
        # Add recommendations based on findings
        if report.overall_validation_score < 80:
            summary_report += "- 🚨 **URGENT**: Overall validation score below 80% - immediate action required\n"
        
        if report.schema_compliance_rate < 95:
            summary_report += "- 🔧 **Schema Issues**: Address schema violations to ensure data integrity\n"
        
        if report.placeholder_detection_rate > 5:
            summary_report += "- 🎭 **Placeholder Content**: Remove placeholder content immediately\n"
        
        if report.duplicate_detection_rate > 10:
            summary_report += "- 🔍 **Duplicates**: Review and consolidate duplicate records\n"
        
        if report.summary.get('critical', 0) > 0:
            summary_report += f"- ⚠️ **Critical Issues**: {report.summary['critical']} critical issues require immediate attention\n"
        
        # Add top issues
        if report.validation_results:
            critical_issues = [r for r in report.validation_results if r.level == ValidationLevel.CRITICAL]
            if critical_issues:
                summary_report += "\n## Top Critical Issues\n"
                for i, issue in enumerate(critical_issues[:5], 1):
                    summary_report += f"{i}. **{issue.field}**: {issue.message}\n"
        
        return summary_report

async def main():
    """Main function to run the validation pipeline"""
    print("🚀 Starting Automated Validation Pipeline")
    print("=" * 50)
    
    # Initialize pipeline
    pipeline = ValidationPipeline()
    
    # Connect to database
    if not await pipeline.connect_database():
        print("❌ Failed to connect to database")
        return
    
    try:
        # Run validation
        report = await pipeline.run_validation()
        
        # Save detailed report
        await pipeline.save_validation_report(report)
        
        # Generate and save summary
        summary = await pipeline.generate_validation_summary_report(report)
        summary_path = "monitoring/validation_summary.md"
        Path(summary_path).parent.mkdir(parents=True, exist_ok=True)
        with open(summary_path, 'w') as f:
            f.write(summary)
        
        print(f"📊 Validation summary saved to {summary_path}")
        
        # Print key metrics
        print(f"\n📈 Validation Results:")
        print(f"  - Overall Score: {report.overall_validation_score:.1f}%")
        print(f"  - Schema Compliance: {report.schema_compliance_rate:.1f}%")
        print(f"  - Total Issues: {report.summary.get('total_issues', 0)}")
        print(f"  - Critical Issues: {report.summary.get('critical', 0)}")
        
        if report.summary.get('critical', 0) > 0:
            print(f"\n🚨 {report.summary['critical']} critical issues detected!")
        else:
            print(f"\n✅ No critical issues detected")
        
    except Exception as e:
        print(f"❌ Validation pipeline failed: {e}")
        raise
    finally:
        if pipeline.client:
            pipeline.client.close()

if __name__ == "__main__":
    asyncio.run(main())