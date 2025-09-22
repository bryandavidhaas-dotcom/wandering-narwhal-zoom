"""
Configuration management for the recommendation engine.

This module defines configuration classes and default values for the
recommendation engine's scoring weights, thresholds, and parameters.
"""

from typing import Dict, Any
from pydantic import BaseModel, Field


class ScoringWeights(BaseModel):
    """
    Weights for different scoring components.
    
    All weights should sum to 1.0 for proper normalization.
    """
    skill_match: float = Field(0.4, ge=0.0, le=1.0, description="Weight for skill matching")
    interest_match: float = Field(0.25, ge=0.0, le=1.0, description="Weight for interest alignment")
    salary_compatibility: float = Field(0.2, ge=0.0, le=1.0, description="Weight for salary compatibility")
    experience_match: float = Field(0.15, ge=0.0, le=1.0, description="Weight for experience level matching")
    
    def validate_weights_sum(self):
        """Validate that weights sum to approximately 1.0."""
        total = self.skill_match + self.interest_match + self.salary_compatibility + self.experience_match
        if abs(total - 1.0) > 0.01:  # Allow small floating point errors
            raise ValueError(f"Weights must sum to 1.0, got {total}")
        return self


class CategorizationThresholds(BaseModel):
    """
    Thresholds for categorizing recommendations into zones.
    
    Attributes:
        safe_zone_min: Minimum score for Safe Zone (high confidence matches)
        stretch_zone_min: Minimum score for Stretch Zone (moderate matches)
        adventure_zone_min: Minimum score for Adventure Zone (exploratory matches)
    """
    safe_zone_min: float = Field(0.7, ge=0.0, le=1.0, description="Minimum score for Safe Zone")
    stretch_zone_min: float = Field(0.5, ge=0.0, le=1.0, description="Minimum score for Stretch Zone")
    adventure_zone_min: float = Field(0.3, ge=0.0, le=1.0, description="Minimum score for Adventure Zone")
    
    def validate_thresholds(self):
        """Validate that thresholds are in descending order."""
        if not (self.safe_zone_min >= self.stretch_zone_min >= self.adventure_zone_min):
            raise ValueError("Thresholds must be in descending order: safe >= stretch >= adventure")
        return self


class FilteringConfig(BaseModel):
    """
    Configuration for filtering logic.
    
    Attributes:
        max_salary_deviation: Maximum deviation from user's salary expectations (as percentage)
        min_skill_overlap: Minimum skill overlap required (as percentage)
        consider_related_skills: Whether to consider related skills in matching
        experience_level_tolerance: How many levels of experience difference to allow
    """
    max_salary_deviation: float = Field(0.3, ge=0.0, le=1.0, description="Max salary deviation (30%)")
    min_skill_overlap: float = Field(0.2, ge=0.0, le=1.0, description="Min skill overlap (20%)")
    consider_related_skills: bool = Field(True, description="Consider related skills in matching")
    experience_level_tolerance: int = Field(1, ge=0, le=3, description="Experience level tolerance")


class ScoringConfig(BaseModel):
    """
    Configuration for scoring algorithms.
    
    Attributes:
        skill_level_multipliers: Multipliers for different skill levels
        mandatory_skill_penalty: Penalty for missing mandatory skills
        certification_bonus: Bonus for having certifications
        recent_experience_bonus: Bonus for recent experience with skills
    """
    skill_level_multipliers: Dict[str, float] = Field(
        default_factory=lambda: {
            "beginner": 0.25,
            "intermediate": 0.5,
            "advanced": 0.75,
            "expert": 1.0
        },
        description="Multipliers for skill proficiency levels"
    )
    mandatory_skill_penalty: float = Field(0.5, ge=0.0, le=1.0, description="Penalty for missing mandatory skills")
    certification_bonus: float = Field(0.1, ge=0.0, le=0.5, description="Bonus for certifications")
    recent_experience_bonus: float = Field(0.05, ge=0.0, le=0.2, description="Bonus for recent skill usage")


class ConsistencyPenaltyConfig(BaseModel):
    """
    Configuration for consistency penalty based on career field mismatches.
    
    Attributes:
        base_penalty: Base penalty for career field mismatch (0.0 to 1.0)
        exploration_level_multiplier: Multiplier based on user's exploration level
        max_penalty: Maximum penalty that can be applied
    """
    base_penalty: float = Field(0.3, ge=0.0, le=1.0, description="Base penalty for field mismatch")
    exploration_level_multiplier: Dict[int, float] = Field(
        default_factory=lambda: {
            1: 2.0,    # Conservative users get high penalty
            2: 1.5,    # Moderate penalty
            3: 1.0,    # Base penalty
            4: 0.7,    # Reduced penalty for adventurous users
            5: 0.4     # Minimal penalty for maximum exploration
        },
        description="Penalty multipliers by exploration level (1-5)"
    )
    max_penalty: float = Field(0.6, ge=0.0, le=1.0, description="Maximum penalty that can be applied")


class RecommendationConfig(BaseModel):
    """
    Main configuration class for the recommendation engine.
    
    Attributes:
        scoring_weights: Weights for different scoring components
        categorization_thresholds: Thresholds for recommendation categories
        filtering_config: Configuration for filtering logic
        scoring_config: Configuration for scoring algorithms
        consistency_penalty_config: Configuration for career field consistency penalties
        max_recommendations: Maximum number of recommendations to return
        min_recommendations: Minimum number of recommendations to return
    """
    scoring_weights: ScoringWeights = Field(default_factory=ScoringWeights)
    categorization_thresholds: CategorizationThresholds = Field(default_factory=CategorizationThresholds)
    filtering_config: FilteringConfig = Field(default_factory=FilteringConfig)
    scoring_config: ScoringConfig = Field(default_factory=ScoringConfig)
    consistency_penalty_config: ConsistencyPenaltyConfig = Field(default_factory=ConsistencyPenaltyConfig)
    max_recommendations: int = Field(20, ge=1, le=100, description="Maximum recommendations to return")
    min_recommendations: int = Field(5, ge=1, le=50, description="Minimum recommendations to return")
    
    # Multi-step architecture parameters
    batch_size: int = Field(20, ge=5, le=50, description="Batch size for multi-call scoring")
    top_n_candidates: int = Field(30, ge=10, le=100, description="Top candidates for final analysis")
    prefilter_limit: int = Field(100, ge=50, le=500, description="Maximum careers after pre-filtering (reduced to prevent prompt overflow)")
    
    def validate_config(self):
        """Validate the entire configuration."""
        self.scoring_weights.validate_weights_sum()
        self.categorization_thresholds.validate_thresholds()
        
        if self.min_recommendations > self.max_recommendations:
            raise ValueError("min_recommendations cannot be greater than max_recommendations")
        
        return self


# Default configuration instance
DEFAULT_CONFIG = RecommendationConfig()