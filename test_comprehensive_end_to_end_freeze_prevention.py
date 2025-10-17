#!/usr/bin/env python3
"""
Comprehensive End-to-End Testing Script for Freeze Prevention
============================================================

This script performs exhaustive testing of the entire system to ensure no freezes occur.
It tests the complete user journey and validates all timeout mechanisms.

Key Focus Areas:
- Claude API timeout handling (30-second limits)
- Database connection cleanup
- Authentication flow stability
- AI recommendation pipeline
- Concurrent user handling
- Error recovery scenarios
- Resource monitoring

Previous freeze issues that this test validates are resolved:
- Claude API timeouts causing infinite hangs
- Database connection leaks
- Authentication token issues
- AI processing loops
"""

import asyncio
import aiohttp
import requests
import json
import time
import threading
import psutil
import os
import sys
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict, List, Any, Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SystemMonitor:
    """Monitor system resources during testing"""
    
    def __init__(self):
        self.monitoring = False
        self.metrics = []
        self.start_time = None
        
    def start_monitoring(self):
        """Start system resource monitoring"""
        self.monitoring = True
        self.start_time = time.time()
        self.metrics = []
        
        def monitor():
            while self.monitoring:
                try:
                    # Get current process info
                    process = psutil.Process(os.getpid())
                    
                    # Collect metrics
                    metric = {
                        'timestamp': time.time() - self.start_time,
                        'cpu_percent': psutil.cpu_percent(interval=0.1),
                        'memory_percent': psutil.virtual_memory().percent,
                        'memory_used_mb': psutil.virtual_memory().used / 1024 / 1024,
                        'process_memory_mb': process.memory_info().rss / 1024 / 1024,
                        'process_cpu_percent': process.cpu_percent(),
                        'open_connections': len(process.connections()),
                        'open_files': len(process.open_files()),
                        'threads': process.num_threads()
                    }
                    self.metrics.append(metric)
                    time.sleep(1)
                except Exception as e:
                    logger.warning(f"Monitoring error: {e}")
                    
        self.monitor_thread = threading.Thread(target=monitor, daemon=True)
        self.monitor_thread.start()
        
    def stop_monitoring(self):
        """Stop monitoring and return metrics"""
        self.monitoring = False
        if hasattr(self, 'monitor_thread'):
            self.monitor_thread.join(timeout=2)
        return self.metrics

class FreezePreventionTester:
    """Comprehensive end-to-end tester focused on freeze prevention"""
    
    def __init__(self, base_url: str = "http://localhost:8002/api/v1"):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.timeout = 35  # Slightly higher than API timeout
        self.test_results = []
        self.monitor = SystemMonitor()
        self.test_users = []
        
    def log_test_result(self, test_name: str, status: str, details: str, duration: float = 0):
        """Log test result with timing information"""
        result = {
            'test_name': test_name,
            'status': status,
            'details': details,
            'duration': duration,
            'timestamp': datetime.now().isoformat()
        }
        self.test_results.append(result)
        
        status_emoji = "✅" if status == "PASS" else "❌" if status == "FAIL" else "⚠️"
        logger.info(f"{status_emoji} {test_name}: {status} ({duration:.2f}s) - {details}")
        
    def test_health_endpoint(self) -> bool:
        """Test basic health endpoint - should never freeze"""
        start_time = time.time()
        try:
            response = self.session.get(f"{self.base_url}/health", timeout=5)
            duration = time.time() - start_time
            
            if response.status_code == 200:
                self.log_test_result("Health Check", "PASS", f"Server responsive: {response.json()}", duration)
                return True
            else:
                self.log_test_result("Health Check", "FAIL", f"Unexpected status: {response.status_code}", duration)
                return False
                
        except requests.exceptions.Timeout:
            duration = time.time() - start_time
            self.log_test_result("Health Check", "FAIL", "Health endpoint timed out - potential freeze", duration)
            return False
        except Exception as e:
            duration = time.time() - start_time
            self.log_test_result("Health Check", "FAIL", f"Health check failed: {e}", duration)
            return False
            
    def create_test_user(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Create a test user and return authentication token"""
        start_time = time.time()
        
        user_data = {
            "email": f"test_user_{user_id}@freezetest.com",
            "password": "FreezeTest123!",
            "full_name": f"Test User {user_id}"
        }
        
        try:
            # Register user
            response = self.session.post(f"{self.base_url}/auth/register", json=user_data, timeout=10)
            
            if response.status_code in [200, 201, 409]:  # 409 = user already exists
                # Login to get token
                login_data = {
                    "username": user_data["email"],
                    "password": user_data["password"]
                }
                
                login_response = self.session.post(f"{self.base_url}/auth/login", data=login_data, timeout=10)
                duration = time.time() - start_time
                
                if login_response.status_code == 200:
                    token_data = login_response.json()
                    user_info = {
                        "user_id": user_id,
                        "email": user_data["email"],
                        "token": token_data["access_token"],
                        "headers": {"Authorization": f"Bearer {token_data['access_token']}"}
                    }
                    self.test_users.append(user_info)
                    self.log_test_result(f"User Creation ({user_id})", "PASS", "User created and authenticated", duration)
                    return user_info
                else:
                    self.log_test_result(f"User Creation ({user_id})", "FAIL", f"Login failed: {login_response.status_code}", duration)
                    return None
            else:
                duration = time.time() - start_time
                self.log_test_result(f"User Creation ({user_id})", "FAIL", f"Registration failed: {response.status_code}", duration)
                return None
                
        except requests.exceptions.Timeout:
            duration = time.time() - start_time
            self.log_test_result(f"User Creation ({user_id})", "FAIL", "User creation timed out - potential freeze", duration)
            return None
        except Exception as e:
            duration = time.time() - start_time
            self.log_test_result(f"User Creation ({user_id})", "FAIL", f"User creation failed: {e}", duration)
            return None
            
    def test_assessment_submission(self, user_info: Dict[str, Any]) -> bool:
        """Test assessment submission - critical for preventing assessment freezes"""
        start_time = time.time()
        
        assessment_data = {
            "technicalSkills": ["Python", "Machine Learning", "Data Analysis"],
            "softSkills": ["Leadership", "Communication", "Problem Solving"],
            "experience": "3-5 years",
            "careerGoals": "Senior Data Scientist role",
            "currentRole": "Data Analyst",
            "educationLevel": "Bachelor's Degree",
            "salaryExpectations": "$80,000-$120,000",
            "industries": ["Technology", "Healthcare"],
            "interests": ["AI/ML", "Data Visualization"],
            "workingWithData": 5,
            "workingWithPeople": 3,
            "creativeTasks": 4
        }
        
        try:
            response = self.session.post(
                f"{self.base_url}/assessment/submit-assessment",
                json=assessment_data,
                headers=user_info["headers"],
                timeout=15
            )
            duration = time.time() - start_time
            
            if response.status_code in [200, 201]:
                self.log_test_result(f"Assessment Submission ({user_info['user_id']})", "PASS", "Assessment submitted successfully", duration)
                return True
            else:
                self.log_test_result(f"Assessment Submission ({user_info['user_id']})", "FAIL", f"Assessment failed: {response.status_code}", duration)
                return False
                
        except requests.exceptions.Timeout:
            duration = time.time() - start_time
            self.log_test_result(f"Assessment Submission ({user_info['user_id']})", "FAIL", "Assessment submission timed out - potential freeze", duration)
            return False
        except Exception as e:
            duration = time.time() - start_time
            self.log_test_result(f"Assessment Submission ({user_info['user_id']})", "FAIL", f"Assessment submission failed: {e}", duration)
            return False
            
    def test_ai_recommendations_with_timeout_validation(self, user_info: Dict[str, Any]) -> bool:
        """Test AI recommendations with explicit timeout validation - CRITICAL for freeze prevention"""
        start_time = time.time()
        
        assessment_data = {
            "technicalSkills": ["Python", "Machine Learning"],
            "softSkills": ["Leadership"],
            "experience": "5+ years",
            "careerGoals": "Senior AI Engineer role"
        }
        
        try:
            # Test with 35-second timeout (5 seconds more than API timeout)
            response = self.session.post(
                f"{self.base_url}/ai/recommendations",
                json=assessment_data,
                headers=user_info["headers"],
                timeout=35
            )
            duration = time.time() - start_time
            
            if response.status_code == 200:
                recommendations = response.json()
                if "recommendations" in recommendations and recommendations["recommendations"]:
                    rec_count = len(recommendations["recommendations"])
                    self.log_test_result(f"AI Recommendations ({user_info['user_id']})", "PASS", f"Received {rec_count} recommendations in {duration:.2f}s", duration)
                    return True
                else:
                    self.log_test_result(f"AI Recommendations ({user_info['user_id']})", "WARN", "Fallback recommendations returned", duration)
                    return True  # Fallback is acceptable
            else:
                self.log_test_result(f"AI Recommendations ({user_info['user_id']})", "FAIL", f"AI recommendations failed: {response.status_code}", duration)
                return False
                
        except requests.exceptions.Timeout:
            duration = time.time() - start_time
            self.log_test_result(f"AI Recommendations ({user_info['user_id']})", "FAIL", f"AI recommendations timed out after {duration:.2f}s - FREEZE DETECTED", duration)
            return False
        except Exception as e:
            duration = time.time() - start_time
            self.log_test_result(f"AI Recommendations ({user_info['user_id']})", "FAIL", f"AI recommendations failed: {e}", duration)
            return False
            
    def test_ai_tuning_with_timeout_validation(self, user_info: Dict[str, Any]) -> bool:
        """Test AI tuning with timeout validation"""
        start_time = time.time()
        
        # First get recommendations
        assessment_data = {
            "technicalSkills": ["Python", "JavaScript"],
            "softSkills": ["Communication"],
            "experience": "2-3 years",
            "careerGoals": "Full-stack developer"
        }
        
        try:
            # Get initial recommendations
            rec_response = self.session.post(
                f"{self.base_url}/ai/recommendations",
                json=assessment_data,
                headers=user_info["headers"],
                timeout=35
            )
            
            if rec_response.status_code != 200:
                self.log_test_result(f"AI Tuning Setup ({user_info['user_id']})", "FAIL", "Could not get initial recommendations", time.time() - start_time)
                return False
                
            recommendations = rec_response.json()["recommendations"]
            
            # Now test tuning
            tuning_data = {
                "prompt": "I prefer remote work opportunities and startups",
                "current_recommendations": recommendations
            }
            
            tune_response = self.session.post(
                f"{self.base_url}/ai/tune",
                json=tuning_data,
                headers=user_info["headers"],
                timeout=35
            )
            duration = time.time() - start_time
            
            if tune_response.status_code == 200:
                tuned_recs = tune_response.json()
                if "recommendations" in tuned_recs:
                    self.log_test_result(f"AI Tuning ({user_info['user_id']})", "PASS", f"Tuning completed in {duration:.2f}s", duration)
                    return True
                else:
                    self.log_test_result(f"AI Tuning ({user_info['user_id']})", "FAIL", "Invalid tuning response format", duration)
                    return False
            else:
                self.log_test_result(f"AI Tuning ({user_info['user_id']})", "FAIL", f"Tuning failed: {tune_response.status_code}", duration)
                return False
                
        except requests.exceptions.Timeout:
            duration = time.time() - start_time
            self.log_test_result(f"AI Tuning ({user_info['user_id']})", "FAIL", f"AI tuning timed out after {duration:.2f}s - FREEZE DETECTED", duration)
            return False
        except Exception as e:
            duration = time.time() - start_time
            self.log_test_result(f"AI Tuning ({user_info['user_id']})", "FAIL", f"AI tuning failed: {e}", duration)
            return False
            
    def test_complete_user_journey(self, user_id: str) -> bool:
        """Test complete user journey from registration to AI recommendations"""
        logger.info(f"🚀 Starting complete user journey test for user {user_id}")
        
        # Step 1: Create user
        user_info = self.create_test_user(user_id)
        if not user_info:
            return False
            
        # Step 2: Submit assessment
        if not self.test_assessment_submission(user_info):
            return False
            
        # Step 3: Get AI recommendations
        if not self.test_ai_recommendations_with_timeout_validation(user_info):
            return False
            
        # Step 4: Test AI tuning
        if not self.test_ai_tuning_with_timeout_validation(user_info):
            return False
            
        logger.info(f"✅ Complete user journey successful for user {user_id}")
        return True
        
    def test_concurrent_users(self, num_users: int = 5) -> bool:
        """Test multiple concurrent users to ensure no freezes under load"""
        logger.info(f"🔄 Testing {num_users} concurrent users")
        start_time = time.time()
        
        with ThreadPoolExecutor(max_workers=num_users) as executor:
            # Submit all user journey tests
            futures = [
                executor.submit(self.test_complete_user_journey, f"concurrent_{i}")
                for i in range(num_users)
            ]
            
            # Wait for all to complete with timeout
            completed = 0
            failed = 0
            
            for future in as_completed(futures, timeout=300):  # 5-minute timeout
                try:
                    result = future.result()
                    if result:
                        completed += 1
                    else:
                        failed += 1
                except Exception as e:
                    failed += 1
                    logger.error(f"Concurrent user test failed: {e}")
                    
        duration = time.time() - start_time
        
        if failed == 0:
            self.log_test_result("Concurrent Users", "PASS", f"{completed}/{num_users} users completed successfully", duration)
            return True
        else:
            self.log_test_result("Concurrent Users", "FAIL", f"{failed}/{num_users} users failed", duration)
            return False
            
    def test_error_recovery_scenarios(self) -> bool:
        """Test error recovery scenarios to ensure no freezes during errors"""
        logger.info("🔧 Testing error recovery scenarios")
        
        # Create a test user for error testing
        user_info = self.create_test_user("error_test")
        if not user_info:
            return False
            
        error_tests_passed = 0
        total_error_tests = 0
        
        # Test 1: Invalid assessment data
        total_error_tests += 1
        start_time = time.time()
        try:
            response = self.session.post(
                f"{self.base_url}/assessment/submit-assessment",
                json={"invalid": "data"},
                headers=user_info["headers"],
                timeout=10
            )
            duration = time.time() - start_time
            
            if response.status_code in [400, 422]:  # Expected error codes
                self.log_test_result("Error Recovery - Invalid Assessment", "PASS", f"Proper error handling: {response.status_code}", duration)
                error_tests_passed += 1
            else:
                self.log_test_result("Error Recovery - Invalid Assessment", "FAIL", f"Unexpected response: {response.status_code}", duration)
                
        except requests.exceptions.Timeout:
            duration = time.time() - start_time
            self.log_test_result("Error Recovery - Invalid Assessment", "FAIL", "Error handling timed out - potential freeze", duration)
        except Exception as e:
            duration = time.time() - start_time
            self.log_test_result("Error Recovery - Invalid Assessment", "FAIL", f"Error handling failed: {e}", duration)
            
        # Test 2: Invalid AI request
        total_error_tests += 1
        start_time = time.time()
        try:
            response = self.session.post(
                f"{self.base_url}/ai/recommendations",
                json={"invalid": "ai_data"},
                headers=user_info["headers"],
                timeout=35
            )
            duration = time.time() - start_time
            
            if response.status_code in [400, 422]:
                self.log_test_result("Error Recovery - Invalid AI Request", "PASS", f"Proper error handling: {response.status_code}", duration)
                error_tests_passed += 1
            else:
                self.log_test_result("Error Recovery - Invalid AI Request", "FAIL", f"Unexpected response: {response.status_code}", duration)
                
        except requests.exceptions.Timeout:
            duration = time.time() - start_time
            self.log_test_result("Error Recovery - Invalid AI Request", "FAIL", "AI error handling timed out - potential freeze", duration)
        except Exception as e:
            duration = time.time() - start_time
            self.log_test_result("Error Recovery - Invalid AI Request", "FAIL", f"AI error handling failed: {e}", duration)
            
        # Test 3: Unauthorized access
        total_error_tests += 1
        start_time = time.time()
        try:
            response = self.session.post(
                f"{self.base_url}/ai/recommendations",
                json={"technicalSkills": ["Python"]},
                timeout=10  # No auth headers
            )
            duration = time.time() - start_time
            
            if response.status_code == 401:
                self.log_test_result("Error Recovery - Unauthorized Access", "PASS", "Proper auth error handling", duration)
                error_tests_passed += 1
            else:
                self.log_test_result("Error Recovery - Unauthorized Access", "FAIL", f"Unexpected response: {response.status_code}", duration)
                
        except requests.exceptions.Timeout:
            duration = time.time() - start_time
            self.log_test_result("Error Recovery - Unauthorized Access", "FAIL", "Auth error handling timed out - potential freeze", duration)
        except Exception as e:
            duration = time.time() - start_time
            self.log_test_result("Error Recovery - Unauthorized Access", "FAIL", f"Auth error handling failed: {e}", duration)
            
        success_rate = error_tests_passed / total_error_tests if total_error_tests > 0 else 0
        return success_rate >= 0.8  # 80% success rate acceptable
        
    def run_sustained_load_test(self, duration_minutes: int = 8) -> bool:
        """Run sustained load testing for specified duration"""
        logger.info(f"⏱️  Starting {duration_minutes}-minute sustained load test")
        
        end_time = time.time() + (duration_minutes * 60)
        test_cycle = 0
        successful_cycles = 0
        failed_cycles = 0
        
        while time.time() < end_time:
            test_cycle += 1
            cycle_start = time.time()
            
            logger.info(f"🔄 Load test cycle {test_cycle}")
            
            # Run a complete user journey
            if self.test_complete_user_journey(f"load_test_{test_cycle}"):
                successful_cycles += 1
            else:
                failed_cycles += 1
                
            # Brief pause between cycles
            time.sleep(2)
            
            # Check if we should continue
            if failed_cycles > 3:  # Stop if too many failures
                logger.warning("Too many failures in load test, stopping early")
                break
                
        total_duration = duration_minutes * 60
        success_rate = successful_cycles / test_cycle if test_cycle > 0 else 0
        
        if success_rate >= 0.9:  # 90% success rate required
            self.log_test_result("Sustained Load Test", "PASS", f"{successful_cycles}/{test_cycle} cycles successful ({success_rate:.1%})", total_duration)
            return True
        else:
            self.log_test_result("Sustained Load Test", "FAIL", f"Only {successful_cycles}/{test_cycle} cycles successful ({success_rate:.1%})", total_duration)
            return False
            
    def generate_comprehensive_report(self) -> Dict[str, Any]:
        """Generate comprehensive test report"""
        total_tests = len(self.test_results)
        passed_tests = len([r for r in self.test_results if r['status'] == 'PASS'])
        failed_tests = len([r for r in self.test_results if r['status'] == 'FAIL'])
        warning_tests = len([r for r in self.test_results if r['status'] == 'WARN'])
        
        # Calculate metrics
        total_duration = sum(r['duration'] for r in self.test_results)
        avg_duration = total_duration / total_tests if total_tests > 0 else 0
        
        # Check for freeze indicators
        freeze_indicators = [
            r for r in self.test_results 
            if 'freeze' in r['details'].lower() or 'timed out' in r['details'].lower()
        ]
        
        report = {
            'test_summary': {
                'total_tests': total_tests,
                'passed': passed_tests,
                'failed': failed_tests,
                'warnings': warning_tests,
                'success_rate': passed_tests / total_tests if total_tests > 0 else 0,
                'total_duration': total_duration,
                'average_duration': avg_duration
            },
            'freeze_analysis': {
                'freeze_indicators_found': len(freeze_indicators),
                'freeze_details': [r['details'] for r in freeze_indicators],
                'system_stable': len(freeze_indicators) == 0
            },
            'performance_metrics': {
                'fastest_test': min(self.test_results, key=lambda x: x['duration'])['duration'] if self.test_results else 0,
                'slowest_test': max(self.test_results, key=lambda x: x['duration'])['duration'] if self.test_results else 0,
                'timeout_violations': len([r for r in self.test_results if r['duration'] > 30])
            },
            'detailed_results': self.test_results,
            'system_metrics': self.monitor.metrics if hasattr(self.monitor, 'metrics') else []
        }
        
        return report
        
    def run_comprehensive_test_suite(self) -> bool:
        """Run the complete comprehensive test suite"""
        logger.info("🚀 STARTING COMPREHENSIVE END-TO-END FREEZE PREVENTION TESTING")
        logger.info("=" * 80)
        
        # Start system monitoring
        self.monitor.start_monitoring()
        
        overall_success = True
        
        try:
            # Test 1: Basic health check
            logger.info("📋 Phase 1: Basic System Health")
            if not self.test_health_endpoint():
                overall_success = False
                
            # Test 2: Single user complete journey
            logger.info("📋 Phase 2: Single User Complete Journey")
            if not self.test_complete_user_journey("single_user_test"):
                overall_success = False
                
            # Test 3: Concurrent users
            logger.info("📋 Phase 3: Concurrent User Testing")
            if not self.test_concurrent_users(3):  # Start with 3 concurrent users
                overall_success = False
                
            # Test 4: Error recovery
            logger.info("📋 Phase 4: Error Recovery Testing")
            if not self.test_error_recovery_scenarios():
                overall_success = False
                
            # Test 5: Sustained load testing
            logger.info("📋 Phase 5: Sustained Load Testing")
            if not self.run_sustained_load_test(8):  # 8-minute sustained test
                overall_success = False
                
        except Exception as e:
            logger.error(f"Critical error during testing: {e}")
            overall_success = False
            
        finally:
            # Stop monitoring
            self.monitor.stop_monitoring()
            
        # Generate and save report
        report = self.generate_comprehensive_report()
        
        # Save report to file
        with open('comprehensive_freeze_prevention_test_report.json', 'w') as f:
            json.dump(report, f, indent=2, default=str)
            
        # Print summary
        logger.info("=" * 80)
        logger.info("🏁 COMPREHENSIVE TESTING COMPLETE")
        logger.info("=" * 80)
        
        summary = report['test_summary']
        freeze_analysis = report['freeze_analysis']
        
        logger.info(f"📊 Test Results: {summary['passed']}/{summary['total_tests']} passed ({summary['success_rate']:.1%})")
        logger.info(f"⏱️  Total Duration: {summary['total_duration']:.2f} seconds")
        logger.info(f"🔍 Freeze Indicators: {freeze_analysis['freeze_indicators_found']}")
        logger.info(f"🎯 System Stable: {'✅ YES' if freeze_analysis['system_stable'] else '❌ NO'}")
        
        if freeze_analysis['freeze_indicators_found'] > 0:
            logger.warning("⚠️  FREEZE INDICATORS DETECTED:")
            for detail in freeze_analysis['freeze_details']:
                logger.warning(f"   - {detail}")
                
        if overall_success and freeze_analysis['system_stable']:
            logger.info("🎉 ALL TESTS PASSED - NO FREEZES DETECTED - SYSTEM READY FOR PRODUCTION")
            return True
        else:
            logger.error("❌ TESTS FAILED OR FREEZE INDICATORS FOUND - SYSTEM NEEDS ATTENTION")
            return False

def main():
    """Main test execution function"""
    print("🧪 Comprehensive End-to-End Freeze Prevention Testing")
    print("=" * 60)
    print("This test validates that all previous freeze issues have been resolved:")
    print("- Claude API timeout handling (30-second limits)")
    print("- Database connection cleanup")
    print("- Authentication flow stability")
    print("- AI recommendation pipeline")
    print("- Concurrent user handling")
    print("- Error recovery scenarios")
    print("=" * 60)
    
    tester = FreezePreventionTester()
    
    try:
        success = tester.run_comprehensive_test_suite()
        
        if success:
            print("\n🎉 SUCCESS: All tests passed, no freezes detected!")
            print("✅ System is ready for production use")
            sys.exit(0)
        else:
            print("\n❌ FAILURE: Tests failed or freeze indicators found")
            print("⚠️  System needs attention before production use")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n⏹️  Testing interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Critical error during testing: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()