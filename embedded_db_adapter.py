#!/usr/bin/env python3
"""
Embedded Database Adapter
========================
Provides MongoDB-like interface using TinyDB for development/testing
"""

from tinydb import TinyDB, Query
from typing import List, Dict, Any
import uuid
from datetime import datetime

class EmbeddedCareerDB:
    def __init__(self, db_path: str = "embedded_careers.json"):
        self.db = TinyDB(db_path)
        self.careers = self.db.table('careers')
    
    def insert_career(self, career_data: Dict[str, Any]) -> str:
        """Insert a career record"""
        if 'career_id' not in career_data:
            career_data['career_id'] = str(uuid.uuid4())
        
        career_data['created_at'] = datetime.utcnow().isoformat()
        career_data['updated_at'] = datetime.utcnow().isoformat()
        
        self.careers.insert(career_data)
        return career_data['career_id']
    
    def find_careers(self, query: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Find careers matching query"""
        if not query:
            return self.careers.all()
        
        Career = Query()
        results = []
        
        for key, value in query.items():
            if hasattr(Career, key):
                results = self.careers.search(getattr(Career, key) == value)
                break
        
        return results
    
    def count_careers(self) -> int:
        """Count total careers"""
        return len(self.careers)
    
    def clear_careers(self):
        """Clear all careers"""
        self.careers.truncate()

# Global instance
embedded_db = EmbeddedCareerDB()
