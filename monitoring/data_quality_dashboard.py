#!/usr/bin/env python3
"""
Data Quality Dashboard for Career Platform
Phase 3: Deploy Quality Monitoring System

This module provides real-time monitoring of data quality metrics,
tracking key indicators and generating alerts for quality degradation.
"""

import asyncio
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from pathlib import Path
import statistics

from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import dash
from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc

# Import models
import sys
sys.path.append(str(Path(__file__).parent.parent))
from backend.models import CareerModel, SkillModel

@dataclass
class QualityMetrics:
    """Data quality metrics structure"""
    timestamp: datetime
    total_records: int
    completeness_score: float
    consistency_score: float
    accuracy_score: float
    uniqueness_score: float
    freshness_score: float
    overall_score: float
    field_completeness: Dict[str, float]
    schema_violations: int
    duplicate_records: int
    placeholder_content: int
    data_growth_rate: float

class DataQualityMonitor:
    """Real-time data quality monitoring system"""
    
    def __init__(self, mongo_url: str = "mongodb://localhost:27017", db_name: str = "career_platform"):
        self.mongo_url = mongo_url
        self.db_name = db_name
        self.client = None
        self.db = None
        self.metrics_history: List[QualityMetrics] = []
        self.alert_thresholds = {
            'overall_score': 85.0,
            'completeness_score': 90.0,
            'consistency_score': 95.0,
            'schema_violations': 5,
            'duplicate_records': 10,
            'placeholder_content': 1
        }
        
        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('monitoring/quality_monitor.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)

    async def connect_database(self) -> bool:
        """Initialize database connection and Beanie ODM"""
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

    async def calculate_completeness_score(self) -> Dict[str, Any]:
        """Calculate field completeness metrics"""
        try:
            careers = await CareerModel.find_all().to_list()
            total_records = len(careers)
            
            if total_records == 0:
                return {'overall': 0.0, 'fields': {}}
            
            # Required fields based on CareerModel
            required_fields = [
                'title', 'description', 'requiredTechnicalSkills', 'requiredSoftSkills',
                'experienceLevel', 'salaryMin', 'salaryMax', 'careerType'
            ]
            
            field_completeness = {}
            total_completeness = 0
            
            for field in required_fields:
                complete_count = 0
                for career in careers:
                    value = getattr(career, field, None)
                    if value is not None and value != '' and value != []:
                        complete_count += 1
                
                completeness_pct = (complete_count / total_records) * 100
                field_completeness[field] = completeness_pct
                total_completeness += completeness_pct
            
            overall_completeness = total_completeness / len(required_fields)
            
            return {
                'overall': overall_completeness,
                'fields': field_completeness,
                'total_records': total_records
            }
            
        except Exception as e:
            self.logger.error(f"Error calculating completeness score: {e}")
            return {'overall': 0.0, 'fields': {}}

    async def calculate_consistency_score(self) -> Dict[str, Any]:
        """Calculate data consistency metrics"""
        try:
            careers = await CareerModel.find_all().to_list()
            total_records = len(careers)
            
            if total_records == 0:
                return {'overall': 100.0, 'violations': 0}
            
            violations = 0
            
            # Check salary consistency
            for career in careers:
                if career.salaryMin and career.salaryMax:
                    if career.salaryMin > career.salaryMax:
                        violations += 1
                
                # Check experience years consistency
                if career.minYearsExperience and career.maxYearsExperience:
                    if career.minYearsExperience > career.maxYearsExperience:
                        violations += 1
                
                # Check for empty required lists
                if not career.requiredTechnicalSkills:
                    violations += 1
                if not career.requiredSoftSkills:
                    violations += 1
            
            consistency_score = max(0, 100 - (violations / total_records * 100))
            
            return {
                'overall': consistency_score,
                'violations': violations,
                'total_records': total_records
            }
            
        except Exception as e:
            self.logger.error(f"Error calculating consistency score: {e}")
            return {'overall': 0.0, 'violations': 0}

    async def calculate_uniqueness_score(self) -> Dict[str, Any]:
        """Calculate data uniqueness metrics"""
        try:
            careers = await CareerModel.find_all().to_list()
            total_records = len(careers)
            
            if total_records == 0:
                return {'overall': 100.0, 'duplicates': 0}
            
            # Check for duplicate titles
            titles = [career.title for career in careers if career.title]
            unique_titles = set(titles)
            duplicates = len(titles) - len(unique_titles)
            
            uniqueness_score = max(0, 100 - (duplicates / total_records * 100))
            
            return {
                'overall': uniqueness_score,
                'duplicates': duplicates,
                'total_records': total_records
            }
            
        except Exception as e:
            self.logger.error(f"Error calculating uniqueness score: {e}")
            return {'overall': 0.0, 'duplicates': 0}

    async def detect_placeholder_content(self) -> Dict[str, Any]:
        """Detect placeholder patterns in career data"""
        try:
            careers = await CareerModel.find_all().to_list()
            total_records = len(careers)
            
            if total_records == 0:
                return {'count': 0, 'percentage': 0.0}
            
            placeholder_patterns = [
                r'A brief description of the .+ role',
                r'Technical Skill \d+',
                r'Skill \d+',
                r'Brief description',
                r'TODO',
                r'TBD',
                r'Placeholder',
                r'Lorem ipsum',
                r'Test data'
            ]
            
            placeholder_count = 0
            
            for career in careers:
                # Check description
                if career.description:
                    for pattern in placeholder_patterns:
                        import re
                        if re.search(pattern, career.description, re.IGNORECASE):
                            placeholder_count += 1
                            break
                
                # Check technical skills
                if career.requiredTechnicalSkills:
                    for skill in career.requiredTechnicalSkills:
                        for pattern in placeholder_patterns:
                            if re.search(pattern, skill, re.IGNORECASE):
                                placeholder_count += 1
                                break
            
            placeholder_percentage = (placeholder_count / total_records) * 100
            
            return {
                'count': placeholder_count,
                'percentage': placeholder_percentage,
                'total_records': total_records
            }
            
        except Exception as e:
            self.logger.error(f"Error detecting placeholder content: {e}")
            return {'count': 0, 'percentage': 0.0}

    async def calculate_freshness_score(self) -> Dict[str, Any]:
        """Calculate data freshness metrics"""
        try:
            careers = await CareerModel.find_all().to_list()
            
            if not careers:
                return {'overall': 0.0, 'avg_age_days': 0}
            
            now = datetime.utcnow()
            ages = []
            
            for career in careers:
                if career.updated_at:
                    age = (now - career.updated_at).days
                    ages.append(age)
            
            if not ages:
                return {'overall': 0.0, 'avg_age_days': 0}
            
            avg_age = statistics.mean(ages)
            
            # Freshness score: 100 for data updated today, decreasing over time
            freshness_score = max(0, 100 - (avg_age / 7 * 10))  # 10 points per week
            
            return {
                'overall': freshness_score,
                'avg_age_days': avg_age,
                'oldest_days': max(ages),
                'newest_days': min(ages)
            }
            
        except Exception as e:
            self.logger.error(f"Error calculating freshness score: {e}")
            return {'overall': 0.0, 'avg_age_days': 0}

    async def collect_quality_metrics(self) -> QualityMetrics:
        """Collect comprehensive quality metrics"""
        try:
            self.logger.info("🔍 Collecting quality metrics...")
            
            # Calculate individual metrics
            completeness = await self.calculate_completeness_score()
            consistency = await self.calculate_consistency_score()
            uniqueness = await self.calculate_uniqueness_score()
            placeholder = await self.detect_placeholder_content()
            freshness = await self.calculate_freshness_score()
            
            # Calculate overall score
            scores = [
                completeness['overall'],
                consistency['overall'],
                uniqueness['overall'],
                max(0, 100 - placeholder['percentage']),  # Invert placeholder percentage
                freshness['overall']
            ]
            overall_score = statistics.mean(scores)
            
            # Calculate data growth rate
            growth_rate = 0.0
            if len(self.metrics_history) > 0:
                prev_count = self.metrics_history[-1].total_records
                current_count = completeness['total_records']
                if prev_count > 0:
                    growth_rate = ((current_count - prev_count) / prev_count) * 100
            
            metrics = QualityMetrics(
                timestamp=datetime.utcnow(),
                total_records=completeness['total_records'],
                completeness_score=completeness['overall'],
                consistency_score=consistency['overall'],
                accuracy_score=95.0,  # Placeholder - would need external validation
                uniqueness_score=uniqueness['overall'],
                freshness_score=freshness['overall'],
                overall_score=overall_score,
                field_completeness=completeness['fields'],
                schema_violations=consistency['violations'],
                duplicate_records=uniqueness['duplicates'],
                placeholder_content=placeholder['count'],
                data_growth_rate=growth_rate
            )
            
            self.metrics_history.append(metrics)
            
            # Keep only last 100 metrics for memory management
            if len(self.metrics_history) > 100:
                self.metrics_history = self.metrics_history[-100:]
            
            self.logger.info(f"✅ Quality metrics collected - Overall Score: {overall_score:.1f}")
            return metrics
            
        except Exception as e:
            self.logger.error(f"Error collecting quality metrics: {e}")
            raise

    def check_alert_conditions(self, metrics: QualityMetrics) -> List[Dict[str, Any]]:
        """Check if any alert conditions are met"""
        alerts = []
        
        # Overall score alert
        if metrics.overall_score < self.alert_thresholds['overall_score']:
            alerts.append({
                'level': 'WARNING',
                'metric': 'Overall Quality Score',
                'current_value': metrics.overall_score,
                'threshold': self.alert_thresholds['overall_score'],
                'message': f"Overall quality score ({metrics.overall_score:.1f}) below threshold ({self.alert_thresholds['overall_score']})"
            })
        
        # Completeness alert
        if metrics.completeness_score < self.alert_thresholds['completeness_score']:
            alerts.append({
                'level': 'WARNING',
                'metric': 'Data Completeness',
                'current_value': metrics.completeness_score,
                'threshold': self.alert_thresholds['completeness_score'],
                'message': f"Data completeness ({metrics.completeness_score:.1f}%) below threshold ({self.alert_thresholds['completeness_score']}%)"
            })
        
        # Schema violations alert
        if metrics.schema_violations > self.alert_thresholds['schema_violations']:
            alerts.append({
                'level': 'ERROR',
                'metric': 'Schema Violations',
                'current_value': metrics.schema_violations,
                'threshold': self.alert_thresholds['schema_violations'],
                'message': f"Schema violations ({metrics.schema_violations}) exceed threshold ({self.alert_thresholds['schema_violations']})"
            })
        
        # Placeholder content alert
        if metrics.placeholder_content > self.alert_thresholds['placeholder_content']:
            alerts.append({
                'level': 'CRITICAL',
                'metric': 'Placeholder Content',
                'current_value': metrics.placeholder_content,
                'threshold': self.alert_thresholds['placeholder_content'],
                'message': f"Placeholder content detected ({metrics.placeholder_content} records) - immediate attention required"
            })
        
        return alerts

    def save_metrics_to_file(self, metrics: QualityMetrics, filepath: str = "monitoring/quality_metrics.json"):
        """Save metrics to JSON file for persistence"""
        try:
            Path(filepath).parent.mkdir(parents=True, exist_ok=True)
            
            # Load existing metrics
            existing_metrics = []
            if Path(filepath).exists():
                with open(filepath, 'r') as f:
                    existing_metrics = json.load(f)
            
            # Add new metrics
            metrics_dict = asdict(metrics)
            metrics_dict['timestamp'] = metrics.timestamp.isoformat()
            existing_metrics.append(metrics_dict)
            
            # Keep only last 1000 entries
            if len(existing_metrics) > 1000:
                existing_metrics = existing_metrics[-1000:]
            
            # Save to file
            with open(filepath, 'w') as f:
                json.dump(existing_metrics, f, indent=2, default=str)
            
            self.logger.info(f"📊 Metrics saved to {filepath}")
            
        except Exception as e:
            self.logger.error(f"Error saving metrics to file: {e}")

    async def generate_quality_report(self, metrics: QualityMetrics) -> str:
        """Generate a comprehensive quality report"""
        report = f"""
# Data Quality Report
Generated: {metrics.timestamp.strftime('%Y-%m-%d %H:%M:%S UTC')}

## Overall Quality Score: {metrics.overall_score:.1f}/100

### Key Metrics:
- **Total Records**: {metrics.total_records:,}
- **Completeness**: {metrics.completeness_score:.1f}%
- **Consistency**: {metrics.consistency_score:.1f}%
- **Uniqueness**: {metrics.uniqueness_score:.1f}%
- **Freshness**: {metrics.freshness_score:.1f}%

### Data Quality Issues:
- **Schema Violations**: {metrics.schema_violations}
- **Duplicate Records**: {metrics.duplicate_records}
- **Placeholder Content**: {metrics.placeholder_content}

### Field Completeness:
"""
        
        for field, completeness in metrics.field_completeness.items():
            status = "✅" if completeness >= 95 else "⚠️" if completeness >= 80 else "❌"
            report += f"- {status} **{field}**: {completeness:.1f}%\n"
        
        report += f"""
### Data Growth:
- **Growth Rate**: {metrics.data_growth_rate:+.2f}%

### Recommendations:
"""
        
        if metrics.overall_score < 85:
            report += "- 🚨 **URGENT**: Overall quality below acceptable threshold - immediate action required\n"
        
        if metrics.completeness_score < 90:
            report += "- 📋 **Action Required**: Improve data completeness for critical fields\n"
        
        if metrics.placeholder_content > 0:
            report += "- 🎭 **Critical**: Remove placeholder content immediately\n"
        
        if metrics.schema_violations > 5:
            report += "- 🔧 **Fix**: Address schema violations to maintain data integrity\n"
        
        return report

class QualityDashboard:
    """Interactive dashboard for data quality monitoring"""
    
    def __init__(self, monitor: DataQualityMonitor):
        self.monitor = monitor
        self.app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
        self.setup_layout()
        self.setup_callbacks()

    def setup_layout(self):
        """Setup dashboard layout"""
        self.app.layout = dbc.Container([
            dbc.Row([
                dbc.Col([
                    html.H1("📊 Data Quality Dashboard", className="text-center mb-4"),
                    html.P("Real-time monitoring of career platform data quality", 
                           className="text-center text-muted mb-4")
                ])
            ]),
            
            # Metrics cards
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H4("Overall Score", className="card-title"),
                            html.H2(id="overall-score", className="text-primary"),
                            html.P("Quality Score", className="card-text")
                        ])
                    ])
                ], width=2),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H4("Records", className="card-title"),
                            html.H2(id="total-records", className="text-info"),
                            html.P("Total Careers", className="card-text")
                        ])
                    ])
                ], width=2),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H4("Completeness", className="card-title"),
                            html.H2(id="completeness-score", className="text-success"),
                            html.P("Field Completeness", className="card-text")
                        ])
                    ])
                ], width=2),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H4("Issues", className="card-title"),
                            html.H2(id="total-issues", className="text-warning"),
                            html.P("Data Issues", className="card-text")
                        ])
                    ])
                ], width=2),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H4("Alerts", className="card-title"),
                            html.H2(id="active-alerts", className="text-danger"),
                            html.P("Active Alerts", className="card-text")
                        ])
                    ])
                ], width=2),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H4("Growth", className="card-title"),
                            html.H2(id="growth-rate", className="text-secondary"),
                            html.P("Data Growth", className="card-text")
                        ])
                    ])
                ], width=2)
            ], className="mb-4"),
            
            # Charts
            dbc.Row([
                dbc.Col([
                    dcc.Graph(id="quality-trends")
                ], width=8),
                dbc.Col([
                    dcc.Graph(id="completeness-breakdown")
                ], width=4)
            ], className="mb-4"),
            
            dbc.Row([
                dbc.Col([
                    dcc.Graph(id="issues-breakdown")
                ], width=6),
                dbc.Col([
                    html.Div(id="alerts-panel")
                ], width=6)
            ]),
            
            # Auto-refresh
            dcc.Interval(
                id='interval-component',
                interval=30*1000,  # Update every 30 seconds
                n_intervals=0
            )
        ], fluid=True)

    def setup_callbacks(self):
        """Setup dashboard callbacks"""
        @self.app.callback(
            [Output('overall-score', 'children'),
             Output('total-records', 'children'),
             Output('completeness-score', 'children'),
             Output('total-issues', 'children'),
             Output('active-alerts', 'children'),
             Output('growth-rate', 'children'),
             Output('quality-trends', 'figure'),
             Output('completeness-breakdown', 'figure'),
             Output('issues-breakdown', 'figure'),
             Output('alerts-panel', 'children')],
            [Input('interval-component', 'n_intervals')]
        )
        def update_dashboard(n):
            return self.update_dashboard_data()

    def update_dashboard_data(self):
        """Update dashboard with latest data"""
        try:
            # Get latest metrics
            if not self.monitor.metrics_history:
                return self.get_empty_dashboard()
            
            latest_metrics = self.monitor.metrics_history[-1]
            alerts = self.monitor.check_alert_conditions(latest_metrics)
            
            # Update metric cards
            overall_score = f"{latest_metrics.overall_score:.1f}"
            total_records = f"{latest_metrics.total_records:,}"
            completeness_score = f"{latest_metrics.completeness_score:.1f}%"
            total_issues = latest_metrics.schema_violations + latest_metrics.duplicate_records + latest_metrics.placeholder_content
            active_alerts = len(alerts)
            growth_rate = f"{latest_metrics.data_growth_rate:+.1f}%"
            
            # Create charts
            quality_trends = self.create_quality_trends_chart()
            completeness_breakdown = self.create_completeness_breakdown_chart(latest_metrics)
            issues_breakdown = self.create_issues_breakdown_chart(latest_metrics)
            alerts_panel = self.create_alerts_panel(alerts)
            
            return (overall_score, total_records, completeness_score, str(total_issues), 
                   str(active_alerts), growth_rate, quality_trends, completeness_breakdown, 
                   issues_breakdown, alerts_panel)
            
        except Exception as e:
            self.monitor.logger.error(f"Error updating dashboard: {e}")
            return self.get_empty_dashboard()

    def get_empty_dashboard(self):
        """Return empty dashboard state"""
        empty_fig = go.Figure()
        empty_fig.add_annotation(text="No data available", xref="paper", yref="paper",
                               x=0.5, y=0.5, showarrow=False)
        
        return ("--", "--", "--", "--", "--", "--", empty_fig, empty_fig, empty_fig, 
                html.Div("No alerts"))

    def create_quality_trends_chart(self):
        """Create quality trends over time chart"""
        if len(self.monitor.metrics_history) < 2:
            fig = go.Figure()
            fig.add_annotation(text="Insufficient data for trends", xref="paper", yref="paper",
                             x=0.5, y=0.5, showarrow=False)
            return fig
        
        timestamps = [m.timestamp for m in self.monitor.metrics_history]
        overall_scores = [m.overall_score for m in self.monitor.metrics_history]
        completeness_scores = [m.completeness_score for m in self.monitor.metrics_history]
        consistency_scores = [m.consistency_score for m in self.monitor.metrics_history]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=timestamps, y=overall_scores, name="Overall Score", 
                                line=dict(color='blue', width=3)))
        fig.add_trace(go.Scatter(x=timestamps, y=completeness_scores, name="Completeness", 
                                line=dict(color='green')))
        fig.add_trace(go.Scatter(x=timestamps, y=consistency_scores, name="Consistency", 
                                line=dict(color='orange')))
        
        fig.update_layout(title="Quality Trends Over Time", xaxis_title="Time", 
                         yaxis_title="Score (%)", yaxis=dict(range=[0, 100]))
        
        return fig

    def create_completeness_breakdown_chart(self, metrics: QualityMetrics):
        """Create field completeness breakdown chart"""
        fields = list(metrics.field_completeness.keys())
        completeness = list(metrics.field_completeness.values())
        
        colors = ['green' if c >= 95 else 'orange' if c >= 80 else 'red' for c in completeness]
        
        fig = go.Figure(data=[go.Bar(x=fields, y=completeness, marker_color=colors)])
        fig.update_layout(title="Field Completeness", xaxis_title="Fields", 
                         yaxis_title="Completeness (%)", yaxis=dict(range=[0, 100]))
        fig.update_xaxis(tickangle=45)
        
        return fig

    def create_issues_breakdown_chart(self, metrics: QualityMetrics):
        """Create issues breakdown pie chart"""
        labels = ['Schema Violations', 'Duplicate Records', 'Placeholder Content']
        values = [metrics.schema_violations, metrics.duplicate_records, metrics.placeholder_content]
        
        fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=0.3)])
        fig.update_layout(title="Data Issues Breakdown")
        
        return fig

    def create_alerts_panel(self, alerts: List[Dict[str, Any]]):
        """Create alerts panel"""
        if not alerts:
            return dbc.Alert("✅ No active alerts", color="success")
        
        alert_components = []
        for alert in alerts:
            color = "danger" if alert['level'] == 'CRITICAL' else "warning" if alert['level'] == 'ERROR' else "info"
            alert_components.append(
                dbc.Alert([
                    html.H6(f"{alert['level']}: {alert['metric']}", className="alert-heading"),
                    html.P(alert['message'])
                ], color=color, className="mb-2")
            )
        
        return html.Div(alert_components)

    def run(self, host='127.0.0.1', port=8050, debug=False):
        """Run the dashboard"""
        self.app.run_server(host=host, port=port, debug=debug)

async def main():
    """Main function to run the data quality monitoring system"""
    print("🚀 Starting Data Quality Monitoring System")
    print("=" * 50)
    
    # Initialize monitor
    monitor = DataQualityMonitor()
    
    # Connect to database
    if not await monitor.connect_database():
        print("❌ Failed to connect to database")
        return
    
    # Collect initial metrics
    try:
        metrics = await monitor.collect_quality_metrics()
        
        # Save metrics
        monitor.save_metrics_to_file(metrics)
        
        # Generate report
        report = await monitor.generate_quality_report(metrics)
        
        # Save report
        report_path = "monitoring/quality_report.md"
        Path(report_path).parent.mkdir(parents=True, exist_ok=True)
        with open(report_path, 'w') as f:
            f.write(report)
        
        print(f"📊 Quality report generated: {report_path}")
        
        # Check for alerts
        alerts = monitor.check_alert_conditions(metrics)
        if alerts:
            print(f"🚨 {len(alerts)} alerts detected:")
            for alert in alerts:
                print(f"  - {alert['level']}: {alert['message']}")
        else:
            print("✅ No alerts detected")
        
        print("\n" + "=" * 50)
        print("📈 Data Quality Dashboard available at: http://localhost:8050")
        print("🔄 Monitoring will continue in real-time...")
        
        # Start dashboard
        dashboard = QualityDashboard(monitor)
        
        # Run continuous monitoring in background
        async def continuous_monitoring():
            while True:
                await asyncio.sleep(300)  # 5 minutes
                try:
                    metrics = await monitor.collect_quality_metrics()
                    monitor.save_metrics_to_file(metrics)
                    
                    alerts = monitor.check_alert_conditions(metrics)
                    if alerts:
                        for alert in alerts:
                            monitor.logger.warning(f"ALERT: {alert['message']}")
                            
                except Exception as e:
                    monitor.logger.error(f"Error in continuous monitoring: {e}")
        
        # Start monitoring task
        monitoring_task = asyncio.create_task(continuous_monitoring())
        
        # Run dashboard (this will block)
        dashboard.run(debug=False)
        
    except Exception as e:
        print(f"❌ Error in monitoring system: {e}")
        raise
    finally:
        if monitor.client:
            monitor.client.close()

if __name__ == "__main__":
    asyncio.run(main())