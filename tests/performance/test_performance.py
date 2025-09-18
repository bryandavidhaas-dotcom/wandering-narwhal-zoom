"""
Performance tests for the recommendation engine.

Tests the performance characteristics of the recommendation engine
including response time, throughput, and scalability.
"""

import unittest
import time
import statistics
from typing import List, Dict, Any
import cProfile
import pstats
import io

# Import the modules we're testing
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from recommendation_engine.engine import RecommendationEngine
from recommendation_engine.mock_data import (
    MOCK_SKILLS, MOCK_CAREERS, MOCK_USER_PROFILE, ALTERNATIVE_USER_PROFILE,
    create_mock_user_profile, create_mock_careers, create_mock_skills
)


class TestRecommendationEnginePerformance(unittest.TestCase):
    """Performance test cases for the RecommendationEngine."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.engine = RecommendationEngine()
        self.skills = MOCK_SKILLS
        self.careers = MOCK_CAREERS
        self.user_profile = MOCK_USER_PROFILE
        
        # Performance thresholds (adjust based on requirements)
        self.max_response_time = 2.0  # seconds
        self.min_throughput = 10  # recommendations per second
    
    def measure_execution_time(self, func, *args, **kwargs) -> tuple:
        """Measure execution time of a function."""
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        return result, execution_time
    
    def test_single_recommendation_response_time(self):
        """Test response time for a single recommendation request."""
        recommendations, execution_time = self.measure_execution_time(
            self.engine.get_recommendations,
            self.user_profile, self.careers, self.skills
        )
        
        # Should complete within acceptable time
        self.assertLess(execution_time, self.max_response_time,
            f"Single recommendation took {execution_time:.3f}s, expected < {self.max_response_time}s")
        
        # Should return valid recommendations
        self.assertIsInstance(recommendations, list)
        self.assertGreater(len(recommendations), 0)
        
        print(f"Single recommendation response time: {execution_time:.3f}s")
    
    def test_multiple_requests_throughput(self):
        """Test throughput with multiple recommendation requests."""
        num_requests = 20
        execution_times = []
        
        # Measure multiple requests
        for i in range(num_requests):
            _, execution_time = self.measure_execution_time(
                self.engine.get_recommendations,
                self.user_profile, self.careers, self.skills
            )
            execution_times.append(execution_time)
        
        # Calculate statistics
        avg_time = statistics.mean(execution_times)
        max_time = max(execution_times)
        min_time = min(execution_times)
        throughput = 1.0 / avg_time if avg_time > 0 else 0
        
        # Validate performance
        self.assertLess(avg_time, self.max_response_time,
            f"Average response time {avg_time:.3f}s exceeds threshold {self.max_response_time}s")
        
        self.assertGreater(throughput, self.min_throughput,
            f"Throughput {throughput:.1f} req/s below threshold {self.min_throughput} req/s")
        
        print(f"Throughput test results:")
        print(f"  Requests: {num_requests}")
        print(f"  Average time: {avg_time:.3f}s")
        print(f"  Min time: {min_time:.3f}s")
        print(f"  Max time: {max_time:.3f}s")
        print(f"  Throughput: {throughput:.1f} req/s")
    
    def test_scalability_with_career_count(self):
        """Test how performance scales with number of careers."""
        career_counts = [5, 10, 20, 50]
        results = []
        
        for count in career_counts:
            # Use subset of careers
            careers_subset = self.careers[:count] if count <= len(self.careers) else self.careers
            
            # If we need more careers than available, duplicate some
            while len(careers_subset) < count:
                careers_subset.extend(self.careers[:min(count - len(careers_subset), len(self.careers))])
            
            careers_subset = careers_subset[:count]
            
            # Measure performance
            _, execution_time = self.measure_execution_time(
                self.engine.get_recommendations,
                self.user_profile, careers_subset, self.skills
            )
            
            results.append((count, execution_time))
            print(f"  {count} careers: {execution_time:.3f}s")
        
        # Check that performance doesn't degrade too much
        # Allow for some linear scaling but not exponential
        if len(results) >= 2:
            first_time = results[0][1]
            last_time = results[-1][1]
            first_count = results[0][0]
            last_count = results[-1][0]
            
            # Calculate scaling factor
            count_ratio = last_count / first_count
            time_ratio = last_time / first_time if first_time > 0 else float('inf')
            
            # Time should not scale worse than O(n^2)
            max_acceptable_ratio = count_ratio ** 2
            self.assertLess(time_ratio, max_acceptable_ratio,
                f"Performance degradation too severe: {time_ratio:.2f}x time for {count_ratio:.2f}x careers")
        
        print(f"Scalability test with career count completed")
    
    def test_scalability_with_user_skills(self):
        """Test how performance scales with number of user skills."""
        # Create user profiles with different numbers of skills
        skill_counts = [2, 5, 10, 15]
        results = []
        
        for count in skill_counts:
            # Create user profile with specified number of skills
            user_skills = self.user_profile.skills[:count] if count <= len(self.user_profile.skills) else self.user_profile.skills
            
            # If we need more skills, duplicate some
            while len(user_skills) < count:
                user_skills.extend(self.user_profile.skills[:min(count - len(user_skills), len(self.user_profile.skills))])
            
            user_skills = user_skills[:count]
            
            # Create modified user profile
            modified_user = MOCK_USER_PROFILE
            modified_user.skills = user_skills
            
            # Measure performance
            _, execution_time = self.measure_execution_time(
                self.engine.get_recommendations,
                modified_user, self.careers, self.skills
            )
            
            results.append((count, execution_time))
            print(f"  {count} user skills: {execution_time:.3f}s")
        
        print(f"Scalability test with user skills completed")
    
    def test_memory_usage_stability(self):
        """Test that memory usage remains stable across multiple requests."""
        import gc
        import psutil
        import os
        
        # Get current process
        process = psutil.Process(os.getpid())
        
        # Measure initial memory
        gc.collect()  # Force garbage collection
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        # Run multiple requests
        num_requests = 50
        for i in range(num_requests):
            recommendations = self.engine.get_recommendations(
                self.user_profile, self.careers, self.skills
            )
            
            # Periodically check memory
            if i % 10 == 0:
                gc.collect()
                current_memory = process.memory_info().rss / 1024 / 1024  # MB
                memory_increase = current_memory - initial_memory
                
                # Memory should not increase significantly
                self.assertLess(memory_increase, 100,  # 100MB threshold
                    f"Memory usage increased by {memory_increase:.1f}MB after {i+1} requests")
        
        # Final memory check
        gc.collect()
        final_memory = process.memory_info().rss / 1024 / 1024  # MB
        total_increase = final_memory - initial_memory
        
        print(f"Memory usage test:")
        print(f"  Initial: {initial_memory:.1f}MB")
        print(f"  Final: {final_memory:.1f}MB")
        print(f"  Increase: {total_increase:.1f}MB")
        
        # Should not have significant memory leaks
        self.assertLess(total_increase, 50,  # 50MB threshold
            f"Total memory increase of {total_increase:.1f}MB suggests memory leak")
    
    def test_concurrent_requests_simulation(self):
        """Simulate concurrent requests to test thread safety and performance."""
        import threading
        import queue
        
        num_threads = 5
        requests_per_thread = 10
        results_queue = queue.Queue()
        
        def worker():
            """Worker function for concurrent requests."""
            thread_times = []
            for _ in range(requests_per_thread):
                start_time = time.time()
                recommendations = self.engine.get_recommendations(
                    self.user_profile, self.careers, self.skills
                )
                end_time = time.time()
                thread_times.append(end_time - start_time)
            
            results_queue.put(thread_times)
        
        # Start threads
        threads = []
        start_time = time.time()
        
        for _ in range(num_threads):
            thread = threading.Thread(target=worker)
            thread.start()
            threads.append(thread)
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        end_time = time.time()
        total_time = end_time - start_time
        
        # Collect results
        all_times = []
        while not results_queue.empty():
            thread_times = results_queue.get()
            all_times.extend(thread_times)
        
        # Calculate statistics
        total_requests = num_threads * requests_per_thread
        avg_time = statistics.mean(all_times)
        overall_throughput = total_requests / total_time
        
        print(f"Concurrent requests test:")
        print(f"  Threads: {num_threads}")
        print(f"  Requests per thread: {requests_per_thread}")
        print(f"  Total requests: {total_requests}")
        print(f"  Total time: {total_time:.3f}s")
        print(f"  Average request time: {avg_time:.3f}s")
        print(f"  Overall throughput: {overall_throughput:.1f} req/s")
        
        # Validate performance under concurrency
        self.assertLess(avg_time, self.max_response_time * 2,  # Allow some degradation under concurrency
            f"Average response time under concurrency {avg_time:.3f}s too high")
    
    def test_profiling_hotspots(self):
        """Profile the recommendation engine to identify performance hotspots."""
        # Create profiler
        profiler = cProfile.Profile()
        
        # Profile the recommendation process
        profiler.enable()
        recommendations = self.engine.get_recommendations(
            self.user_profile, self.careers, self.skills
        )
        profiler.disable()
        
        # Analyze results
        stats_stream = io.StringIO()
        stats = pstats.Stats(profiler, stream=stats_stream)
        stats.sort_stats('cumulative')
        stats.print_stats(20)  # Top 20 functions
        
        profile_output = stats_stream.getvalue()
        
        # Basic validation that profiling worked
        self.assertIn('function calls', profile_output)
        
        print("Performance profiling results (top functions by cumulative time):")
        print(profile_output)
        
        # Should return valid recommendations
        self.assertIsInstance(recommendations, list)
        self.assertGreater(len(recommendations), 0)
    
    def test_large_dataset_performance(self):
        """Test performance with larger datasets."""
        # Create larger datasets
        large_careers = []
        large_skills = []
        
        # Multiply existing data
        multiplier = 5
        for i in range(multiplier):
            for career in self.careers:
                # Create modified career with unique ID
                modified_career = career
                modified_career.career_id = f"{career.career_id}_copy_{i}"
                large_careers.append(modified_career)
            
            for skill in self.skills:
                # Create modified skill with unique ID
                modified_skill = skill
                modified_skill.skill_id = f"{skill.skill_id}_copy_{i}"
                large_skills.append(modified_skill)
        
        print(f"Testing with {len(large_careers)} careers and {len(large_skills)} skills")
        
        # Measure performance with large dataset
        recommendations, execution_time = self.measure_execution_time(
            self.engine.get_recommendations,
            self.user_profile, large_careers, large_skills
        )
        
        # Should still complete in reasonable time
        max_large_dataset_time = self.max_response_time * 3  # Allow more time for larger dataset
        self.assertLess(execution_time, max_large_dataset_time,
            f"Large dataset processing took {execution_time:.3f}s, expected < {max_large_dataset_time}s")
        
        # Should return valid recommendations
        self.assertIsInstance(recommendations, list)
        self.assertGreater(len(recommendations), 0)
        
        print(f"Large dataset performance: {execution_time:.3f}s")


class TestPerformanceRegression(unittest.TestCase):
    """Test for performance regressions."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.engine = RecommendationEngine()
        self.skills = MOCK_SKILLS
        self.careers = MOCK_CAREERS
        self.user_profile = MOCK_USER_PROFILE
        
        # Baseline performance expectations (update these based on actual measurements)
        self.baseline_response_time = 1.0  # seconds
        self.baseline_throughput = 20  # requests per second
    
    def test_performance_regression(self):
        """Test that performance hasn't regressed from baseline."""
        # Measure current performance
        num_requests = 10
        execution_times = []
        
        for _ in range(num_requests):
            start_time = time.time()
            recommendations = self.engine.get_recommendations(
                self.user_profile, self.careers, self.skills
            )
            end_time = time.time()
            execution_times.append(end_time - start_time)
        
        avg_time = statistics.mean(execution_times)
        current_throughput = 1.0 / avg_time if avg_time > 0 else 0
        
        # Check against baseline (allow 20% degradation)
        max_acceptable_time = self.baseline_response_time * 1.2
        min_acceptable_throughput = self.baseline_throughput * 0.8
        
        self.assertLess(avg_time, max_acceptable_time,
            f"Performance regression detected: {avg_time:.3f}s > {max_acceptable_time:.3f}s baseline")
        
        self.assertGreater(current_throughput, min_acceptable_throughput,
            f"Throughput regression detected: {current_throughput:.1f} < {min_acceptable_throughput:.1f} baseline")
        
        print(f"Performance regression test:")
        print(f"  Current avg time: {avg_time:.3f}s (baseline: {self.baseline_response_time:.3f}s)")
        print(f"  Current throughput: {current_throughput:.1f} req/s (baseline: {self.baseline_throughput:.1f} req/s)")


if __name__ == '__main__':
    # Run with verbose output to see performance metrics
    unittest.main(verbosity=2)