import re
import pytest
from playwright.sync_api import Page, expect

def test_career_journey_e2e(page: Page):
    """
    End-to-end test for the 'Explore this Career' feature.
    """
    # Step 1: Navigate to the application's login page
    page.goto("http://localhost:5173/auth")

    # Step 2: Log in with a sample user
    page.fill('input[name="email"]', "testuser@example.com")
    page.fill('input[name="password"]', "password123")
    page.click('button[type="submit"]')

    # Step 3: Wait for the dashboard to load and find the "Explore this Career" button
    page.wait_for_url("http://localhost:5173/dashboard", timeout=60000)
    
    # Get the first career recommendation
    first_career_card = page.locator(".career-card").first
    career_title_element = first_career_card.locator("h3")
    
    # Extract the career title text
    career_title = career_title_element.inner_text()
    
    # Find and click the "Explore this Career" button within the first career card
    explore_button = first_career_card.locator('button:has-text("Explore this Career")')
    expect(explore_button).to_be_visible()
    explore_button.click()

    # Step 4: Wait for the career detail page to load
    # The URL should match the kebab-case version of the career title
    expected_career_slug = career_title.lower().replace(" ", "-")
    page.wait_for_url(f"http://localhost:5173/career/{expected_career_slug}")

    # Step 5: Assert that the page's title or a key heading contains the correct career name
    heading_element = page.locator(f"h1:has-text('{career_title}')")
    expect(heading_element).to_be_visible()

    print(f"Successfully navigated to the career detail page for: {career_title}")
    print("End-to-end test for 'Explore this Career' feature completed successfully.")
