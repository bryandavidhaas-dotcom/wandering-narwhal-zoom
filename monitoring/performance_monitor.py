#!/usr/bin/env python3
"""
Performance Monitoring System for Career Platform
Phase 3: Deploy Quality Monitoring System

This module monitors query performance and response times, tracks database
connection health and availability, monitors data growth and storage utilization,
and creates performance benchmarks and SLA tracking.
"""

import asyncio
import json
import logging
import time
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from pathlib import Path
from collections import deque, defaultdict
import statistics
import psutil

from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
import pymongo

# Import models
import sys
sys.path.append(str(Path(__file__).parent.parent))
from backend.models import CareerModel, SkillModel

@dataclass
class QueryPerformanceMetric:
    """Individual query performance measurement"""
    timestamp: datetime
    query_type: str
    collection: str
    execution_time_ms: float
    documents_examined: int
    documents_returned: int
    index_used: bool
    query_filter: str
    memory_usage_mb: Optional[float] = None
    cpu_usage_percent: Optional[float] = None

@dataclass
class ConnectionMetric:
    """Database connection health metric"""
    timestamp: datetime
    active_connections: int
    available_connections: int
    connection_pool_size: int
    connection_wait_time_ms: float
    failed_connections: int
    connection_success_rate: float

@dataclass
class StorageMetric:
    """Storage and data growth metric"""
    timestamp: datetime
    total_documents: int
    storage_size_mb: float
    index_size_mb: float
    data_size_mb: float
    avg_document_size_kb: float
    growth_rate_percent: float
    fragmentation_percent: float

@dataclass
class PerformanceBenchmark:
    """Performance benchmark definition"""
    metric_name: str
    target_value: float
    warning_threshold: float
    critical_threshold: float
    unit: str
    description: str

@dataclass
class SLAMetric:
    """Service Level Agreement metric"""
    name: str
    target_percentage: float
    current_percentage: float
    measurement_period: str
    violations_count: int
    last_violation: Optional[datetime]

class QueryProfiler:
    """Profile and analyze database query performance"""
    
    def __init__(self, client: AsyncIOMotorClient, db_name: str):
        self.client = client
        self.db = client[db_name]
        self.logger = logging.getLogger(__name__)
        self.query_history = deque(maxlen=1000)  # Keep last 1000 queries
    
    async def profile_query(self, collection_name: str, query_filter: Dict, 
                          query_type: str = "find") -> QueryPerformanceMetric:
        """Profile a single query execution"""
        collection = self.db[collection_name]
        
        # Start timing and resource monitoring
        start_time = time.time()
        start_cpu = psutil.cpu_percent()
        process = psutil.Process()
        start_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        try:
            # Execute query with explain
            if query_type == "find":
                cursor = collection.find(query_filter)
                explain_result = await cursor.explain()
                documents = await cursor.to_list(length=None)
                documents_returned = len(documents)
            elif query_type == "count":
                documents_returned = await collection.count_documents(query_filter)
                explain_result = await collection.find(query_filter).explain()
            elif query_type == "aggregate":
                # For aggregation, query_filter should be the pipeline
                cursor = collection.aggregate(query_filter)
                explain_result = await cursor.explain() if hasattr(cursor, 'explain') else {}
                documents = await cursor.to_list(length=None)
                documents_returned = len(documents)
            else:
                raise ValueError(f"Unsupported query type: {query_type}")
            
            # Calculate metrics
            end_time = time.time()
            execution_time_ms = (end_time - start_time) * 1000
            
            end_cpu = psutil.cpu_percent()
            end_memory = process.memory_info().rss / 1024 / 1024  # MB
            
            # Extract explain information
            execution_stats = explain_result.get('executionStats', {})
            documents_examined = execution_stats.get('totalDocsExamined', 0)
            index_used = len(execution_stats.get('executionStages', {}).get('indexName', '')) > 0
            
            metric = QueryPerformanceMetric(
                timestamp=datetime.utcnow(),
                query_type=query_type,
                collection=collection_name,
                execution_time_ms=execution_time_ms,
                documents_examined=documents_examined,
                documents_returned=documents_returned,
                index_used=index_used,
                query_filter=str(query_filter)[:200],  # Truncate for storage
                memory_usage_mb=end_memory - start_memory,
                cpu_usage_percent=end_cpu - start_cpu
            )
            
            self.query_history.append(metric)
            return metric
            
        except Exception as e:
            self.logger.error(f"Error profiling query: {e}")
            # Return error metric
            return QueryPerformanceMetric(
                timestamp=datetime.utcnow(),
                query_type=query_type,
                collection=collection_name,
                execution_time_ms=(time.time() - start_time) * 1000,
                documents_examined=0,
                documents_returned=0,
                index_used=False,
                query_filter=str(query_filter)[:200],
                memory_usage_mb=0,
                cpu_usage_percent=0
            )
    
    async def profile_common_queries(self) -> List[QueryPerformanceMetric]:
        """Profile common application queries"""
        common_queries = [
            # Career searches
            ("careers", {"experienceLevel": "Mid Level"}, "find"),
            ("careers", {"careerType": "Technology"}, "find"),
            ("careers", {"salaryMin": {"$gte": 50000}}, "find"),
            ("careers", {"requiredTechnicalSkills": {"$in": ["Python", "JavaScript"]}}, "find"),
            
            # Aggregations
            ("careers", [
                {"$group": {"_id": "$experienceLevel", "count": {"$sum": 1}}},
                {"$sort": {"count": -1}}
            ], "aggregate"),
            
            # Counts
            ("careers", {}, "count"),
            ("careers", {"experienceLevel": "Senior Level"}, "count"),
        ]
        
        results = []
        for collection, query_filter, query_type in common_queries:
            try:
                metric = await self.profile_query(collection, query_filter, query_type)
                results.append(metric)
                
                # Small delay between queries
                await asyncio.sleep(0.1)
                
            except Exception as e:
                self.logger.error(f"Error profiling query {query_type} on {collection}: {e}")
        
        return results
    
    def get_query_statistics(self, time_window_minutes: int = 60) -> Dict[str, Any]:
        """Get query performance statistics for a time window"""
        cutoff_time = datetime.utcnow() - timedelta(minutes=time_window_minutes)
        recent_queries = [q for q in self.query_history if q.timestamp > cutoff_time]
        
        if not recent_queries:
            return {"error": "No queries in time window"}
        
        execution_times = [q.execution_time_ms for q in recent_queries]
        
        # Group by query type
        by_type = defaultdict(list)
        for query in recent_queries:
            by_type[query.query_type].append(query.execution_time_ms)
        
        # Group by collection
        by_collection = defaultdict(list)
        for query in recent_queries:
            by_collection[query.collection].append(query.execution_time_ms)
        
        return {
            "time_window_minutes": time_window_minutes,
            "total_queries": len(recent_queries),
            "overall_stats": {
                "avg_execution_time_ms": statistics.mean(execution_times),
                "median_execution_time_ms": statistics.median(execution_times),
                "min_execution_time_ms": min(execution_times),
                "max_execution_time_ms": max(execution_times),
                "p95_execution_time_ms": self._percentile(execution_times, 95),
                "p99_execution_time_ms": self._percentile(execution_times, 99)
            },
            "by_query_type": {
                query_type: {
                    "count": len(times),
                    "avg_ms": statistics.mean(times),
                    "max_ms": max(times)
                } for query_type, times in by_type.items()
            },
            "by_collection": {
                collection: {
                    "count": len(times),
                    "avg_ms": statistics.mean(times),
                    "max_ms": max(times)
                } for collection, times in by_collection.items()
            },
            "slow_queries": [
                {
                    "timestamp": q.timestamp.isoformat(),
                    "query_type": q.query_type,
                    "collection": q.collection,
                    "execution_time_ms": q.execution_time_ms,
                    "query_filter": q.query_filter
                }
                for q in sorted(recent_queries, key=lambda x: x.execution_time_ms, reverse=True)[:5]
            ]
        }
    
    def _percentile(self, data: List[float], percentile: int) -> float:
        """Calculate percentile of data"""
        if not data:
            return 0.0
        sorted_data = sorted(data)
        index = int(len(sorted_data) * percentile / 100)
        return sorted_data[min(index, len(sorted_data) - 1)]

class ConnectionMonitor:
    """Monitor database connection health and performance"""
    
    def __init__(self, client: AsyncIOMotorClient, db_name: str):
        self.client = client
        self.db = client[db_name]
        self.logger = logging.getLogger(__name__)
        self.connection_history = deque(maxlen=500)
    
    async def collect_connection_metrics(self) -> ConnectionMetric:
        """Collect current connection metrics"""
        try:
            # Get server status
            server_status = await self.db.command('serverStatus')
            
            connections = server_status.get('connections', {})
            active_connections = connections.get('current', 0)
            available_connections = connections.get('available', 0)
            
            # Calculate connection pool size
            connection_pool_size = active_connections + available_connections
            
            # Test connection response time
            start_time = time.time()
            await self.client.admin.command('ping')
            connection_wait_time_ms = (time.time() - start_time) * 1000
            
            # Get connection success rate (simplified - would need more sophisticated tracking)
            connection_success_rate = 100.0  # Assume 100% if we can get metrics
            failed_connections = 0  # Would need to track this over time
            
            metric = ConnectionMetric(
                timestamp=datetime.utcnow(),
                active_connections=active_connections,
                available_connections=available_connections,
                connection_pool_size=connection_pool_size,
                connection_wait_time_ms=connection_wait_time_ms,
                failed_connections=failed_connections,
                connection_success_rate=connection_success_rate
            )
            
            self.connection_history.append(metric)
            return metric
            
        except Exception as e:
            self.logger.error(f"Error collecting connection metrics: {e}")
            # Return error metric
            return ConnectionMetric(
                timestamp=datetime.utcnow(),
                active_connections=0,
                available_connections=0,
                connection_pool_size=0,
                connection_wait_time_ms=0,
                failed_connections=1,
                connection_success_rate=0.0
            )
    
    def get_connection_statistics(self, time_window_minutes: int = 60) -> Dict[str, Any]:
        """Get connection statistics for a time window"""
        cutoff_time = datetime.utcnow() - timedelta(minutes=time_window_minutes)
        recent_metrics = [m for m in self.connection_history if m.timestamp > cutoff_time]
        
        if not recent_metrics:
            return {"error": "No connection metrics in time window"}
        
        return {
            "time_window_minutes": time_window_minutes,
            "current_connections": recent_metrics[-1].active_connections if recent_metrics else 0,
            "avg_active_connections": statistics.mean([m.active_connections for m in recent_metrics]),
            "max_active_connections": max([m.active_connections for m in recent_metrics]),
            "avg_connection_wait_time_ms": statistics.mean([m.connection_wait_time_ms for m in recent_metrics]),
            "max_connection_wait_time_ms": max([m.connection_wait_time_ms for m in recent_metrics]),
            "connection_success_rate": statistics.mean([m.connection_success_rate for m in recent_metrics]),
            "total_failed_connections": sum([m.failed_connections for m in recent_metrics])
        }

class StorageMonitor:
    """Monitor storage utilization and data growth"""
    
    def __init__(self, client: AsyncIOMotorClient, db_name: str):
        self.client = client
        self.db = client[db_name]
        self.logger = logging.getLogger(__name__)
        self.storage_history = deque(maxlen=500)
    
    async def collect_storage_metrics(self) -> StorageMetric:
        """Collect current storage metrics"""
        try:
            # Get database stats
            db_stats = await self.db.command('dbStats')
            
            # Get collection stats for careers
            careers_stats = await self.db.command('collStats', 'careers')
            
            total_documents = careers_stats.get('count', 0)
            storage_size_mb = db_stats.get('storageSize', 0) / (1024 * 1024)
            index_size_mb = db_stats.get('indexSize', 0) / (1024 * 1024)
            data_size_mb = db_stats.get('dataSize', 0) / (1024 * 1024)
            
            avg_document_size_kb = 0
            if total_documents > 0:
                avg_document_size_kb = (data_size_mb * 1024) / total_documents
            
            # Calculate growth rate
            growth_rate_percent = 0.0
            if len(self.storage_history) > 0:
                prev_metric = self.storage_history[-1]
                if prev_metric.total_documents > 0:
                    growth_rate_percent = ((total_documents - prev_metric.total_documents) / 
                                         prev_metric.total_documents) * 100
            
            # Calculate fragmentation (simplified)
            fragmentation_percent = 0.0
            if storage_size_mb > 0:
                fragmentation_percent = max(0, ((storage_size_mb - data_size_mb) / storage_size_mb) * 100)
            
            metric = StorageMetric(
                timestamp=datetime.utcnow(),
                total_documents=total_documents,
                storage_size_mb=storage_size_mb,
                index_size_mb=index_size_mb,
                data_size_mb=data_size_mb,
                avg_document_size_kb=avg_document_size_kb,
                growth_rate_percent=growth_rate_percent,
                fragmentation_percent=fragmentation_percent
            )
            
            self.storage_history.append(metric)
            return metric
            
        except Exception as e:
            self.logger.error(f"Error collecting storage metrics: {e}")
            return StorageMetric(
                timestamp=datetime.utcnow(),
                total_documents=0,
                storage_size_mb=0,
                index_size_mb=0,
                data_size_mb=0,
                avg_document_size_kb=0,
                growth_rate_percent=0,
                fragmentation_percent=0
            )
    
    def get_storage_statistics(self, time_window_minutes: int = 1440) -> Dict[str, Any]:  # 24 hours default
        """Get storage statistics for a time window"""
        cutoff_time = datetime.utcnow() - timedelta(minutes=time_window_minutes)
        recent_metrics = [m for m in self.storage_history if m.timestamp > cutoff_time]
        
        if not recent_metrics:
            return {"error": "No storage metrics in time window"}
        
        current = recent_metrics[-1]
        oldest = recent_metrics[0]
        
        return {
            "time_window_minutes": time_window_minutes,
            "current_storage": {
                "total_documents": current.total_documents,
                "storage_size_mb": current.storage_size_mb,
                "index_size_mb": current.index_size_mb,
                "data_size_mb": current.data_size_mb,
                "avg_document_size_kb": current.avg_document_size_kb,
                "fragmentation_percent": current.fragmentation_percent
            },
            "growth_metrics": {
                "document_growth": current.total_documents - oldest.total_documents,
                "storage_growth_mb": current.storage_size_mb - oldest.storage_size_mb,
                "avg_growth_rate_percent": statistics.mean([m.growth_rate_percent for m in recent_metrics]),
                "max_growth_rate_percent": max([m.growth_rate_percent for m in recent_metrics])
            },
            "projections": {
                "documents_next_month": self._project_growth(
                    current.total_documents, 
                    statistics.mean([m.growth_rate_percent for m in recent_metrics[-7:]]) if len(recent_metrics) >= 7 else 0,
                    30
                ),
                "storage_next_month_mb": self._project_growth(
                    current.storage_size_mb,
                    (current.storage_size_mb - oldest.storage_size_mb) / oldest.storage_size_mb * 100 if oldest.storage_size_mb > 0 else 0,
                    30
                )
            }
        }
    
    def _project_growth(self, current_value: float, growth_rate_percent: float, days: int) -> float:
        """Project future growth based on current rate"""
        if growth_rate_percent <= 0:
            return current_value
        
        daily_growth_rate = growth_rate_percent / 100 / 30  # Assume monthly rate
        return current_value * ((1 + daily_growth_rate) ** days)

class PerformanceMonitor:
    """Main performance monitoring system"""
    
    def __init__(self, mongo_url: str = "mongodb://localhost:27017", db_name: str = "career_platform"):
        self.mongo_url = mongo_url
        self.db_name = db_name
        self.client = None
        self.db = None
        
        # Initialize components
        self.query_profiler = None
        self.connection_monitor = None
        self.storage_monitor = None
        
        # Performance benchmarks
        self.benchmarks = self._setup_default_benchmarks()
        
        # SLA definitions
        self.slas = self._setup_default_slas()
        
        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('monitoring/performance_monitor.log'),
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
            
            # Initialize monitors
            self.query_profiler = QueryProfiler(self.client, self.db_name)
            self.connection_monitor = ConnectionMonitor(self.client, self.db_name)
            self.storage_monitor = StorageMonitor(self.client, self.db_name)
            
            self.logger.info("✅ Performance monitoring system connected")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Database connection failed: {e}")
            return False
    
    def _setup_default_benchmarks(self) -> List[PerformanceBenchmark]:
        """Setup default performance benchmarks"""
        return [
            PerformanceBenchmark(
                metric_name="avg_query_time_ms",
                target_value=100.0,
                warning_threshold=200.0,
                critical_threshold=500.0,
                unit="milliseconds",
                description="Average query execution time"
            ),
            PerformanceBenchmark(
                metric_name="p95_query_time_ms",
                target_value=250.0,
                warning_threshold=500.0,
                critical_threshold=1000.0,
                unit="milliseconds",
                description="95th percentile query execution time"
            ),
            PerformanceBenchmark(
                metric_name="connection_wait_time_ms",
                target_value=10.0,
                warning_threshold=50.0,
                critical_threshold=100.0,
                unit="milliseconds",
                description="Database connection wait time"
            ),
            PerformanceBenchmark(
                metric_name="storage_growth_rate_percent",
                target_value=5.0,
                warning_threshold=15.0,
                critical_threshold=25.0,
                unit="percent",
                description="Monthly storage growth rate"
            )
        ]
    
    def _setup_default_slas(self) -> List[SLAMetric]:
        """Setup default SLA metrics"""
        return [
            SLAMetric(
                name="Query Response Time",
                target_percentage=95.0,  # 95% of queries under 200ms
                current_percentage=0.0,
                measurement_period="24h",
                violations_count=0,
                last_violation=None
            ),
            SLAMetric(
                name="Database Availability",
                target_percentage=99.9,  # 99.9% uptime
                current_percentage=0.0,
                measurement_period="24h",
                violations_count=0,
                last_violation=None
            ),
            SLAMetric(
                name="Connection Success Rate",
                target_percentage=99.5,  # 99.5% successful connections
                current_percentage=0.0,
                measurement_period="24h",
                violations_count=0,
                last_violation=None
            )
        ]
    
    async def run_performance_assessment(self) -> Dict[str, Any]:
        """Run comprehensive performance assessment"""
        self.logger.info("🔍 Running performance assessment...")
        
        try:
            # Profile common queries
            query_metrics = await self.query_profiler.profile_common_queries()
            query_stats = self.query_profiler.get_query_statistics(60)
            
            # Collect connection metrics
            connection_metric = await self.connection_monitor.collect_connection_metrics()
            connection_stats = self.connection_monitor.get_connection_statistics(60)
            
            # Collect storage metrics
            storage_metric = await self.storage_monitor.collect_storage_metrics()
            storage_stats = self.storage_monitor.get_storage_statistics(1440)  # 24 hours
            
            # Update SLA metrics
            self._update_sla_metrics(query_stats, connection_stats)
            
            # Check benchmarks
            benchmark_results = self._check_benchmarks(query_stats, connection_stats, storage_stats)
            
            assessment = {
                "timestamp": datetime.utcnow().isoformat(),
                "query_performance": {
                    "metrics_collected": len(query_metrics),
                    "statistics": query_stats
                },
                "connection_health": {
                    "current_metric": asdict(connection_metric),
                    "statistics": connection_stats
                },
                "storage_utilization": {
                    "current_metric": asdict(storage_metric),
                    "statistics": storage_stats
                },
                "benchmark_results": benchmark_results,
                "sla_status": [asdict(sla) for sla in self.slas],
                "overall_health_score": self._calculate_health_score(benchmark_results)
            }
            
            self.logger.info("✅ Performance assessment completed")
            return assessment
            
        except Exception as e:
            self.logger.error(f"❌ Performance assessment failed: {e}")
            raise
    
    def _update_sla_metrics(self, query_stats: Dict, connection_stats: Dict):
        """Update SLA metrics based on current performance"""
        try:
            # Update Query Response Time SLA
            if "overall_stats" in query_stats:
                p95_time = query_stats["overall_stats"].get("p95_execution_time_ms", 0)
                query_sla = next((sla for sla in self.slas if sla.name == "Query Response Time"), None)
                if query_sla:
                    # Calculate percentage of queries under 200ms threshold
                    if p95_time <= 200:
                        query_sla.current_percentage = 95.0  # Simplified calculation
                    else:
                        query_sla.current_percentage = max(0, 95.0 - (p95_time - 200) / 10)
                    
                    if query_sla.current_percentage < query_sla.target_percentage:
                        query_sla.violations_count += 1
                        query_sla.last_violation = datetime.utcnow()
            
            # Update Connection Success Rate SLA
            connection_sla = next((sla for sla in self.slas if sla.name == "Connection Success Rate"), None)
            if connection_sla and "connection_success_rate" in connection_stats:
                connection_sla.current_percentage = connection_stats["connection_success_rate"]
                
                if connection_sla.current_percentage < connection_sla.target_percentage:
                    connection_sla.violations_count += 1
                    connection_sla.last_violation = datetime.utcnow()
            
            # Update Database Availability SLA (simplified - assume 100% if we can collect metrics)
            availability_sla = next((sla for sla in self.slas if sla.name == "Database Availability"), None)
            if availability_sla:
                availability_sla.current_percentage = 100.0  # Simplified
                
        except Exception as e:
            self.logger.error(f"Error updating SLA metrics: {e}")
    
    def _check_benchmarks(self, query_stats: Dict, connection_stats: Dict, storage_stats: Dict) -> Dict[str, Any]:
        """Check current performance against benchmarks"""
        results = {}
        
        try:
            # Check query performance benchmarks
            if "overall_stats" in query_stats:
                avg_query_time = query_stats["overall_stats"].get("avg_execution_time_ms", 0)
                p95_query_time = query_stats["overall_stats"].get("p95_execution_time_ms", 0)
                
                results["avg_query_time_ms"] = self._evaluate_benchmark("avg_query_time_ms", avg_query_time)
                results["p95_query_time_ms"] = self._evaluate_benchmark("p95_query_time_ms", p95_query_time)
            
            # Check connection benchmarks
            if "avg_connection_wait_time_ms" in connection_stats:
                connection_wait_time = connection_stats["avg_connection_wait_time_ms"]
                results["connection_wait_time_ms"] = self._evaluate_benchmark("connection_wait_time_ms", connection_wait_time)
            
            # Check storage benchmarks
            if "growth_metrics" in storage_stats:
                growth_rate = storage_stats["growth_metrics"].get("avg_growth_rate_percent", 0)
                results["storage_growth_rate_percent"] = self._evaluate_benchmark("storage_growth_rate_percent", abs(growth_rate))
            
        except Exception as e:
            self.logger.error(f"Error checking benchmarks: {e}")
        
        return results
    
    def _evaluate_benchmark(self, metric_name: str, current_value: float) -> Dict[str, Any]:
        """Evaluate a metric against its benchmark"""
        benchmark = next((b for b in self.benchmarks if b.metric_name == metric_name), None)
        if not benchmark:
            return {"status": "unknown", "message": "No benchmark defined"}
        
        if current_value <= benchmark.target_value:
            status = "excellent"
            message = f"Performance excellent: {current_value} {benchmark.unit} (target: {benchmark.target_value})"
        elif current_value <= benchmark.warning_threshold:
            status = "good"
            message = f"Performance good: {current_value} {benchmark.unit} (target: {benchmark.target_value})"
        elif current_value <= benchmark.critical_threshold:
            status = "warning"
            message = f"Performance warning: {current_value} {benchmark.unit} (threshold: {benchmark.warning_threshold})"
        else:
            status = "critical"
            message = f"Performance critical: {current_value} {benchmark.unit} (threshold: {benchmark.critical_threshold})"
        
        return {
            "status": status,
            "current_value": current_value,
            "target_value": benchmark.target_value,
            "warning_threshold": benchmark.warning_threshold,
            "critical_threshold": benchmark.critical_threshold,
            "message": message
        }
    
    def _calculate_health_score(self, benchmark_results: Dict[str, Any]) -> float:
        """Calculate overall health score based on benchmark results"""
        if not benchmark_results:
            return 100.0
        
        status_scores = {
            "excellent": 100,
            "good": 80,
            "warning": 60,
            "critical": 20,
            "unknown": 50
        }
        
        scores = [status_scores.get(result.get("status", "unknown"), 50) 
                 for result in benchmark_results.values()]
        
        return statistics.mean(scores) if scores else 100.0
    
    async def save_performance_report(self, assessment: Dict[str, Any], 
                                    filepath: str = "monitoring/performance_report.json"):
        """Save performance assessment to file"""
        try:
            Path(filepath).parent.mkdir(parents=True, exist_ok=True)
            
            with open(filepath, 'w') as f:
                json.dump(assessment, f, indent=2, default=str)
            
            self.logger.info(f"📊 Performance report saved to {filepath}")
            
        except Exception as e:
            self.logger.error(f"Error saving performance report: {e}")

async