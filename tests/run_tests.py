"""
Test runner for the recommendation engine test suite.

This script runs all tests (unit, integration, golden datasets, performance)
and provides a comprehensive test report.
"""

import unittest
import sys
import os
import time
from io import StringIO

# Add the project root to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))


class TestResult:
    """Container for test results."""
    
    def __init__(self, name: str):
        self.name = name
        self.tests_run = 0
        self.failures = 0
        self.errors = 0
        self.skipped = 0
        self.success_rate = 0.0
        self.execution_time = 0.0
        self.details = []


class RecommendationEngineTestRunner:
    """Comprehensive test runner for the recommendation engine."""
    
    def __init__(self):
        self.results = []
        self.total_start_time = None
        self.total_end_time = None
    
    def run_test_suite(self, test_module_path: str, suite_name: str) -> TestResult:
        """Run a specific test suite and return results."""
        print(f"\n{'='*60}")
        print(f"Running {suite_name}")
        print(f"{'='*60}")
        
        # Capture test output
        test_output = StringIO()
        
        # Discover and run tests
        start_time = time.time()
        
        try:
            # Load the test module
            loader = unittest.TestLoader()
            suite = loader.discover(test_module_path, pattern='test_*.py')
            
            # Run tests with custom result handler
            runner = unittest.TextTestRunner(
                stream=test_output,
                verbosity=2,
                buffer=True
            )
            
            test_result = runner.run(suite)
            
        except Exception as e:
            print(f"Error running {suite_name}: {e}")
            result = TestResult(suite_name)
            result.details.append(f"Error: {e}")
            return result
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        # Create result summary
        result = TestResult(suite_name)
        result.tests_run = test_result.testsRun
        result.failures = len(test_result.failures)
        result.errors = len(test_result.errors)
        result.skipped = len(test_result.skipped)
        result.execution_time = execution_time
        
        # Calculate success rate
        if result.tests_run > 0:
            successful_tests = result.tests_run - result.failures - result.errors
            result.success_rate = (successful_tests / result.tests_run) * 100
        
        # Capture details
        output_content = test_output.getvalue()
        result.details.append(output_content)
        
        # Add failure details
        if test_result.failures:
            result.details.append("FAILURES:")
            for test, traceback in test_result.failures:
                result.details.append(f"  {test}: {traceback}")
        
        if test_result.errors:
            result.details.append("ERRORS:")
            for test, traceback in test_result.errors:
                result.details.append(f"  {test}: {traceback}")
        
        # Print summary
        print(f"\n{suite_name} Results:")
        print(f"  Tests run: {result.tests_run}")
        print(f"  Failures: {result.failures}")
        print(f"  Errors: {result.errors}")
        print(f"  Skipped: {result.skipped}")
        print(f"  Success rate: {result.success_rate:.1f}%")
        print(f"  Execution time: {result.execution_time:.2f}s")
        
        return result
    
    def run_all_tests(self, include_performance: bool = True):
        """Run all test suites."""
        print("Starting Recommendation Engine Test Suite")
        print(f"Python version: {sys.version}")
        print(f"Test directory: {os.path.dirname(__file__)}")
        
        self.total_start_time = time.time()
        
        # Define test suites
        test_suites = [
            ("unit", "Unit Tests"),
            ("integration", "Integration Tests"),
            ("golden_datasets", "Golden Dataset Tests"),
        ]
        
        if include_performance:
            test_suites.append(("performance", "Performance Tests"))
        
        # Run each test suite
        for suite_path, suite_name in test_suites:
            full_path = os.path.join(os.path.dirname(__file__), suite_path)
            if os.path.exists(full_path):
                result = self.run_test_suite(full_path, suite_name)
                self.results.append(result)
            else:
                print(f"Warning: Test suite directory not found: {full_path}")
        
        self.total_end_time = time.time()
        
        # Print comprehensive summary
        self.print_summary()
    
    def print_summary(self):
        """Print comprehensive test summary."""
        total_time = self.total_end_time - self.total_start_time if self.total_start_time else 0
        
        print(f"\n{'='*80}")
        print("COMPREHENSIVE TEST SUMMARY")
        print(f"{'='*80}")
        
        # Overall statistics
        total_tests = sum(r.tests_run for r in self.results)
        total_failures = sum(r.failures for r in self.results)
        total_errors = sum(r.errors for r in self.results)
        total_skipped = sum(r.skipped for r in self.results)
        
        overall_success_rate = 0.0
        if total_tests > 0:
            successful_tests = total_tests - total_failures - total_errors
            overall_success_rate = (successful_tests / total_tests) * 100
        
        print(f"Total execution time: {total_time:.2f}s")
        print(f"Total tests run: {total_tests}")
        print(f"Total failures: {total_failures}")
        print(f"Total errors: {total_errors}")
        print(f"Total skipped: {total_skipped}")
        print(f"Overall success rate: {overall_success_rate:.1f}%")
        
        # Per-suite breakdown
        print(f"\nPer-Suite Breakdown:")
        print(f"{'Suite':<25} {'Tests':<8} {'Pass':<8} {'Fail':<8} {'Error':<8} {'Success%':<10} {'Time(s)':<10}")
        print(f"{'-'*80}")
        
        for result in self.results:
            passed = result.tests_run - result.failures - result.errors
            print(f"{result.name:<25} {result.tests_run:<8} {passed:<8} {result.failures:<8} "
                  f"{result.errors:<8} {result.success_rate:<10.1f} {result.execution_time:<10.2f}")
        
        # Status assessment
        print(f"\nTest Suite Status:")
        if total_failures == 0 and total_errors == 0:
            print("✅ ALL TESTS PASSED - Recommendation engine is ready for deployment")
        elif total_failures > 0 or total_errors > 0:
            print("❌ TESTS FAILED - Issues need to be addressed before deployment")
            
            # Highlight critical failures
            critical_suites = [r for r in self.results if r.failures > 0 or r.errors > 0]
            if critical_suites:
                print(f"\nSuites with issues:")
                for result in critical_suites:
                    print(f"  - {result.name}: {result.failures} failures, {result.errors} errors")
        
        # Recommendations
        print(f"\nRecommendations:")
        if overall_success_rate >= 95:
            print("  - Excellent test coverage and quality")
            print("  - Ready for production deployment")
        elif overall_success_rate >= 85:
            print("  - Good test coverage with minor issues")
            print("  - Address failing tests before deployment")
        elif overall_success_rate >= 70:
            print("  - Moderate test coverage with significant issues")
            print("  - Requires substantial fixes before deployment")
        else:
            print("  - Poor test coverage or major issues")
            print("  - Extensive debugging and fixes required")
        
        # Performance insights (if performance tests were run)
        perf_results = [r for r in self.results if r.name == "Performance Tests"]
        if perf_results:
            perf_result = perf_results[0]
            if perf_result.failures == 0 and perf_result.errors == 0:
                print("  - Performance tests passed - system meets performance requirements")
            else:
                print("  - Performance issues detected - optimization may be needed")
    
    def save_report(self, filename: str = "test_report.txt"):
        """Save detailed test report to file."""
        report_path = os.path.join(os.path.dirname(__file__), filename)
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write("RECOMMENDATION ENGINE TEST REPORT\n")
            f.write("=" * 50 + "\n\n")
            f.write(f"Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Python version: {sys.version}\n\n")
            
            # Write summary
            total_tests = sum(r.tests_run for r in self.results)
            total_failures = sum(r.failures for r in self.results)
            total_errors = sum(r.errors for r in self.results)
            
            f.write(f"SUMMARY:\n")
            f.write(f"Total tests: {total_tests}\n")
            f.write(f"Failures: {total_failures}\n")
            f.write(f"Errors: {total_errors}\n\n")
            
            # Write detailed results
            for result in self.results:
                f.write(f"\n{result.name.upper()}\n")
                f.write("-" * len(result.name) + "\n")
                f.write(f"Tests run: {result.tests_run}\n")
                f.write(f"Failures: {result.failures}\n")
                f.write(f"Errors: {result.errors}\n")
                f.write(f"Success rate: {result.success_rate:.1f}%\n")
                f.write(f"Execution time: {result.execution_time:.2f}s\n\n")
                
                # Write details
                for detail in result.details:
                    f.write(detail)
                    f.write("\n")
        
        print(f"\nDetailed report saved to: {report_path}")


def main():
    """Main entry point for test runner."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Run recommendation engine tests")
    parser.add_argument("--no-performance", action="store_true", 
                       help="Skip performance tests (faster execution)")
    parser.add_argument("--suite", choices=["unit", "integration", "golden", "performance"],
                       help="Run only specific test suite")
    parser.add_argument("--report", default="test_report.txt",
                       help="Output file for detailed report")
    
    args = parser.parse_args()
    
    runner = RecommendationEngineTestRunner()
    
    if args.suite:
        # Run specific suite
        suite_map = {
            "unit": ("unit", "Unit Tests"),
            "integration": ("integration", "Integration Tests"), 
            "golden": ("golden_datasets", "Golden Dataset Tests"),
            "performance": ("performance", "Performance Tests")
        }
        
        if args.suite in suite_map:
            suite_path, suite_name = suite_map[args.suite]
            full_path = os.path.join(os.path.dirname(__file__), suite_path)
            result = runner.run_test_suite(full_path, suite_name)
            runner.results.append(result)
            runner.print_summary()
    else:
        # Run all tests
        include_performance = not args.no_performance
        runner.run_all_tests(include_performance=include_performance)
    
    # Save detailed report
    if runner.results:
        runner.save_report(args.report)
    
    # Exit with appropriate code
    total_failures = sum(r.failures for r in runner.results)
    total_errors = sum(r.errors for r in runner.results)
    
    if total_failures > 0 or total_errors > 0:
        sys.exit(1)  # Indicate test failures
    else:
        sys.exit(0)  # All tests passed


if __name__ == "__main__":
    main()