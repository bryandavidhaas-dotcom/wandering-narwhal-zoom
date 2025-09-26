describe('End-to-End Navigation', () => {
  beforeEach(() => {
    // Mock the API response for recommendations
    cy.intercept('POST', '/api/recommendations', {
      fixture: 'recommendations.json'
    }).as('getRecommendations');

    // Mock the API response for a specific career
    cy.intercept('GET', '/api/career/senior-product-manager', {
      fixture: 'career_detail.json'
    }).as('getCareerDetail');

    // Mock user authentication
    cy.login(); // Assuming a custom command for login

    // Visit the dashboard
    cy.visit('/dashboard');
  });

  it('should allow a user to navigate from the dashboard to a career detail page', () => {
    // Wait for recommendations to load
    cy.wait('@getRecommendations');

    // Click on the "Explore This Career" button for the first recommendation
    cy.contains('h3', 'Senior Product Manager').parents('.card').find('button').contains('Explore This Career').click();

    // Verify that the URL has changed to the career detail page
    cy.url().should('include', '/career/senior-product-manager');

    // Wait for the career detail page to load
    cy.wait('@getCareerDetail');

    // Verify that the career title is displayed on the career detail page
    cy.contains('h1', 'Senior Product Manager').should('be.visible');
  });

  it('should display the "Day in the Life" tab content after navigating', () => {
    // Navigate to the career detail page
    cy.contains('h3', 'Senior Product Manager').parents('.card').find('button').contains('Explore This Career').click();
    cy.url().should('include', '/career/senior-product-manager');
    cy.wait('@getCareerDetail');

    // Click on the "Day in Life" tab
    cy.contains('button', 'Day in Life').click();

    // Verify that the "Day in the Life" content is visible
    cy.contains('h3', 'A Typical Day as a Senior Product Manager').should('be.visible');
    cy.contains('p', 'Product strategy, stakeholder management, data analysis, team collaboration').should('be.visible');
  });

  it('should maintain data consistency between the dashboard and career detail page', () => {
    // Get the career title from the dashboard
    cy.contains('h3', 'Senior Product Manager').invoke('text').as('careerTitle');

    // Navigate to the career detail page
    cy.contains('h3', 'Senior Product Manager').parents('.card').find('button').contains('Explore This Career').click();
    cy.url().should('include', '/career/senior-product-manager');
    cy.wait('@getCareerDetail');

    // Compare the career title on the career detail page with the title from the dashboard
    cy.get('@careerTitle').then((careerTitle) => {
      cy.contains('h1', careerTitle).should('be.visible');
    });
  });
});