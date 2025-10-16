#!/usr/bin/env python3
"""
Comprehensive Data Quality Analysis for Careers Database System

This script analyzes all three data sources:
1. careers.db (SQLite database)
2. new_career_data.json (49 records with placeholder content)
3. production_career_data.json (361 records, production-ready)

Identifies and reports:
- Records with NULL or empty critical fields
- Placeholder patterns
- Generic/template data
- Inconsistent data formats
- Missing required fields
- Data quality scores
"""

import sqlite3
import json
import re
from pathlib import Path
from typing import Dict, List, Any, Tuple
from collections import defaultdict, Counter
from datetime import datetime
import statistics

class CareerDataQualityAnalyzer:
    def __init__(self):
        self.results = {
            'sqlite_db': {},
            'new_career_data': {},
            'production_career_data': {},
            'summary': {},
            'recommendations': []
        }
        
        # Define placeholder patterns to detect
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
            r'Generic .+'
        ]
        
        # Define required fields based on MongoDB schema
        self.required_fields = [
            'title',
            'careerType',
            'description',
            'salaryRange',
            'experienceLevel',
            'requiredTechnicalSkills',
            'requiredSoftSkills',
            'minExperienceYears',
            'maxExperienceYears',
            'minSalary',
            'maxSalary'
        ]
        
        # Define critical fields that should not be generic
        self.critical_fields = [
            'title',
            'description',
            'requiredTechnicalSkills',
            'companies'
        ]

    def analyze_sqlite_database(self, db_path: str = "careers.db") -> Dict[str, Any]:
        """Analyze the SQLite careers database"""
        print("🔍 Analyzing SQLite Database (careers.db)...")
        
        db_path = Path(db_path)
        if not db_path.exists():
            return {"error": f"Database file not found at: {db_path}"}
        
        analysis = {
            'file_exists': True,
            'total_records': 0,
            'schema_info': {},
            'data_quality': {},
            'placeholder_analysis': {},
            'field_completeness': {},
            'examples': {}
        }
        
        try:
            with sqlite3.connect(db_path) as conn:
                cursor = conn.cursor()
                
                # Get schema information
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                tables = cursor.fetchall()
                
                if not tables:
                    analysis['error'] = "No tables found in database"
                    return analysis
                
                # Focus on careers table
                if any(table[0] == 'careers' for table in tables):
                    # Get table schema
                    cursor.execute("PRAGMA table_info(careers);")
                    columns = cursor.fetchall()
                    analysis['schema_info'] = {
                        'columns': [{'name': col[1], 'type': col[2], 'not_null': bool(col[3]), 'primary_key': bool(col[5])} for col in columns],
                        'column_count': len(columns)
                    }
                    
                    # Get total record count
                    cursor.execute("SELECT COUNT(*) FROM careers;")
                    total_records = cursor.fetchone()[0]
                    analysis['total_records'] = total_records
                    
                    if total_records > 0:
                        # Analyze data quality
                        analysis['data_quality'] = self._analyze_sqlite_data_quality(cursor)
                        analysis['placeholder_analysis'] = self._analyze_sqlite_placeholders(cursor)
                        analysis['field_completeness'] = self._analyze_sqlite_field_completeness(cursor)
                        analysis['examples'] = self._get_sqlite_examples(cursor)
                    
                else:
                    analysis['error'] = "No 'careers' table found in database"
                    
        except sqlite3.Error as e:
            analysis['error'] = f"SQLite error: {e}"
        except Exception as e:
            analysis['error'] = f"Unexpected error: {e}"
            
        return analysis

    def _analyze_sqlite_data_quality(self, cursor) -> Dict[str, Any]:
        """Analyze data quality issues in SQLite database"""
        quality_issues = {}
        
        # Check for NULL primary keys
        cursor.execute("SELECT COUNT(*) FROM careers WHERE id IS NULL;")
        null_ids = cursor.fetchone()[0]
        quality_issues['null_primary_keys'] = null_ids
        
        # Check for empty/null critical fields
        critical_field_issues = {}
        for field in ['title', 'description', 'salaryRange', 'experienceLevel']:
            try:
                cursor.execute(f"SELECT COUNT(*) FROM careers WHERE {field} IS NULL OR {field} = '';")
                empty_count = cursor.fetchone()[0]
                critical_field_issues[field] = empty_count
            except sqlite3.OperationalError:
                critical_field_issues[field] = "Field not found"
        
        quality_issues['critical_field_issues'] = critical_field_issues
        
        # Check for duplicate titles
        cursor.execute("SELECT title, COUNT(*) FROM careers WHERE title IS NOT NULL GROUP BY title HAVING COUNT(*) > 1;")
        duplicates = cursor.fetchall()
        quality_issues['duplicate_titles'] = len(duplicates)
        quality_issues['duplicate_examples'] = duplicates[:5]  # First 5 examples
        
        return quality_issues

    def _analyze_sqlite_placeholders(self, cursor) -> Dict[str, Any]:
        """Analyze placeholder patterns in SQLite database"""
        placeholder_analysis = {}
        
        # Check description field for placeholder patterns
        cursor.execute("SELECT description FROM careers WHERE description IS NOT NULL;")
        descriptions = [row[0] for row in cursor.fetchall()]
        
        placeholder_counts = {}
        for pattern in self.placeholder_patterns:
            count = sum(1 for desc in descriptions if re.search(pattern, desc, re.IGNORECASE))
            if count > 0:
                placeholder_counts[pattern] = count
        
        placeholder_analysis['description_placeholders'] = placeholder_counts
        placeholder_analysis['total_placeholder_descriptions'] = len([d for d in descriptions if any(re.search(p, d, re.IGNORECASE) for p in self.placeholder_patterns)])
        placeholder_analysis['total_descriptions'] = len(descriptions)
        
        # Check for generic salary ranges
        cursor.execute("SELECT salaryRange, COUNT(*) FROM careers WHERE salaryRange IS NOT NULL GROUP BY salaryRange ORDER BY COUNT(*) DESC LIMIT 5;")
        salary_distribution = cursor.fetchall()
        placeholder_analysis['salary_distribution'] = salary_distribution
        
        return placeholder_analysis

    def _analyze_sqlite_field_completeness(self, cursor) -> Dict[str, Any]:
        """Analyze field completeness in SQLite database"""
        completeness = {}
        
        # Get all column names
        cursor.execute("PRAGMA table_info(careers);")
        columns = [col[1] for col in cursor.fetchall()]
        
        cursor.execute("SELECT COUNT(*) FROM careers;")
        total_records = cursor.fetchone()[0]
        
        for column in columns:
            try:
                cursor.execute(f"SELECT COUNT(*) FROM careers WHERE {column} IS NOT NULL AND {column} != '';")
                non_empty_count = cursor.fetchone()[0]
                completeness[column] = {
                    'non_empty_count': non_empty_count,
                    'completeness_percentage': (non_empty_count / total_records * 100) if total_records > 0 else 0
                }
            except sqlite3.OperationalError:
                completeness[column] = {'error': 'Could not analyze field'}
        
        return completeness

    def _get_sqlite_examples(self, cursor) -> Dict[str, Any]:
        """Get examples of problematic records from SQLite database"""
        examples = {}
        
        # Get examples of placeholder descriptions
        cursor.execute("SELECT id, title, description FROM careers WHERE description LIKE '%brief description%' LIMIT 3;")
        placeholder_examples = cursor.fetchall()
        examples['placeholder_descriptions'] = [
            {'id': row[0], 'title': row[1], 'description': row[2][:100] + '...' if len(row[2]) > 100 else row[2]}
            for row in placeholder_examples
        ]
        
        # Get examples of records with NULL values
        cursor.execute("SELECT id, title, description FROM careers WHERE id IS NULL OR title IS NULL OR description IS NULL LIMIT 3;")
        null_examples = cursor.fetchall()
        examples['null_value_examples'] = [
            {'id': row[0], 'title': row[1], 'description': row[2][:100] + '...' if row[2] and len(row[2]) > 100 else row[2]}
            for row in null_examples
        ]
        
        return examples

    def analyze_json_file(self, file_path: str, source_name: str) -> Dict[str, Any]:
        """Analyze a JSON career data file"""
        print(f"🔍 Analyzing {source_name} ({file_path})...")
        
        file_path = Path(file_path)
        if not file_path.exists():
            return {"error": f"File not found at: {file_path}"}
        
        analysis = {
            'file_exists': True,
            'total_records': 0,
            'data_quality': {},
            'placeholder_analysis': {},
            'field_completeness': {},
            'schema_consistency': {},
            'examples': {}
        }
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Handle different JSON structures
            if isinstance(data, dict) and 'careers' in data:
                careers = data['careers']
                analysis['total_records'] = data.get('total_careers', len(careers))
            elif isinstance(data, list):
                careers = data
                analysis['total_records'] = len(careers)
            else:
                return {"error": "Unexpected JSON structure"}
            
            if careers:
                analysis['data_quality'] = self._analyze_json_data_quality(careers)
                analysis['placeholder_analysis'] = self._analyze_json_placeholders(careers)
                analysis['field_completeness'] = self._analyze_json_field_completeness(careers)
                analysis['schema_consistency'] = self._analyze_json_schema_consistency(careers)
                analysis['examples'] = self._get_json_examples(careers)
            
        except json.JSONDecodeError as e:
            analysis['error'] = f"JSON decode error: {e}"
        except Exception as e:
            analysis['error'] = f"Unexpected error: {e}"
            
        return analysis

    def _analyze_json_data_quality(self, careers: List[Dict]) -> Dict[str, Any]:
        """Analyze data quality issues in JSON data"""
        quality_issues = {}
        
        # Check for missing required fields
        missing_fields = defaultdict(int)
        for career in careers:
            for field in self.required_fields:
                if field not in career or career[field] is None or career[field] == '':
                    missing_fields[field] += 1
        
        quality_issues['missing_required_fields'] = dict(missing_fields)
        
        # Check for duplicate titles
        titles = [career.get('title', '') for career in careers]
        title_counts = Counter(titles)
        duplicates = {title: count for title, count in title_counts.items() if count > 1 and title}
        quality_issues['duplicate_titles'] = len(duplicates)
        quality_issues['duplicate_examples'] = list(duplicates.items())[:5]
        
        # Check for inconsistent data types
        type_inconsistencies = {}
        for field in ['minSalary', 'maxSalary', 'minExperienceYears', 'maxExperienceYears']:
            non_numeric = sum(1 for career in careers if field in career and not isinstance(career[field], (int, float)))
            if non_numeric > 0:
                type_inconsistencies[field] = non_numeric
        
        quality_issues['type_inconsistencies'] = type_inconsistencies
        
        return quality_issues

    def _analyze_json_placeholders(self, careers: List[Dict]) -> Dict[str, Any]:
        """Analyze placeholder patterns in JSON data"""
        placeholder_analysis = {}
        
        # Analyze descriptions for placeholder patterns
        descriptions = [career.get('description', '') for career in careers if career.get('description')]
        
        placeholder_counts = {}
        placeholder_records = []
        
        for i, career in enumerate(careers):
            description = career.get('description', '')
            has_placeholder = False
            
            for pattern in self.placeholder_patterns:
                if re.search(pattern, description, re.IGNORECASE):
                    if pattern not in placeholder_counts:
                        placeholder_counts[pattern] = 0
                    placeholder_counts[pattern] += 1
                    has_placeholder = True
            
            if has_placeholder:
                placeholder_records.append({
                    'index': i,
                    'title': career.get('title', 'Unknown'),
                    'description': description[:100] + '...' if len(description) > 100 else description
                })
        
        placeholder_analysis['description_placeholders'] = placeholder_counts
        placeholder_analysis['total_placeholder_descriptions'] = len(placeholder_records)
        placeholder_analysis['total_descriptions'] = len(descriptions)
        placeholder_analysis['placeholder_percentage'] = (len(placeholder_records) / len(descriptions) * 100) if descriptions else 0
        
        # Analyze technical skills for placeholder patterns
        tech_skills_placeholders = 0
        total_tech_skills = 0
        
        for career in careers:
            tech_skills = career.get('requiredTechnicalSkills', [])
            if isinstance(tech_skills, list):
                total_tech_skills += len(tech_skills)
                for skill in tech_skills:
                    if isinstance(skill, str) and any(re.search(pattern, skill, re.IGNORECASE) for pattern in self.placeholder_patterns):
                        tech_skills_placeholders += 1
        
        placeholder_analysis['technical_skills_placeholders'] = tech_skills_placeholders
        placeholder_analysis['total_technical_skills'] = total_tech_skills
        
        # Check for identical salary ranges (indicating template data)
        salary_ranges = [career.get('salaryRange', '') for career in careers if career.get('salaryRange')]
        salary_counts = Counter(salary_ranges)
        most_common_salary = salary_counts.most_common(1)[0] if salary_counts else ('', 0)
        
        placeholder_analysis['salary_analysis'] = {
            'most_common_salary': most_common_salary[0],
            'most_common_count': most_common_salary[1],
            'unique_salary_ranges': len(salary_counts),
            'total_salary_records': len(salary_ranges)
        }
        
        return placeholder_analysis

    def _analyze_json_field_completeness(self, careers: List[Dict]) -> Dict[str, Any]:
        """Analyze field completeness in JSON data"""
        completeness = {}
        total_records = len(careers)
        
        # Get all unique fields across all records
        all_fields = set()
        for career in careers:
            all_fields.update(career.keys())
        
        for field in all_fields:
            non_empty_count = 0
            for career in careers:
                value = career.get(field)
                if value is not None and value != '' and value != []:
                    non_empty_count += 1
            
            completeness[field] = {
                'non_empty_count': non_empty_count,
                'completeness_percentage': (non_empty_count / total_records * 100) if total_records > 0 else 0,
                'is_required': field in self.required_fields
            }
        
        return completeness

    def _analyze_json_schema_consistency(self, careers: List[Dict]) -> Dict[str, Any]:
        """Analyze schema consistency across JSON records"""
        consistency = {}
        
        # Check field presence consistency
        all_fields = set()
        for career in careers:
            all_fields.update(career.keys())
        
        field_presence = {}
        for field in all_fields:
            present_count = sum(1 for career in careers if field in career)
            field_presence[field] = {
                'present_in_records': present_count,
                'presence_percentage': (present_count / len(careers) * 100) if careers else 0
            }
        
        consistency['field_presence'] = field_presence
        
        # Check data type consistency
        type_consistency = {}
        for field in all_fields:
            types_found = set()
            for career in careers:
                if field in career and career[field] is not None:
                    types_found.add(type(career[field]).__name__)
            
            type_consistency[field] = {
                'types_found': list(types_found),
                'is_consistent': len(types_found) <= 1
            }
        
        consistency['type_consistency'] = type_consistency
        
        return consistency

    def _get_json_examples(self, careers: List[Dict]) -> Dict[str, Any]:
        """Get examples of problematic records from JSON data"""
        examples = {}
        
        # Get examples of placeholder records
        placeholder_examples = []
        for i, career in enumerate(careers[:10]):  # Check first 10 records
            description = career.get('description', '')
            if any(re.search(pattern, description, re.IGNORECASE) for pattern in self.placeholder_patterns):
                placeholder_examples.append({
                    'index': i,
                    'title': career.get('title', 'Unknown'),
                    'description': description[:150] + '...' if len(description) > 150 else description,
                    'technical_skills': career.get('requiredTechnicalSkills', [])[:3]  # First 3 skills
                })
        
        examples['placeholder_examples'] = placeholder_examples[:3]  # Top 3 examples
        
        # Get examples of incomplete records
        incomplete_examples = []
        for i, career in enumerate(careers):
            missing_fields = [field for field in self.required_fields if field not in career or not career[field]]
            if missing_fields:
                incomplete_examples.append({
                    'index': i,
                    'title': career.get('title', 'Unknown'),
                    'missing_fields': missing_fields
                })
        
        examples['incomplete_examples'] = incomplete_examples[:3]  # Top 3 examples
        
        return examples

    def calculate_data_quality_score(self, analysis: Dict[str, Any]) -> float:
        """Calculate overall data quality score (0-100)"""
        if 'error' in analysis:
            return 0.0
        
        score = 100.0
        
        # Deduct points for placeholder content
        if 'placeholder_analysis' in analysis:
            placeholder_data = analysis['placeholder_analysis']
            if 'placeholder_percentage' in placeholder_data:
                score -= placeholder_data['placeholder_percentage'] * 0.8  # Heavy penalty for placeholders
        
        # Deduct points for missing required fields
        if 'field_completeness' in analysis:
            completeness_data = analysis['field_completeness']
            required_field_penalties = 0
            required_field_count = 0
            
            for field, data in completeness_data.items():
                if isinstance(data, dict) and data.get('is_required', False):
                    required_field_count += 1
                    completeness_pct = data.get('completeness_percentage', 0)
                    required_field_penalties += (100 - completeness_pct) * 0.1
            
            if required_field_count > 0:
                score -= required_field_penalties / required_field_count
        
        # Deduct points for data quality issues
        if 'data_quality' in analysis:
            quality_data = analysis['data_quality']
            if 'null_primary_keys' in quality_data and quality_data['null_primary_keys'] > 0:
                score -= 20  # Major penalty for NULL primary keys
            
            if 'duplicate_titles' in quality_data:
                score -= min(quality_data['duplicate_titles'] * 2, 15)  # Penalty for duplicates
        
        return max(0.0, min(100.0, score))

    def generate_recommendations(self) -> List[str]:
        """Generate recommendations based on analysis results"""
        recommendations = []
        
        # Analyze results and generate specific recommendations
        for source, analysis in self.results.items():
            if source == 'summary' or source == 'recommendations' or 'error' in analysis:
                continue
            
            source_name = source.replace('_', ' ').title()
            
            # Check for placeholder content
            if 'placeholder_analysis' in analysis:
                placeholder_data = analysis['placeholder_analysis']
                if placeholder_data.get('placeholder_percentage', 0) > 50:
                    recommendations.append(f"🚨 HIGH PRIORITY: {source_name} contains {placeholder_data.get('placeholder_percentage', 0):.1f}% placeholder content - requires immediate data replacement")
                elif placeholder_data.get('placeholder_percentage', 0) > 10:
                    recommendations.append(f"⚠️ MEDIUM PRIORITY: {source_name} contains {placeholder_data.get('placeholder_percentage', 0):.1f}% placeholder content - needs data cleanup")
            
            # Check for missing required fields
            if 'field_completeness' in analysis:
                completeness_data = analysis['field_completeness']
                critical_missing = []
                for field, data in completeness_data.items():
                    if isinstance(data, dict) and data.get('is_required', False) and data.get('completeness_percentage', 100) < 90:
                        critical_missing.append(f"{field} ({data.get('completeness_percentage', 0):.1f}% complete)")
                
                if critical_missing:
                    recommendations.append(f"📋 REQUIRED FIELDS: {source_name} missing critical data in: {', '.join(critical_missing)}")
            
            # Check for data quality issues
            if 'data_quality' in analysis:
                quality_data = analysis['data_quality']
                if quality_data.get('null_primary_keys', 0) > 0:
                    recommendations.append(f"🔑 CRITICAL: {source_name} has {quality_data['null_primary_keys']} records with NULL primary keys - database corruption detected")
        
        # Add general recommendations
        recommendations.extend([
            "🎯 STRATEGY: Use production_career_data.json as the primary data source (highest quality)",
            "🔄 MIGRATION: Replace careers.db content with cleaned production data",
            "🗑️ CLEANUP: Remove or replace new_career_data.json placeholder records",
            "✅ VALIDATION: Implement data validation rules to prevent future placeholder content",
            "📊 MONITORING: Set up automated data quality checks for ongoing maintenance"
        ])
        
        return recommendations

    def run_comprehensive_analysis(self) -> Dict[str, Any]:
        """Run comprehensive analysis on all data sources"""
        print("🚀 Starting Comprehensive Career Data Quality Analysis")
        print("=" * 60)
        
        # Analyze SQLite database
        self.results['sqlite_db'] = self.analyze_sqlite_database()
        
        # Analyze JSON files
        self.results['new_career_data'] = self.analyze_json_file('new_career_data.json', 'New Career Data')
        self.results['production_career_data'] = self.analyze_json_file('production_career_data.json', 'Production Career Data')
        
        # Calculate quality scores
        scores = {}
        for source, analysis in self.results.items():
            if source not in ['summary', 'recommendations']:
                scores[source] = self.calculate_data_quality_score(analysis)
        
        # Generate summary
        self.results['summary'] = {
            'analysis_timestamp': datetime.now().isoformat(),
            'data_sources_analyzed': len([k for k in self.results.keys() if k not in ['summary', 'recommendations']]),
            'quality_scores': scores,
            'overall_assessment': self._generate_overall_assessment(scores)
        }
        
        # Generate recommendations
        self.results['recommendations'] = self.generate_recommendations()
        
        return self.results

    def _generate_overall_assessment(self, scores: Dict[str, float]) -> str:
        """Generate overall assessment based on quality scores"""
        if not scores:
            return "No data sources could be analyzed"
        
        avg_score = sum(scores.values()) / len(scores)
        
        if avg_score >= 80:
            return "GOOD - Most data sources have acceptable quality"
        elif avg_score >= 60:
            return "FAIR - Significant data quality issues need attention"
        elif avg_score >= 40:
            return "POOR - Major data quality problems require immediate action"
        else:
            return "CRITICAL - Severe data quality issues, extensive cleanup required"

    def print_detailed_report(self):
        """Print a detailed, formatted report"""
        print("\n" + "="*80)
        print("📊 COMPREHENSIVE CAREER DATA QUALITY ANALYSIS REPORT")
        print("="*80)
        
        # Print summary
        if 'summary' in self.results:
            summary = self.results['summary']
            print(f"\n🕒 Analysis Timestamp: {summary.get('analysis_timestamp', 'Unknown')}")
            print(f"📁 Data Sources Analyzed: {summary.get('data_sources_analyzed', 0)}")
            print(f"🎯 Overall Assessment: {summary.get('overall_assessment', 'Unknown')}")
            
            print(f"\n📈 QUALITY SCORES:")
            for source, score in summary.get('quality_scores', {}).items():
                status = "🟢" if score >= 80 else "🟡" if score >= 60 else "🔴"
                print(f"   {status} {source.replace('_', ' ').title()}: {score:.1f}/100")
        
        # Print detailed analysis for each source
        for source, analysis in self.results.items():
            if source in ['summary', 'recommendations']:
                continue
                
            source_name = source.replace('_', ' ').title()
            print(f"\n" + "─"*60)
            print(f"📋 {source_name.upper()} ANALYSIS")
            print("─"*60)
            
            if 'error' in analysis:
                print(f"❌ Error: {analysis['error']}")
                continue
            
            print(f"📊 Total Records: {analysis.get('total_records', 0)}")
            
            # Print placeholder analysis
            if 'placeholder_analysis' in analysis:
                placeholder_data = analysis['placeholder_analysis']
                print(f"\n🎭 PLACEHOLDER CONTENT:")
                print(f"   • Placeholder Descriptions: {placeholder_data.get('total_placeholder_descriptions', 0)}/{placeholder_data.get('total_descriptions', 0)} ({placeholder_data.get('placeholder_percentage', 0):.1f}%)")
                
                if 'description_placeholders' in placeholder_data:
                    for pattern, count in placeholder_data['description_placeholders'].items():
                        print(f"     - '{pattern}': {count} occurrences")
            
            # Print field completeness
            if 'field_completeness' in analysis:
                print(f"\n📋 FIELD COMPLETENESS:")
                completeness_data = analysis['field_completeness']
                
                # Show required fields first
                required_fields = {k: v for k, v in completeness_data.items() if isinstance(v, dict) and v.get('is_required', False)}
                if required_fields:
                    print("   Required Fields:")
                    for field, data in sorted(required_fields.items(), key=lambda x: x[1].get('completeness_percentage', 0)):
                        pct = data.get('completeness_percentage', 0)
                        status = "✅" if pct >= 95 else "⚠️" if pct >= 80 else "❌"
                        print(f"     {status} {field}: {pct:.1f}% complete")
            
            # Print examples
            if 'examples' in analysis and analysis['examples']:
                print(f"\n🔍 EXAMPLES OF ISSUES:")
                examples = analysis['examples']
                
                if 'placeholder_examples' in examples and examples['placeholder_examples']:
                    print("   Placeholder Content Examples:")
                    for i, example in enumerate(examples['placeholder_examples'][:2], 1):
                        print(f"     {i}. {example.get('title', 'Unknown')}")
                        print(f"        Description: {example.get('description', 'N/A')}")
        
        # Print recommendations
        if 'recommendations' in self.results:
            print(f"\n" + "="*60)
            print("💡 RECOMMENDATIONS")
            print("="*60)
            
            for i, recommendation in enumerate(self.results['recommendations'], 1):
                print(f"{i:2d}. {recommendation}")
        
        print(f"\n" + "="*80)
        print("📋 ANALYSIS COMPLETE")
        print("="*80)

    def save_report_to_file(self, filename: str = "data_quality_report.json"):
        """Save the complete analysis results to a JSON file"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
        print(f"📄 Report saved to: {filename}")


def main():
    """Main function to run the analysis"""
    analyzer = CareerDataQualityAnalyzer()
    
    # Run comprehensive analysis
    results = analyzer.run_comprehensive_analysis()
    
    # Print detailed report
    analyzer.print_detailed_report()
    
    # Save report to file
    analyzer.save_report_to_file()
    
    return results


if __name__ == "__main__":
    main()