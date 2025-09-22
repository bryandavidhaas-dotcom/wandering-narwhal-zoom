# End-to-End Test Plan: "Explore this Career" Feature

## 1. Objective

This document outlines the end-to-end (E2E) test plan for the "Explore this Career" feature. The primary goal is to ensure the entire user workflow is functioning correctly, from fetching career recommendations to viewing a specific career's detail page. This test is critical to prevent regressions, especially after the backend change to normalize job titles to kebab-case.

## 2. Test Case: Successful Navigation to Career Detail Page

This test case validates the complete workflow for a user exploring a recommended career.

### 2.1. Test Steps

1.  **Setup: Mock User Profile**
    *   The test runner should have a predefined user profile (e.g., a JSON fixture). This profile will be used to mock the user's session and provide consistent data for the API request.
    *   The profile should be comprehensive enough to generate a predictable set of career recommendations.

2.  **Step 1: Fetch Career Recommendations**
    *   The test should simulate a logged-in user landing on the dashboard or recommendations page.
    *   It will intercept the API call to the recommendations endpoint (e.g., `/api/recommendations`).
    *   The test will provide the mock user profile as the payload for this request.

3.  **Step 2: Verify API Response**
    *   Upon receiving the response from the recommendations API, the test must perform the following assertions:
        *   The HTTP status code is 200 (OK).
        *   The response body is a JSON array of career recommendations.
        *   Each object in the array contains a `careerType` property.
        *   **Crucially, the value of `careerType` for every recommendation must be in kebab-case** (e.g., "data-analyst", "software-engineer"). A regular expression can be used for this validation: `^[a-z]+(-[a-z]+)*$`.

4.  **Step 3: Simulate User Interaction**
    *   The test should select one of the career recommendations displayed on the page. For consistency, it's best to target a specific recommendation, for example, the first one in the list.
    *   It will then simulate a user click on the "Explore this Career" button associated with that recommendation.

5.  **Step 4: Validate Navigation and Page Content**
    *   After the button click, the test must verify that the application navigates to the correct career detail page.
    *   The URL should correspond to the `careerType` of the selected recommendation (e.g., `/career/data-analyst`).
    *   Once on the career detail page, the test should assert that the page has loaded successfully. This can be done by checking for the presence of a key element on the page, such as:
        *   The career title (e.g., an `<h1>` tag containing "Data Analyst").
        *   A container for the career description.
        *   Any other element that is expected to be present on a fully loaded career detail page.

### 2.2. Success Criteria

*   All steps are executed without errors.
*   The `careerType` in the API response is validated to be in kebab-case.
*   The application correctly navigates to the expected URL.
*   The career detail page loads its content successfully.

## 3. Tooling and Framework

This test plan is designed to be implemented using a modern E2E testing framework such as **Cypress** or **Playwright**. These frameworks provide the necessary tools for:

*   Mocking API requests and responses.
*   Simulating user interactions (clicks, navigation).
*   Asserting on DOM elements and network requests.

## 4. Implementation Notes

*   **Fixtures:** Use fixture files to store the mock user profile and, if necessary, a mock API response. This will make the test more maintainable and independent of the live backend.
*   **Selectors:** Use stable and unique selectors for targeting elements (e.g., `data-testid` attributes) to avoid test fragility due to UI changes.
*   **Environment:** The test should be run in a controlled environment, preferably against a local or staging build of the application.