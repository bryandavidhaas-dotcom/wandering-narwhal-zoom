describe('CareerDetail Component', () => {
  beforeEach(() => {
    // Mock the API response for a specific career
    cy.intercept('GET', '/api/career/senior-product-manager', {
      fixture: 'career_detail.json'
    }).as('getCareerDetail');

    // Mock user authentication
    cy.login(); // Assuming a custom command for login

    // Visit the career detail page
    cy.visit('/career/senior-product-manager');
  });

  it('should display the career title and description', () => {
    cy.contains('h1', 'Senior Product Manager').should('be.visible');
    cy.contains('p', 'Lead complex product initiatives, mentor junior PMs, drive product strategy for major features').should('be.visible');
  });

  it('should display the key information section', () => {
    cy.contains('div', 'Salary Range').should('contain', '$120,000 - $160,000');
    cy.contains('div', 'Experience Level').should('contain', 'mid');
    cy.contains('div', 'Learning Path').should('contain', 'Advanced Product Management (3-4 months)');
  });

  it('should display the required skills', () => {
    cy.contains('h4', 'Technical Skills').should('be.visible');
    cy.contains('span', 'Product Management').should('be.visible');
    cy.contains('span', 'Data Analysis').should('be.visible');

    cy.contains('h4', 'Soft Skills').should('be.visible');
    cy.contains('span', 'Leadership').should('be.visible');
    cy.contains('span', 'Communication').should('be.visible');
  });

  it('should display the "Day in Life" tab content', () => {
    cy.contains('button', 'Day in Life').click();
    cy.contains('h3', 'A Typical Day as a Senior Product Manager').should('be.visible');
    cy.contains('p', 'Product strategy, stakeholder management, data analysis, team collaboration').should('be.visible');
  });

  it('should display the career progression path', () => {
    cy.contains('button', 'Career Path').click();
    cy.contains('h4', 'Product Manager').should('be.visible');
    cy.contains('h4', 'Principal Product Manager').should('be.visible');
  });

  it('should handle API errors gracefully', () => {
    // Mock a failed API response
    cy.intercept('GET', '/api/career/non-existent-career', {
      statusCode: 404,
      body: { detail: 'Career not found' }
    }).as('getNonExistentCareer');

    cy.visit('/career/non-existent-career');

    cy.contains('h2', 'Career Not Found').should('be.visible');
    cy.contains('p', 'The career you\'re looking for doesn\'t exist or you don\'t have access.').should('be.visible');
  });
});