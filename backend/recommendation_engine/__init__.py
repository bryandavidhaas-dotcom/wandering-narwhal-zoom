"""
Recommendation Engine Package

A modular recommendation engine for career matching based on user profiles,
skills, interests, and preferences.
"""

from ..models import UserProfileModel as UserProfile, CareerModel as Career, SkillModel as Skill
from .engine import RecommendationEngine
from .filters import FilterEngine
from .scoring import ScoringEngine
from .categorization import CategorizationEngine

__version__ = "0.1.0"
__all__ = [
    "UserProfile",
    "Career", 
    "Skill",
    "RecommendationEngine",
    "FilterEngine",
    "ScoringEngine",
    "CategorizationEngine"
]