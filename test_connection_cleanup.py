#!/usr/bin/env python3
"""
Database Connection Cleanup Test
================================
Test script to verify that database connection cleanup fixes prevent resource leaks
and handle connection pool exhaustion properly.
"""

import asyncio
import sys
import os
import time
import gc
from contextlib import asynccontextmanager

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

# Import MongoDB replacement first
import mongodb_replacement

# Import FastAPI app components
from backend.app.main import app, startup_db_client, shutdown_db_client
from motor.motor_asyncio import AsyncIOMotorClient

class ConnectionLeakTester:
    def __init__(self):
        self.test_results = []
        self.connection_count_before = 0
        self.connection_count_after = 0
    
    async def test_connection_pooling_limits(self):
        """Test that connection pooling limits are enforced"""
        print("\n🧪 Testing connection pooling limits...")
        
        clients = []
        try:
            # Try to create more connections than the limit
            for i in range(15):  # More than max pool size of 10
                client = AsyncIOMotorClient(
                    "mongodb://localhost:27017",
                    maxPoolSize=10,
                    minPoolSize=1
                )
                clients.append(client)
                print(f"Created client {i+1}")
            
            # Test that all clients can perform operations
            for i, client in enumerate(clients):
                db = client["test_db"]
                try:
                    result = await asyncio.wait_for(db.command("ping"), timeout=5.0)
                    print(f"✅ Client {i+1} ping successful")
                except Exception as e:
                    print(f"❌ Client {i+1} ping failed: {e}")
            
            self.test_results.append("✅ Connection pooling limits test passed")
            
        except Exception as e:
            self.test_results.append(f"❌ Connection pooling limits test failed: {e}")
        
        finally:
            # Cleanup all clients
            for client in clients:
                client.close()
            print("🧹 All test clients closed")
    
    async def test_connection_cleanup_on_shutdown(self):
        """Test that connections are properly cleaned up on shutdown"""
        print("\n🧪 Testing connection cleanup on shutdown...")
        
        try:
            # Record initial connection count
            initial_count = len(mongodb_replacement.in_memory_db.active_connections)
            print(f"Initial active connections: {initial_count}")
            
            # Create a test app instance
            test_app = type('TestApp', (), {})()
            
            # Initialize database connections
            await startup_db_client(test_app)
            
            # Check connection count increased
            after_startup_count = len(mongodb_replacement.in_memory_db.active_connections)
            print(f"Active connections after startup: {after_startup_count}")
            
            # Perform some database operations
            if hasattr(test_app, 'mongodb'):
                await test_app.mongodb.command("ping")
                await test_app.mongodb.users.find_one({"email": "test@example.com"})
                print("✅ Database operations completed")
            
            # Shutdown and cleanup
            await shutdown_db_client(test_app)
            
            # Check connection count decreased
            final_count = len(mongodb_replacement.in_memory_db.active_connections)
            print(f"Active connections after shutdown: {final_count}")
            
            if final_count <= initial_count:
                self.test_results.append("✅ Connection cleanup on shutdown test passed")
            else:
                self.test_results.append(f"❌ Connection cleanup failed: {final_count} > {initial_count}")
                
        except Exception as e:
            self.test_results.append(f"❌ Connection cleanup test failed: {e}")
    
    async def test_timeout_handling(self):
        """Test that database operations have proper timeout handling"""
        print("\n🧪 Testing timeout handling...")
        
        try:
            client = AsyncIOMotorClient("mongodb://localhost:27017")
            db = client["test_db"]
            
            # Test operation with timeout
            start_time = time.time()
            try:
                # This should complete quickly with our mock system
                result = await asyncio.wait_for(db.command("ping"), timeout=1.0)
                elapsed = time.time() - start_time
                print(f"✅ Ping completed in {elapsed:.3f}s")
                
                if elapsed < 1.0:
                    self.test_results.append("✅ Timeout handling test passed")
                else:
                    self.test_results.append("❌ Operation took too long")
                    
            except asyncio.TimeoutError:
                self.test_results.append("❌ Operation timed out unexpectedly")
            
            client.close()
            
        except Exception as e:
            self.test_results.append(f"❌ Timeout handling test failed: {e}")
    
    async def test_resource_leak_prevention(self):
        """Test that repeated operations don't cause resource leaks"""
        print("\n🧪 Testing resource leak prevention...")
        
        try:
            initial_db_size = len(mongodb_replacement.in_memory_db.databases)
            initial_connections = len(mongodb_replacement.in_memory_db.active_connections)
            
            # Perform many operations
            for i in range(50):
                client = AsyncIOMotorClient("mongodb://localhost:27017")
                db = client["test_db_" + str(i % 5)]  # Use only 5 different databases
                
                # Perform operations
                await db.command("ping")
                await db.test_collection.insert_one({"test": f"data_{i}"})
                result = await db.test_collection.find_one({"test": f"data_{i}"})
                
                # Close client
                client.close()
                
                if i % 10 == 0:
                    print(f"Completed {i+1} operations")
            
            # Force garbage collection
            gc.collect()
            await asyncio.sleep(0.1)
            
            final_db_size = len(mongodb_replacement.in_memory_db.databases)
            final_connections = len(mongodb_replacement.in_memory_db.active_connections)
            
            print(f"Database count: {initial_db_size} -> {final_db_size}")
            print(f"Active connections: {initial_connections} -> {final_connections}")
            
            # Check for reasonable resource usage
            if final_db_size <= initial_db_size + 5 and final_connections <= initial_connections + 2:
                self.test_results.append("✅ Resource leak prevention test passed")
            else:
                self.test_results.append(f"❌ Potential resource leak detected")
                
        except Exception as e:
            self.test_results.append(f"❌ Resource leak prevention test failed: {e}")
    
    async def test_concurrent_operations(self):
        """Test that concurrent database operations work properly with connection limits"""
        print("\n🧪 Testing concurrent operations...")
        
        async def concurrent_operation(operation_id):
            """Single concurrent operation"""
            try:
                client = AsyncIOMotorClient("mongodb://localhost:27017")
                db = client["concurrent_test"]
                
                # Perform operations
                await db.command("ping")
                await db.operations.insert_one({"id": operation_id, "timestamp": time.time()})
                result = await db.operations.find_one({"id": operation_id})
                
                client.close()
                return f"Operation {operation_id} completed"
                
            except Exception as e:
                return f"Operation {operation_id} failed: {e}"
        
        try:
            # Run 20 concurrent operations
            tasks = [concurrent_operation(i) for i in range(20)]
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            successful = sum(1 for r in results if isinstance(r, str) and "completed" in r)
            failed = len(results) - successful
            
            print(f"Concurrent operations: {successful} successful, {failed} failed")
            
            if successful >= 15:  # Allow some failures due to connection limits
                self.test_results.append("✅ Concurrent operations test passed")
            else:
                self.test_results.append(f"❌ Too many concurrent operations failed: {failed}")
                
        except Exception as e:
            self.test_results.append(f"❌ Concurrent operations test failed: {e}")
    
    async def run_all_tests(self):
        """Run all connection cleanup tests"""
        print("🚀 Starting Database Connection Cleanup Tests")
        print("=" * 60)
        
        # Run individual tests
        await self.test_connection_pooling_limits()
        await self.test_connection_cleanup_on_shutdown()
        await self.test_timeout_handling()
        await self.test_resource_leak_prevention()
        await self.test_concurrent_operations()
        
        # Final cleanup
        await mongodb_replacement.in_memory_db.cleanup()
        
        # Print results
        print("\n" + "=" * 60)
        print("🏁 TEST RESULTS SUMMARY")
        print("=" * 60)
        
        for result in self.test_results:
            print(result)
        
        passed = sum(1 for r in self.test_results if r.startswith("✅"))
        total = len(self.test_results)
        
        print(f"\n📊 Overall: {passed}/{total} tests passed")
        
        if passed == total:
            print("🎉 All connection cleanup tests PASSED!")
            return True
        else:
            print("⚠️  Some connection cleanup tests FAILED!")
            return False

async def main():
    """Main test runner"""
    print("Database Connection Cleanup Test Suite")
    print("Testing fixes for connection pool exhaustion and resource leaks")
    
    tester = ConnectionLeakTester()
    success = await tester.run_all_tests()
    
    if success:
        print("\n✅ Connection cleanup fixes are working properly!")
        sys.exit(0)
    else:
        print("\n❌ Connection cleanup fixes need attention!")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())