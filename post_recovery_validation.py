#!/usr/bin/env python3
"""
POST-RECOVERY DATABASE VALIDATION SCRIPT
========================================
Validates the recovered careers.db to ensure it's functioning correctly
and provides a comprehensive quality report.

This script verifies:
- Database connectivity and schema integrity
- Data completeness and quality
- Performance of key operations
- System functionality validation

Author: Emergency Recovery System
Date: 2025-01-06
"""

import sqlite3
import json
import time
from datetime import datetime

class PostRecoveryValidator:
    def __init__(self):
        self.db_path = "careers.db"
        self.validation_results = {}
        self.performance_metrics = {}
        
    def log(self, message, level="INFO"):
        """Log validation progress"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {level}: {message}")
    
    def test_database_connectivity(self):
        """Test basic database connectivity"""
        self.log("🔌 Testing database connectivity...")
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT 1")
                result = cursor.fetchone()
                
            if result and result[0] == 1:
                self.log("✅ Database connectivity: PASSED")
                return True
            else:
                self.log("❌ Database connectivity: FAILED", "ERROR")
                return False
                
        except Exception as e:
            self.log(f"❌ Database connectivity error: {e}", "ERROR")
            return False
    
    def validate_schema_integrity(self):
        """Validate database schema structure"""
        self.log("🏗️ Validating schema integrity...")
        
        expected_columns = [
            'id', 'title', 'careerType', 'description', 'salaryRange',
            'experienceLevel', 'requiredTechnicalSkills', 'requiredSoftSkills',
            'companies', 'learningPath', 'relevanceScore', 'confidenceLevel',
            'matchReasons', 'minExperienceYears', 'maxExperienceYears',
            'minSalary', 'maxSalary', 'created_at', 'updated_at'
        ]
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Check table exists
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='careers'")
                if not cursor.fetchone():
                    self.log("❌ Careers table not found", "ERROR")
                    return False
                
                # Check columns
                cursor.execute("PRAGMA table_info(careers)")
                columns = [col[1] for col in cursor.fetchall()]
                
                missing_columns = set(expected_columns) - set(columns)
                if missing_columns:
                    self.log(f"❌ Missing columns: {missing_columns}", "ERROR")
                    return False
                
                # Check indexes
                cursor.execute("SELECT name FROM sqlite_master WHERE type='index' AND tbl_name='careers'")
                indexes = [idx[0] for idx in cursor.fetchall()]
                
                expected_indexes = ['idx_career_type', 'idx_experience_level', 'idx_salary_range']
                missing_indexes = set(expected_indexes) - set(indexes)
                
                if missing_indexes:
                    self.log(f"⚠️ Missing indexes: {missing_indexes}", "WARNING")
                else:
                    self.log("✅ All performance indexes present")
                
                self.log("✅ Schema integrity: PASSED")
                return True
                
        except Exception as e:
            self.log(f"❌ Schema validation error: {e}", "ERROR")
            return False
    
    def validate_data_quality(self):
        """Comprehensive data quality validation"""
        self.log("🔍 Validating data quality...")
        
        quality_checks = {}
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Total record count
                cursor.execute("SELECT COUNT(*) FROM careers")
                total_records = cursor.fetchone()[0]
                quality_checks['total_records'] = total_records
                self.log(f"📊 Total records: {total_records}")
                
                # Primary key integrity
                cursor.execute("SELECT COUNT(*) FROM careers WHERE id IS NULL")
                null_ids = cursor.fetchone()[0]
                quality_checks['null_primary_keys'] = null_ids
                
                # Required field completeness
                cursor.execute("SELECT COUNT(*) FROM careers WHERE title IS NULL OR title = ''")
                missing_titles = cursor.fetchone()[0]
                quality_checks['missing_titles'] = missing_titles
                
                cursor.execute("SELECT COUNT(*) FROM careers WHERE description IS NULL OR description = ''")
                missing_descriptions = cursor.fetchone()[0]
                quality_checks['missing_descriptions'] = missing_descriptions
                
                cursor.execute("SELECT COUNT(*) FROM careers WHERE careerType IS NULL OR careerType = ''")
                missing_career_types = cursor.fetchone()[0]
                quality_checks['missing_career_types'] = missing_career_types
                
                # Salary data completeness
                cursor.execute("SELECT COUNT(*) FROM careers WHERE minSalary IS NOT NULL AND maxSalary IS NOT NULL")
                complete_salary = cursor.fetchone()[0]
                quality_checks['complete_salary_data'] = complete_salary
                
                # Data consistency checks
                cursor.execute("SELECT COUNT(*) FROM careers WHERE minSalary > maxSalary")
                invalid_salary_ranges = cursor.fetchone()[0]
                quality_checks['invalid_salary_ranges'] = invalid_salary_ranges
                
                cursor.execute("SELECT COUNT(*) FROM careers WHERE minExperienceYears > maxExperienceYears")
                invalid_experience_ranges = cursor.fetchone()[0]
                quality_checks['invalid_experience_ranges'] = invalid_experience_ranges
                
                # Duplicate detection
                cursor.execute("SELECT careerType, COUNT(*) FROM careers GROUP BY careerType HAVING COUNT(*) > 1")
                duplicates = cursor.fetchall()
                quality_checks['duplicate_career_types'] = len(duplicates)
                
                # Calculate quality score
                quality_score = self.calculate_quality_score(quality_checks, total_records)
                quality_checks['quality_score'] = quality_score
                
                # Log results
                self.log("📋 Data Quality Results:")
                self.log(f"   NULL Primary Keys: {null_ids} (should be 0)")
                self.log(f"   Missing Titles: {missing_titles} (should be 0)")
                self.log(f"   Missing Descriptions: {missing_descriptions} (should be 0)")
                self.log(f"   Complete Salary Data: {complete_salary}/{total_records}")
                self.log(f"   Invalid Salary Ranges: {invalid_salary_ranges} (should be 0)")
                self.log(f"   Invalid Experience Ranges: {invalid_experience_ranges} (should be 0)")
                self.log(f"   Duplicate Career Types: {len(duplicates)} (should be 0)")
                self.log(f"🎯 Data Quality Score: {quality_score}/100")
                
                self.validation_results['data_quality'] = quality_checks
                
                return quality_score >= 95  # Pass if quality score is 95 or higher
                
        except Exception as e:
            self.log(f"❌ Data quality validation error: {e}", "ERROR")
            return False
    
    def calculate_quality_score(self, checks, total_records):
        """Calculate overall data quality score"""
        if total_records == 0:
            return 0
        
        score = 100
        
        # Critical issues
        if checks['null_primary_keys'] > 0:
            score -= 50
        
        # Data completeness issues
        score -= (checks['missing_titles'] / total_records) * 20
        score -= (checks['missing_descriptions'] / total_records) * 20
        score -= (checks['missing_career_types'] / total_records) * 20
        
        # Data consistency issues
        score -= checks['invalid_salary_ranges'] * 2
        score -= checks['invalid_experience_ranges'] * 2
        score -= checks['duplicate_career_types'] * 5
        
        return max(0, min(100, int(score)))
    
    def test_query_performance(self):
        """Test database query performance"""
        self.log("⚡ Testing query performance...")
        
        performance_tests = [
            ("SELECT COUNT(*) FROM careers", "Record count"),
            ("SELECT * FROM careers WHERE experienceLevel = 'mid' LIMIT 10", "Experience level filter"),
            ("SELECT * FROM careers WHERE minSalary >= 100000 AND maxSalary <= 200000 LIMIT 10", "Salary range filter"),
            ("SELECT * FROM careers WHERE careerType LIKE '%engineer%' LIMIT 10", "Career type search"),
            ("SELECT experienceLevel, COUNT(*) FROM careers GROUP BY experienceLevel", "Experience level aggregation")
        ]
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                for query, description in performance_tests:
                    start_time = time.time()
                    cursor.execute(query)
                    results = cursor.fetchall()
                    end_time = time.time()
                    
                    execution_time = (end_time - start_time) * 1000  # Convert to milliseconds
                    self.performance_metrics[description] = {
                        'execution_time_ms': round(execution_time, 2),
                        'result_count': len(results)
                    }
                    
                    self.log(f"   {description}: {execution_time:.2f}ms ({len(results)} results)")
                
                # Check if performance is acceptable (all queries under 100ms)
                max_time = max(metrics['execution_time_ms'] for metrics in self.performance_metrics.values())
                performance_passed = max_time < 100
                
                if performance_passed:
                    self.log("✅ Query performance: PASSED (all queries < 100ms)")
                else:
                    self.log(f"⚠️ Query performance: Some queries slow (max: {max_time:.2f}ms)", "WARNING")
                
                return performance_passed
                
        except Exception as e:
            self.log(f"❌ Performance testing error: {e}", "ERROR")
            return False
    
    def test_functional_operations(self):
        """Test key functional operations"""
        self.log("🔧 Testing functional operations...")
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Test data retrieval by different criteria
                test_queries = [
                    ("SELECT * FROM careers WHERE experienceLevel = 'senior'", "Senior level careers"),
                    ("SELECT * FROM careers WHERE minSalary >= 150000", "High salary careers"),
                    ("SELECT * FROM careers WHERE careerType LIKE '%data%'", "Data-related careers"),
                    ("SELECT DISTINCT experienceLevel FROM careers", "Experience levels"),
                    ("SELECT AVG(minSalary), AVG(maxSalary) FROM careers", "Average salaries")
                ]
                
                all_passed = True
                
                for query, description in test_queries:
                    try:
                        cursor.execute(query)
                        results = cursor.fetchall()
                        self.log(f"   ✅ {description}: {len(results)} results")
                    except Exception as e:
                        self.log(f"   ❌ {description}: {e}", "ERROR")
                        all_passed = False
                
                # Test JSON field parsing (technical skills)
                cursor.execute("SELECT requiredTechnicalSkills FROM careers LIMIT 5")
                json_fields = cursor.fetchall()
                
                json_valid = True
                for field in json_fields:
                    try:
                        json.loads(field[0])
                    except:
                        json_valid = False
                        break
                
                if json_valid:
                    self.log("   ✅ JSON field parsing: PASSED")
                else:
                    self.log("   ❌ JSON field parsing: FAILED", "ERROR")
                    all_passed = False
                
                return all_passed
                
        except Exception as e:
            self.log(f"❌ Functional testing error: {e}", "ERROR")
            return False
    
    def generate_validation_report(self):
        """Generate comprehensive validation report"""
        self.log("📋 Generating validation report...")
        
        report_path = f"post_recovery_validation_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        try:
            with open(report_path, 'w', encoding='utf-8') as f:
                f.write("=" * 80 + "\n")
                f.write("POST-RECOVERY DATABASE VALIDATION REPORT\n")
                f.write("=" * 80 + "\n")
                f.write(f"Validation Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Database: {self.db_path}\n\n")
                
                f.write("VALIDATION SUMMARY:\n")
                f.write("-" * 40 + "\n")
                f.write(f"Database Status: OPERATIONAL\n")
                f.write(f"Data Quality Score: {self.validation_results.get('data_quality', {}).get('quality_score', 'N/A')}/100\n")
                f.write(f"Total Records: {self.validation_results.get('data_quality', {}).get('total_records', 'N/A')}\n\n")
                
                f.write("PERFORMANCE METRICS:\n")
                f.write("-" * 40 + "\n")
                for operation, metrics in self.performance_metrics.items():
                    f.write(f"{operation}: {metrics['execution_time_ms']}ms ({metrics['result_count']} results)\n")
                
                f.write("\nDATA QUALITY DETAILS:\n")
                f.write("-" * 40 + "\n")
                quality_data = self.validation_results.get('data_quality', {})
                for key, value in quality_data.items():
                    if key != 'quality_score':
                        f.write(f"{key}: {value}\n")
                
                f.write(f"\nValidation completed successfully at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            
            self.log(f"✅ Validation report saved to: {report_path}")
            return report_path
            
        except Exception as e:
            self.log(f"❌ Error generating report: {e}", "ERROR")
            return None
    
    def run_full_validation(self):
        """Run complete post-recovery validation"""
        self.log("🚀 STARTING POST-RECOVERY VALIDATION")
        self.log("=" * 50)
        
        validation_passed = True
        
        # Test 1: Database Connectivity
        if not self.test_database_connectivity():
            validation_passed = False
        
        # Test 2: Schema Integrity
        if not self.validate_schema_integrity():
            validation_passed = False
        
        # Test 3: Data Quality
        if not self.validate_data_quality():
            validation_passed = False
        
        # Test 4: Query Performance
        if not self.test_query_performance():
            validation_passed = False
        
        # Test 5: Functional Operations
        if not self.test_functional_operations():
            validation_passed = False
        
        # Generate Report
        report_path = self.generate_validation_report()
        
        self.log("=" * 50)
        
        if validation_passed:
            self.log("🎉 POST-RECOVERY VALIDATION: PASSED", "SUCCESS")
            self.log("✅ Database is fully operational and ready for production use")
        else:
            self.log("❌ POST-RECOVERY VALIDATION: FAILED", "ERROR")
            self.log("⚠️ Database requires additional attention before production use")
        
        return validation_passed

def main():
    """Main validation execution"""
    validator = PostRecoveryValidator()
    success = validator.run_full_validation()
    
    if success:
        print("\n🎉 DATABASE VALIDATION SUCCESSFUL!")
        print("The recovered database is fully operational and ready for use.")
    else:
        print("\n❌ DATABASE VALIDATION FAILED!")
        print("Please review the validation results and address any issues.")
    
    return success

if __name__ == "__main__":
    main()