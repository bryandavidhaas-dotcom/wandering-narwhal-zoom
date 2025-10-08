#!/usr/bin/env python3
"""
Alerting System for Career Platform
Phase 3: Deploy Quality Monitoring System

This module provides threshold-based alerts for critical quality metrics,
email/notification system for quality issues, monitoring for database connectivity
and performance, and escalation procedures for critical failures.
"""

import asyncio
import json
import logging
import smtplib
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, asdict
from pathlib import Path
from enum import Enum
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

import aiohttp
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
import psutil

# Import models and monitoring components
import sys
sys.path.append(str(Path(__file__).parent.parent))
from backend.models import CareerModel, SkillModel

class AlertLevel(str, Enum):
    """Alert severity levels"""
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"

class AlertChannel(str, Enum):
    """Alert delivery channels"""
    EMAIL = "EMAIL"
    SLACK = "SLACK"
    WEBHOOK = "WEBHOOK"
    LOG = "LOG"
    CONSOLE = "CONSOLE"

@dataclass
class AlertThreshold:
    """Alert threshold configuration"""
    metric_name: str
    threshold_value: float
    comparison_operator: str  # '<', '>', '<=', '>=', '==', '!='
    level: AlertLevel
    channels: List[AlertChannel]
    cooldown_minutes: int = 30
    description: str = ""

@dataclass
class Alert:
    """Individual alert instance"""
    id: str
    timestamp: datetime
    level: AlertLevel
    metric_name: str
    current_value: float
    threshold_value: float
    message: str
    description: str
    channels: List[AlertChannel]
    acknowledged: bool = False
    resolved: bool = False
    escalated: bool = False
    escalation_count: int = 0

@dataclass
class AlertingConfig:
    """Alerting system configuration"""
    email_smtp_server: str = "smtp.gmail.com"
    email_smtp_port: int = 587
    email_username: str = ""
    email_password: str = ""
    email_from: str = ""
    email_to: List[str] = None
    slack_webhook_url: str = ""
    webhook_urls: List[str] = None
    escalation_delay_minutes: int = 60
    max_escalations: int = 3
    
    def __post_init__(self):
        if self.email_to is None:
            self.email_to = []
        if self.webhook_urls is None:
            self.webhook_urls = []

class DatabaseHealthMonitor:
    """Monitor database connectivity and performance"""
    
    def __init__(self, mongo_url: str = "mongodb://localhost:27017", db_name: str = "career_platform"):
        self.mongo_url = mongo_url
        self.db_name = db_name
        self.client = None
        self.db = None
        self.logger = logging.getLogger(__name__)
    
    async def check_connectivity(self) -> Dict[str, Any]:
        """Check database connectivity"""
        try:
            if not self.client:
                self.client = AsyncIOMotorClient(self.mongo_url)
                self.db = self.client[self.db_name]
            
            start_time = datetime.utcnow()
            await self.client.admin.command('ping')
            end_time = datetime.utcnow()
            
            response_time = (end_time - start_time).total_seconds() * 1000  # ms
            
            return {
                'connected': True,
                'response_time_ms': response_time,
                'timestamp': datetime.utcnow()
            }
            
        except Exception as e:
            return {
                'connected': False,
                'error': str(e),
                'response_time_ms': None,
                'timestamp': datetime.utcnow()
            }
    
    async def check_performance_metrics(self) -> Dict[str, Any]:
        """Check database performance metrics"""
        try:
            if not self.client:
                return {'error': 'No database connection'}
            
            # Get server status
            server_status = await self.db.command('serverStatus')
            
            # Get collection stats
            careers_stats = await self.db.command('collStats', 'careers')
            
            metrics = {
                'connections': {
                    'current': server_status.get('connections', {}).get('current', 0),
                    'available': server_status.get('connections', {}).get('available', 0)
                },
                'operations': {
                    'insert': server_status.get('opcounters', {}).get('insert', 0),
                    'query': server_status.get('opcounters', {}).get('query', 0),
                    'update': server_status.get('opcounters', {}).get('update', 0),
                    'delete': server_status.get('opcounters', {}).get('delete', 0)
                },
                'memory': {
                    'resident_mb': server_status.get('mem', {}).get('resident', 0),
                    'virtual_mb': server_status.get('mem', {}).get('virtual', 0)
                },
                'collection_stats': {
                    'document_count': careers_stats.get('count', 0),
                    'storage_size_mb': careers_stats.get('storageSize', 0) / (1024 * 1024),
                    'index_size_mb': careers_stats.get('totalIndexSize', 0) / (1024 * 1024)
                },
                'timestamp': datetime.utcnow()
            }
            
            return metrics
            
        except Exception as e:
            self.logger.error(f"Error checking performance metrics: {e}")
            return {'error': str(e), 'timestamp': datetime.utcnow()}

class SystemHealthMonitor:
    """Monitor system resources and health"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def get_system_metrics(self) -> Dict[str, Any]:
        """Get system resource metrics"""
        try:
            return {
                'cpu_percent': psutil.cpu_percent(interval=1),
                'memory_percent': psutil.virtual_memory().percent,
                'disk_percent': psutil.disk_usage('/').percent,
                'load_average': os.getloadavg() if hasattr(os, 'getloadavg') else [0, 0, 0],
                'timestamp': datetime.utcnow()
            }
        except Exception as e:
            self.logger.error(f"Error getting system metrics: {e}")
            return {'error': str(e), 'timestamp': datetime.utcnow()}

class NotificationService:
    """Handle alert notifications across different channels"""
    
    def __init__(self, config: AlertingConfig):
        self.config = config
        self.logger = logging.getLogger(__name__)
    
    async def send_alert(self, alert: Alert) -> Dict[AlertChannel, bool]:
        """Send alert through configured channels"""
        results = {}
        
        for channel in alert.channels:
            try:
                if channel == AlertChannel.EMAIL:
                    results[channel] = await self._send_email_alert(alert)
                elif channel == AlertChannel.SLACK:
                    results[channel] = await self._send_slack_alert(alert)
                elif channel == AlertChannel.WEBHOOK:
                    results[channel] = await self._send_webhook_alert(alert)
                elif channel == AlertChannel.LOG:
                    results[channel] = self._send_log_alert(alert)
                elif channel == AlertChannel.CONSOLE:
                    results[channel] = self._send_console_alert(alert)
                else:
                    results[channel] = False
                    
            except Exception as e:
                self.logger.error(f"Error sending alert via {channel}: {e}")
                results[channel] = False
        
        return results
    
    async def _send_email_alert(self, alert: Alert) -> bool:
        """Send email alert"""
        try:
            if not self.config.email_username or not self.config.email_to:
                self.logger.warning("Email configuration incomplete")
                return False
            
            msg = MIMEMultipart()
            msg['From'] = self.config.email_from or self.config.email_username
            msg['To'] = ', '.join(self.config.email_to)
            msg['Subject'] = f"[{alert.level.value}] Career Platform Alert: {alert.metric_name}"
            
            body = f"""
Career Platform Alert

Alert Level: {alert.level.value}
Metric: {alert.metric_name}
Current Value: {alert.current_value}
Threshold: {alert.threshold_value}
Time: {alert.timestamp.strftime('%Y-%m-%d %H:%M:%S UTC')}

Message: {alert.message}

Description: {alert.description}

Alert ID: {alert.id}

Please investigate and take appropriate action.
            """
            
            msg.attach(MIMEText(body, 'plain'))
            
            server = smtplib.SMTP(self.config.email_smtp_server, self.config.email_smtp_port)
            server.starttls()
            server.login(self.config.email_username, self.config.email_password)
            
            text = msg.as_string()
            server.sendmail(self.config.email_username, self.config.email_to, text)
            server.quit()
            
            self.logger.info(f"Email alert sent for {alert.id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to send email alert: {e}")
            return False
    
    async def _send_slack_alert(self, alert: Alert) -> bool:
        """Send Slack alert"""
        try:
            if not self.config.slack_webhook_url:
                self.logger.warning("Slack webhook URL not configured")
                return False
            
            # Color coding for different alert levels
            color_map = {
                AlertLevel.INFO: "#36a64f",      # Green
                AlertLevel.WARNING: "#ff9500",   # Orange
                AlertLevel.ERROR: "#ff0000",     # Red
                AlertLevel.CRITICAL: "#8B0000"   # Dark Red
            }
            
            payload = {
                "attachments": [
                    {
                        "color": color_map.get(alert.level, "#36a64f"),
                        "title": f"{alert.level.value} Alert: {alert.metric_name}",
                        "text": alert.message,
                        "fields": [
                            {
                                "title": "Current Value",
                                "value": str(alert.current_value),
                                "short": True
                            },
                            {
                                "title": "Threshold",
                                "value": str(alert.threshold_value),
                                "short": True
                            },
                            {
                                "title": "Time",
                                "value": alert.timestamp.strftime('%Y-%m-%d %H:%M:%S UTC'),
                                "short": True
                            },
                            {
                                "title": "Alert ID",
                                "value": alert.id,
                                "short": True
                            }
                        ],
                        "footer": "Career Platform Monitoring",
                        "ts": int(alert.timestamp.timestamp())
                    }
                ]
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(self.config.slack_webhook_url, json=payload) as response:
                    if response.status == 200:
                        self.logger.info(f"Slack alert sent for {alert.id}")
                        return True
                    else:
                        self.logger.error(f"Slack alert failed with status {response.status}")
                        return False
                        
        except Exception as e:
            self.logger.error(f"Failed to send Slack alert: {e}")
            return False
    
    async def _send_webhook_alert(self, alert: Alert) -> bool:
        """Send webhook alert"""
        try:
            if not self.config.webhook_urls:
                return True  # No webhooks configured, consider success
            
            alert_data = {
                "alert_id": alert.id,
                "timestamp": alert.timestamp.isoformat(),
                "level": alert.level.value,
                "metric_name": alert.metric_name,
                "current_value": alert.current_value,
                "threshold_value": alert.threshold_value,
                "message": alert.message,
                "description": alert.description
            }
            
            success_count = 0
            async with aiohttp.ClientSession() as session:
                for webhook_url in self.config.webhook_urls:
                    try:
                        async with session.post(webhook_url, json=alert_data) as response:
                            if response.status == 200:
                                success_count += 1
                            else:
                                self.logger.error(f"Webhook {webhook_url} failed with status {response.status}")
                    except Exception as e:
                        self.logger.error(f"Webhook {webhook_url} failed: {e}")
            
            if success_count > 0:
                self.logger.info(f"Webhook alerts sent to {success_count}/{len(self.config.webhook_urls)} endpoints")
                return True
            else:
                return False
                
        except Exception as e:
            self.logger.error(f"Failed to send webhook alerts: {e}")
            return False
    
    def _send_log_alert(self, alert: Alert) -> bool:
        """Send log alert"""
        try:
            log_level = {
                AlertLevel.INFO: logging.INFO,
                AlertLevel.WARNING: logging.WARNING,
                AlertLevel.ERROR: logging.ERROR,
                AlertLevel.CRITICAL: logging.CRITICAL
            }.get(alert.level, logging.INFO)
            
            self.logger.log(log_level, f"ALERT [{alert.id}] {alert.level.value}: {alert.message} "
                                      f"(Current: {alert.current_value}, Threshold: {alert.threshold_value})")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to send log alert: {e}")
            return False
    
    def _send_console_alert(self, alert: Alert) -> bool:
        """Send console alert"""
        try:
            emoji_map = {
                AlertLevel.INFO: "ℹ️",
                AlertLevel.WARNING: "⚠️",
                AlertLevel.ERROR: "❌",
                AlertLevel.CRITICAL: "🚨"
            }
            
            emoji = emoji_map.get(alert.level, "ℹ️")
            print(f"\n{emoji} [{alert.timestamp.strftime('%H:%M:%S')}] {alert.level.value} ALERT")
            print(f"   Metric: {alert.metric_name}")
            print(f"   Message: {alert.message}")
            print(f"   Current: {alert.current_value} | Threshold: {alert.threshold_value}")
            print(f"   Alert ID: {alert.id}")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to send console alert: {e}")
            return False

class AlertingSystem:
    """Main alerting system orchestrator"""
    
    def __init__(self, config: AlertingConfig):
        self.config = config
        self.thresholds: List[AlertThreshold] = []
        self.active_alerts: Dict[str, Alert] = {}
        self.alert_history: List[Alert] = []
        self.last_alert_times: Dict[str, datetime] = {}
        
        # Initialize components
        self.db_monitor = DatabaseHealthMonitor()
        self.system_monitor = SystemHealthMonitor()
        self.notification_service = NotificationService(config)
        
        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('monitoring/alerting_system.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
        # Setup default thresholds
        self._setup_default_thresholds()
    
    def _setup_default_thresholds(self):
        """Setup default alert thresholds"""
        default_thresholds = [
            # Data Quality Thresholds
            AlertThreshold(
                metric_name="overall_quality_score",
                threshold_value=85.0,
                comparison_operator="<",
                level=AlertLevel.WARNING,
                channels=[AlertChannel.EMAIL, AlertChannel.SLACK, AlertChannel.LOG],
                cooldown_minutes=30,
                description="Overall data quality score below acceptable threshold"
            ),
            AlertThreshold(
                metric_name="overall_quality_score",
                threshold_value=70.0,
                comparison_operator="<",
                level=AlertLevel.CRITICAL,
                channels=[AlertChannel.EMAIL, AlertChannel.SLACK, AlertChannel.CONSOLE],
                cooldown_minutes=15,
                description="Overall data quality score critically low"
            ),
            AlertThreshold(
                metric_name="schema_violations",
                threshold_value=5,
                comparison_operator=">",
                level=AlertLevel.ERROR,
                channels=[AlertChannel.EMAIL, AlertChannel.LOG],
                cooldown_minutes=60,
                description="Schema violations detected"
            ),
            AlertThreshold(
                metric_name="placeholder_content",
                threshold_value=0,
                comparison_operator=">",
                level=AlertLevel.CRITICAL,
                channels=[AlertChannel.EMAIL, AlertChannel.SLACK, AlertChannel.CONSOLE],
                cooldown_minutes=5,
                description="Placeholder content detected in production data"
            ),
            
            # Database Performance Thresholds
            AlertThreshold(
                metric_name="db_response_time_ms",
                threshold_value=1000,
                comparison_operator=">",
                level=AlertLevel.WARNING,
                channels=[AlertChannel.LOG, AlertChannel.CONSOLE],
                cooldown_minutes=15,
                description="Database response time high"
            ),
            AlertThreshold(
                metric_name="db_response_time_ms",
                threshold_value=5000,
                comparison_operator=">",
                level=AlertLevel.ERROR,
                channels=[AlertChannel.EMAIL, AlertChannel.SLACK],
                cooldown_minutes=10,
                description="Database response time critically high"
            ),
            AlertThreshold(
                metric_name="db_connectivity",
                threshold_value=0,
                comparison_operator="==",
                level=AlertLevel.CRITICAL,
                channels=[AlertChannel.EMAIL, AlertChannel.SLACK, AlertChannel.CONSOLE],
                cooldown_minutes=5,
                description="Database connectivity lost"
            ),
            
            # System Resource Thresholds
            AlertThreshold(
                metric_name="cpu_percent",
                threshold_value=80.0,
                comparison_operator=">",
                level=AlertLevel.WARNING,
                channels=[AlertChannel.LOG],
                cooldown_minutes=30,
                description="High CPU usage detected"
            ),
            AlertThreshold(
                metric_name="memory_percent",
                threshold_value=85.0,
                comparison_operator=">",
                level=AlertLevel.WARNING,
                channels=[AlertChannel.LOG, AlertChannel.EMAIL],
                cooldown_minutes=30,
                description="High memory usage detected"
            ),
            AlertThreshold(
                metric_name="disk_percent",
                threshold_value=90.0,
                comparison_operator=">",
                level=AlertLevel.ERROR,
                channels=[AlertChannel.EMAIL, AlertChannel.SLACK],
                cooldown_minutes=60,
                description="Disk space critically low"
            )
        ]
        
        self.thresholds.extend(default_thresholds)
    
    def add_threshold(self, threshold: AlertThreshold):
        """Add custom alert threshold"""
        self.thresholds.append(threshold)
        self.logger.info(f"Added alert threshold for {threshold.metric_name}")
    
    def remove_threshold(self, metric_name: str, level: AlertLevel = None):
        """Remove alert threshold(s)"""
        original_count = len(self.thresholds)
        
        if level:
            self.thresholds = [t for t in self.thresholds 
                             if not (t.metric_name == metric_name and t.level == level)]
        else:
            self.thresholds = [t for t in self.thresholds if t.metric_name != metric_name]
        
        removed_count = original_count - len(self.thresholds)
        self.logger.info(f"Removed {removed_count} threshold(s) for {metric_name}")
    
    def _should_send_alert(self, threshold: AlertThreshold) -> bool:
        """Check if alert should be sent based on cooldown"""
        key = f"{threshold.metric_name}_{threshold.level.value}"
        last_alert_time = self.last_alert_times.get(key)
        
        if not last_alert_time:
            return True
        
        cooldown_delta = timedelta(minutes=threshold.cooldown_minutes)
        return datetime.utcnow() - last_alert_time > cooldown_delta
    
    def _evaluate_threshold(self, metric_name: str, current_value: float, threshold: AlertThreshold) -> bool:
        """Evaluate if threshold condition is met"""
        try:
            if threshold.comparison_operator == '<':
                return current_value < threshold.threshold_value
            elif threshold.comparison_operator == '>':
                return current_value > threshold.threshold_value
            elif threshold.comparison_operator == '<=':
                return current_value <= threshold.threshold_value
            elif threshold.comparison_operator == '>=':
                return current_value >= threshold.threshold_value
            elif threshold.comparison_operator == '==':
                return current_value == threshold.threshold_value
            elif threshold.comparison_operator == '!=':
                return current_value != threshold.threshold_value
            else:
                self.logger.error(f"Unknown comparison operator: {threshold.comparison_operator}")
                return False
        except Exception as e:
            self.logger.error(f"Error evaluating threshold: {e}")
            return False
    
    async def check_metrics_and_alert(self, metrics: Dict[str, Any]):
        """Check metrics against thresholds and send alerts"""
        for threshold in self.thresholds:
            if threshold.metric_name not in metrics:
                continue
            
            current_value = metrics[threshold.metric_name]
            
            # Skip if value is None or not numeric
            if current_value is None or not isinstance(current_value, (int, float)):
                continue
            
            # Check if threshold is breached
            if self._evaluate_threshold(threshold.metric_name, current_value, threshold):
                # Check cooldown
                if not self._should_send_alert(threshold):
                    continue
                
                # Create alert
                alert_id = f"{threshold.metric_name}_{threshold.level.value}_{int(datetime.utcnow().timestamp())}"
                alert = Alert(
                    id=alert_id,
                    timestamp=datetime.utcnow(),
                    level=threshold.level,
                    metric_name=threshold.metric_name,
                    current_value=current_value,
                    threshold_value=threshold.threshold_value,
                    message=f"{threshold.metric_name} {threshold.comparison_operator} {threshold.threshold_value} "
                           f"(current: {current_value})",
                    description=threshold.description,
                    channels=threshold.channels
                )
                
                # Send alert
                await self._send_alert(alert)
                
                # Update tracking
                key = f"{threshold.metric_name}_{threshold.level.value}"
                self.last_alert_times[key] = datetime.utcnow()
                self.active_alerts[alert_id] = alert
                self.alert_history.append(alert)
                
                # Keep history manageable
                if len(self.alert_history) > 1000:
                    self.alert_history = self.alert_history[-500:]
    
    async def _send_alert(self, alert: Alert):
        """Send alert through notification service"""
        try:
            results = await self.notification_service.send_alert(alert)
            
            success_channels = [channel for channel, success in results.items() if success]
            failed_channels = [channel for channel, success in results.items() if not success]
            
            if success_channels:
                self.logger.info(f"Alert {alert.id} sent successfully via: {success_channels}")
            
            if failed_channels:
                self.logger.error(f"Alert {alert.id} failed to send via: {failed_channels}")
            
            # Schedule escalation if critical and some channels failed
            if alert.level == AlertLevel.CRITICAL and failed_channels:
                await self._schedule_escalation(alert)
                
        except Exception as e:
            self.logger.error(f"Error sending alert {alert.id}: {e}")
    
    async def _schedule_escalation(self, alert: Alert):
        """Schedule alert escalation"""
        try:
            # Simple escalation: retry after delay
            await asyncio.sleep(self.config.escalation_delay_minutes * 60)
            
            if alert.escalation_count < self.config.max_escalations:
                alert.escalation_count += 1
                alert.escalated = True
                
                # Add more channels for escalation
                escalation_channels = list(set(alert.channels + [AlertChannel.EMAIL, AlertChannel.CONSOLE]))
                alert.channels = escalation_channels
                
                self.logger.warning(f"Escalating alert {alert.id} (attempt {alert.escalation_count})")
                await self._send_alert(alert)
                
        except Exception as e:
            self.logger.error(f"Error escalating alert {alert.id}: {e}")
    
    async def run_monitoring_cycle(self):
        """Run a complete monitoring cycle"""
        try:
            self.logger.info("🔍 Starting monitoring cycle...")
            
            # Collect all metrics
            metrics = {}
            
            # Database health metrics
            db_health = await self.db_monitor.check_connectivity()
            if db_health['connected']:
                metrics['db_connectivity'] = 1
                metrics['db_response_time_ms'] = db_health['response_time_ms']
                
                # Get performance metrics
                perf_metrics = await self.db_monitor.check_performance_metrics()
                if 'error' not in perf_metrics:
                    metrics.update({
                        'db_connections_current': perf_metrics['connections']['current'],
                        'db_connections_available': perf_metrics['connections']['available'],
                        'db_document_count': perf_metrics['collection_stats']['document_count'],
                        'db_storage_size_mb': perf_metrics['collection_stats']['storage_size_mb']
                    })
            else:
                metrics['db_connectivity'] = 0
                metrics['db_response_time_ms'] = None
            
            # System metrics
            system_metrics = self.system_monitor.get_system_metrics()
            if 'error' not in system_metrics:
                metrics.update({
                    'cpu_percent': system_metrics['cpu_percent'],
                    'memory_percent': system_metrics['memory_percent'],
                    'disk_percent': system_metrics['disk_percent']
                })
            
            # Check metrics against thresholds
            await self.check_metrics_and_alert(metrics)
            
            self.logger.info("✅ Monitoring cycle completed")
            
        except Exception as e:
            self.logger.error(f"Error in monitoring cycle: {e}")
    
    def get_alert_summary(self) -> Dict[str, Any]:
        """Get summary of alert status"""
        active_count = len(self.active_alerts)
        recent_alerts = [a for a in self.alert_history if a.timestamp > datetime.utcnow() - timedelta(hours=24)]
        
        level_counts = {}
        for alert in recent_alerts:
            level_counts[alert.level.value] = level_counts.get(alert.level.value, 0) + 1
        
        return {
            'active_alerts': active_count,
            'alerts_last_24h': len(recent_alerts),
            'level_breakdown': level_counts,
            'last_check': datetime.utcnow().isoformat()
        }
    
    async def acknowledge_alert(self, alert_id: str) -> bool:
        """Acknowledge an active alert"""
        if alert_id in self.active_alerts:
            self.active_alerts[alert_id].acknowledged = True
            self.logger.info(f"Alert {alert_id} acknowledged")
            return True
        return False
    
    async def resolve_alert(self, alert_id: str) -> bool:
        """Resolve an active alert"""
        if alert_id in self.active_alerts:
            self.active_alerts[alert_id].resolved = True
            del self.active_alerts[alert_id]
            self.logger.info(f"Alert {alert_id} resolved")
            return True
        return False

async def main():
    """Main function to run the alerting system"""
    print("🚀 Starting Alerting System")
    print("=" * 50)
    
    # Load configuration from environment or config file
    config = AlertingConfig(
        email_username=os.getenv('ALERT_EMAIL_USERNAME', ''),
        email_password=os.getenv('ALERT_EMAIL_PASSWORD', ''),
        email_from=os.getenv('ALERT_EMAIL_FROM', ''),
        email_to=os.getenv('ALERT_EMAIL_TO', '').split(',') if os.getenv('ALERT_EMAIL_TO') else [],
        slack_webhook_url=os.getenv('ALERT_SLACK_WEBHOOK', ''),
        webhook_urls=os.getenv('ALERT_WEBHOOK_URLS', '').split(',') if os.getenv('ALERT_WEBHOOK_URLS') else []
    )
    
    # Initialize alerting system
    alerting_system = AlertingSystem(config)
    
    print("📊 Alerting system initialized with default thresholds")
    print(f"   - {len(alerting_system.thresholds)} thresholds configured")
    print(f"   - Email alerts: {'✅' if config.email_username else '❌'}")
    print(f"   - Slack alerts: {'✅' if config.slack_webhook_url else '❌'}")
    
    try:
        # Run continuous monitoring
        print("\n🔄 Starting continuous monitoring...")
        while True:
            await alerting_system.run_monitoring_cycle()
            
            # Print summary
            summary = alerting_system.get_alert_summary()
            print(f"📈 Active alerts: {summary['active_alerts']} | "
                  f"Last 24h: {summary['alerts_last_24h']}")
            
            # Wait before next cycle
            await asyncio.sleep(300)  # 5 minutes
            
    except KeyboardInterrupt:
        print("\n🛑 Alerting system stopped by user")
    except Exception as e:
        print(f"❌ Alerting system error: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(main())