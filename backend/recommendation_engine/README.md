# Career Recommendation Engine

A modular, configurable recommendation engine for career matching based on user profiles, skills, interests, and preferences.

## Overview

This recommendation engine implements a multi-stage process to provide personalized career recommendations:

1. **Multi-stage Filtering**: Filters careers based on salary expectations, skill requirements, and interests
2. **Weighted Scoring**: Scores careers using configurable weights for different factors
3. **Categorization**: Organizes recommendations into Safe Zone, Stretch Zone, and Adventure Zone
4. **Explainability**: Provides detailed reasons for each recommendation

## Architecture

The engine follows a modular architecture with separate components for:

- **Models** (`models.py`): Pydantic data models for validation
- **Configuration** (`config.py`): Configurable weights, thresholds, and parameters
- **Filtering** (`filters.py`): Multi-stage filtering logic
- **Scoring** (`scoring.py`): Weighted scoring algorithms
- **Categorization** (`categorization.py`): Zone-based categorization
- **Engine** (`engine.py`): Main orchestration class
- **Mock Data** (`mock_data.py`): Sample data for testing

## Quick Start

```python
from recommendation_engine import RecommendationEngine
from recommendation_engine.mock_data import MOCK_USER_PROFILE, MOCK_CAREERS, MOCK_SKILLS

# Initialize the engine
engine = RecommendationEngine(skills_db=MOCK_SKILLS)

# Get recommendations
recommendations = engine.get_recommendations(
    user_profile=MOCK_USER_PROFILE,
    available_careers=MOCK_CAREERS,
    limit=10
)

# Print results
for rec in recommendations:
    print(f"{rec.career.title} - {rec.category.value} - Score: {rec.score.total_score:.2f}")
    print(f"Reasons: {', '.join(rec.reasons[:3])}")
    print()
```

## Core Components

### 1. Data Models

The engine uses Pydantic models for data validation and structure:

#### UserProfile
Contains comprehensive user information:
- Personal info (age, location, salary expectations)
- Assessment results (personality traits, work values, interests)
- Professional data (resume, LinkedIn, experience)
- Skills with proficiency levels

#### Career
Represents a career path with:
- Required skills and proficiency levels
- Salary range and market demand
- Description and growth potential
- Related careers

#### Skill
Centralized skill definition with:
- Unique identifier and name
- Category classification
- Related skills mapping

### 2. Filtering System

Multi-stage filtering process:

```python
from recommendation_engine.filters import FilterEngine
from recommendation_engine.config import FilteringConfig

config = FilteringConfig(
    max_salary_deviation=0.3,  # 30% salary deviation allowed
    min_skill_overlap=0.2,     # 20% minimum skill overlap
    consider_related_skills=True
)

filter_engine = FilterEngine(config, skills_db)
filtered_careers = filter_engine.filter_careers(user_profile, all_careers)
```

### 3. Scoring System

Weighted scoring based on multiple factors:

```python
from recommendation_engine.scoring import ScoringEngine
from recommendation_engine.config import ScoringWeights, ScoringConfig

weights = ScoringWeights(
    skill_match=0.4,           # 40% weight on skill matching
    interest_match=0.25,       # 25% weight on interest alignment
    salary_compatibility=0.2,  # 20% weight on salary compatibility
    experience_match=0.15      # 15% weight on experience matching
)

scoring_engine = ScoringEngine(ScoringConfig(), weights)
scores = scoring_engine.score_multiple_careers(user_profile, careers)
```

### 4. Categorization System

Organizes recommendations into three zones:

- **Safe Zone**: High-confidence matches with existing skills (score ≥ 0.7)
- **Stretch Zone**: Good matches requiring some development (score ≥ 0.5)
- **Adventure Zone**: Exploratory matches requiring significant upskilling (score ≥ 0.3)

```python
from recommendation_engine.categorization import CategorizationEngine
from recommendation_engine.config import CategorizationThresholds

thresholds = CategorizationThresholds(
    safe_zone_min=0.7,
    stretch_zone_min=0.5,
    adventure_zone_min=0.3
)

categorization_engine = CategorizationEngine(thresholds)
recommendations = categorization_engine.categorize_recommendations(
    user_profile, careers, scores
)
```

## Configuration

The engine is highly configurable through the `RecommendationConfig` class:

```python
from recommendation_engine.config import RecommendationConfig, ScoringWeights

# Custom configuration
config = RecommendationConfig(
    scoring_weights=ScoringWeights(
        skill_match=0.5,        # Emphasize skills more
        interest_match=0.3,
        salary_compatibility=0.1,
        experience_match=0.1
    ),
    max_recommendations=15,
    min_recommendations=3
)

engine = RecommendationEngine(config=config, skills_db=skills)
```

## Advanced Usage

### Getting Recommendations by Category

```python
# Get recommendations organized by category
categorized_recs = engine.get_recommendations_by_category(
    user_profile=user_profile,
    available_careers=careers,
    limit_per_category=5
)

print("Safe Zone:", len(categorized_recs["safe_zone"]))
print("Stretch Zone:", len(categorized_recs["stretch_zone"]))
print("Adventure Zone:", len(categorized_recs["adventure_zone"]))
```

### Explaining Individual Recommendations

```python
# Get detailed explanation for a specific career
explanation = engine.explain_recommendation(user_profile, career)

print(f"Career: {explanation['career_title']}")
print(f"Score: {explanation['total_score']:.2f}")
print(f"Category: {explanation['category']}")
print(f"Confidence: {explanation['confidence']:.2f}")
print("Reasons:")
for reason in explanation['reasons']:
    print(f"  - {reason}")
```

### Getting Statistics

```python
# Get comprehensive statistics about the recommendation process
stats = engine.get_recommendation_statistics(user_profile, careers)

print("Filtering Stats:", stats['filtering_stats'])
print("Category Distribution:", stats['category_distribution'])
print("Score Statistics:", stats['score_statistics'])
```

## Customization

### Custom Scoring Weights

```python
# Emphasize different factors based on user type
junior_weights = ScoringWeights(
    skill_match=0.3,
    interest_match=0.4,      # Higher weight on interests for juniors
    salary_compatibility=0.1,
    experience_match=0.2
)

senior_weights = ScoringWeights(
    skill_match=0.5,         # Higher weight on skills for seniors
    interest_match=0.2,
    salary_compatibility=0.2,
    experience_match=0.1
)
```

### Custom Thresholds

```python
# More conservative thresholds
conservative_thresholds = CategorizationThresholds(
    safe_zone_min=0.8,       # Higher bar for safe zone
    stretch_zone_min=0.6,
    adventure_zone_min=0.4
)

# More aggressive thresholds
aggressive_thresholds = CategorizationThresholds(
    safe_zone_min=0.6,       # Lower bar for safe zone
    stretch_zone_min=0.4,
    adventure_zone_min=0.2
)
```

## Testing with Mock Data

The engine includes comprehensive mock data for testing:

```python
from recommendation_engine.mock_data import (
    MOCK_SKILLS, MOCK_CAREERS, MOCK_USER_PROFILE, ALTERNATIVE_USER_PROFILE
)

# Test with different user profiles
recommendations_1 = engine.get_recommendations(MOCK_USER_PROFILE, MOCK_CAREERS)
recommendations_2 = engine.get_recommendations(ALTERNATIVE_USER_PROFILE, MOCK_CAREERS)

# Compare results
print(f"User 1 got {len(recommendations_1)} recommendations")
print(f"User 2 got {len(recommendations_2)} recommendations")
```

## Integration Guidelines

### For Microservices Architecture

```python
# Service initialization
class RecommendationService:
    def __init__(self):
        self.engine = RecommendationEngine(
            config=load_config_from_db(),
            skills_db=load_skills_from_db()
        )
    
    def get_user_recommendations(self, user_id: str, limit: int = 10):
        user_profile = load_user_profile(user_id)
        careers = load_available_careers()
        
        return self.engine.get_recommendations(
            user_profile=user_profile,
            available_careers=careers,
            limit=limit
        )
```

### For API Endpoints

```python
from fastapi import FastAPI
from recommendation_engine import RecommendationEngine

app = FastAPI()
engine = RecommendationEngine()

@app.post("/recommendations")
async def get_recommendations(user_profile: UserProfile, limit: int = 10):
    careers = await load_careers_from_db()
    recommendations = engine.get_recommendations(user_profile, careers, limit)
    
    return {
        "recommendations": [
            {
                "career": rec.career.dict(),
                "score": rec.score.total_score,
                "category": rec.category.value,
                "reasons": rec.reasons
            }
            for rec in recommendations
        ]
    }
```

## Performance Considerations

- **Caching**: Cache skill databases and career data
- **Batch Processing**: Process multiple users in batches
- **Async Operations**: Use async/await for database operations
- **Configuration Updates**: Hot-reload configuration without restart

## Future Enhancements

1. **Machine Learning Integration**: Replace rule-based scoring with ML models
2. **Real-time Learning**: Update recommendations based on user feedback
3. **A/B Testing**: Built-in support for testing different configurations
4. **Advanced NLP**: Better interest and skill matching using NLP
5. **Market Data Integration**: Real-time job market data integration

## Dependencies

- `pydantic`: Data validation and settings management
- `typing`: Type hints support
- `datetime`: Date and time handling
- `enum`: Enumeration support

## License

This recommendation engine is designed for integration into larger career guidance systems and can be adapted for various use cases.