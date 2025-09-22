# Recommendation Engine Architecture Analysis

## 1. Overview

The current recommendation engine is a hybrid system with logic distributed between a Python-based backend and a TypeScript-based frontend. This distribution of responsibilities is a primary contributor to the existing scalability and accuracy issues.

## 2. Backend Architecture (`recommendation-engine`)

The backend is a modular system responsible for the core recommendation logic. It is composed of several key components:

- **`engine.py`**: Orchestrates the recommendation process by coordinating the filtering, scoring, and categorization components.
- **`filters.py`**: Implements multi-stage filtering based on user preferences, skills, and interests.
- **`scoring.py`**: Ranks careers using a weighted scoring algorithm that considers skill match, interest alignment, salary, and experience.
- **`categorization.py`**: Categorizes recommendations into "Safe," "Stretch," and "Adventure" zones. This component also contains a hardcoded, keyword-based system for determining career fields, which is a significant source of inaccuracy.

## 3. Frontend Architecture (`frontend/src/utils/careerMatching.ts`)

The frontend contains a surprising amount of business logic, effectively creating a parallel recommendation engine. Key issues include:

- **Hardcoded Career Templates**: The `careerMatching.ts` file contains an extensive, hardcoded list of `COMPREHENSIVE_CAREER_TEMPLATES`. This approach is not scalable and makes it difficult to update or expand the career database.
- **Duplicated Logic**: The frontend duplicates the filtering, scoring, and categorization logic found in the backend. This redundancy leads to inconsistencies and increases the maintenance overhead.
- **Safety Guardrails**: While well-intentioned, the safety guardrails implemented in the frontend are complex and tightly coupled with the hardcoded templates. This makes them difficult to manage and verify.

## 4. Key Issues

### 4.1. Architectural Uncertainty and Scalability

The lack of a clear boundary between frontend and backend responsibilities is the most significant architectural flaw. The duplicated logic and hardcoded data in the frontend create a system that is difficult to scale and maintain. Any change to the recommendation logic must be implemented in both places, increasing the risk of inconsistencies.

### 4.2. Inappropriate Recommendations and Accuracy

The keyword-based career categorization in `categorization.py` is too rigid and likely the primary cause of inaccurate recommendations. For example, a senior-level "SVP of Product" might be miscategorized due to keyword matches with unrelated fields, leading to suggestions like "Police Chief." The frontend's separate logic further complicates debugging and resolving these issues.

## 5. Conclusion

The current architecture is not sustainable. To address the scalability and accuracy issues, the system must be refactored to establish a clear separation of concerns. The backend should be the single source of truth for all recommendation logic, while the frontend should focus on presentation and user interaction.