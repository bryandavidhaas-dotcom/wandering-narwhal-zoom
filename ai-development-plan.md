# Development Plan: Purely AI-Driven Recommendation Engine

This document outlines the development plan for creating a new, purely AI-driven recommendation engine, as specified in the `refined-prd.md`. This plan explicitly excludes the use of the previous rules-based recommendation engine.

## Guiding Principle

The new engine will be built from the ground up to be powered by an external AI model. All recommendation and tuning logic will be handled by this model. The existing `RecommendationEngine` and `EnhancedRecommendationEngine` are considered legacy and will not be used.

## Epics & User Stories

### Epic 1: AI Model Integration & API Wrapper

**Description:** Develop the backend service that acts as a wrapper for the external AI model, handling all communication and data transformation.

**User Stories:**

*   **Story 1.1:** As a developer, I need to build an API endpoint that accepts a `User Assessment` and sends it to the AI model to generate initial recommendations.
*   **Story 1.2:** As a developer, I need to ensure the AI model's JSON response is parsed and returned in a consistent format (`Recommendation Set`).
*   **Story 1.3:** As a developer, I need to create a new API endpoint for interactive tuning that sends the current recommendations and a user's chat prompt to the AI model.

### Epic 2: Frontend Integration for AI-Powered Recommendations

**Description:** Connect the existing frontend to the new AI-driven backend API and build the required user interface components.

**User Stories:**

*   **Story 2.1:** As a developer, I need to update the frontend to send the `User Assessment` to the new AI API endpoint.
*   **Story 2.2:** As a user, I want to see the AI-generated `Recommendation Set` on the results page.
*   **Story 2.3:** As a user, I want a chat interface on the results page where I can type prompts to refine my recommendations.
*   **Story 2.4:** As a user, I want the recommendations to update in real-time based on my chat prompts, with the updates coming directly from the AI model.
*   **Story 2.5:** As a developer, I need to implement the new color scheme across the frontend to align with the updated design.

### Epic 3: Data Models & Authentication

**Description:** Define the necessary data structures for the new AI-driven workflow and ensure all endpoints are secure.

**User Stories:**

*   **Story 3.1:** As a developer, I need to define and implement the data models for `User`, `User Assessment`, `Recommendation Set`, and `Tuning Interaction` as described in the PRD.
*   **Story 3.2:** As a developer, I need to ensure all new AI-related API endpoints are protected by the existing user authentication system.

## MVP Milestones

1.  **Milestone 1: Build the AI API Wrapper**
    *   Set up a new FastAPI router or module for the AI engine.
    *   Implement the endpoint to handle the initial `User Assessment` and communicate with the external AI model.
    *   Implement the endpoint for interactive tuning via chat prompts.

2.  **Milestone 2: Connect Frontend to the New AI Backend**
    *   Integrate the existing user assessment UI to send data to the new AI API.
    *   Display the initial, AI-generated `Recommendation Set` on the results page.

3.  **Milestone 3: Implement the Interactive Chat UI**
    *   Develop the chat interface on the results page.
    *   Connect the chat UI to the new AI tuning endpoint.
    *   Ensure the results page updates dynamically with the new recommendations from the AI model.

4.  **Milestone 4: Finalize and Secure**
    *   Implement and display the conversation history.
    *   Secure all new endpoints.
    *   Conduct end-to-end testing of the purely AI-driven workflow.

## Technology Stack

*   **Frontend:** Existing React/Vite frontend
*   **Backend:** Existing Python/FastAPI backend (with a new, separate module for the AI engine)
*   **Database:** Existing MongoDB
*   **AI Model:** External, API-based AI model (e.g., OpenAI GPT, Google Gemini, or similar).