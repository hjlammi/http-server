describe('server', function() {
    beforeEach(function() {
        cy.visit('http://127.0.0.1:8000');
    });

    it('receives 200 OK response from the server', function() {
        cy.request('/').as('response');
        cy.get('@response').should((response) => {
            expect(response.statusText).to.equal('OK');
            expect(response.status).to.equal(200);
        });
    });

    it('receives 404 Not Found response from the server', function() {
        cy.request({
            url:'/notfound',
            failOnStatusCode: false
        }).as('response');
        cy.get('@response').should((response) => {
            expect(response.statusText).to.equal('Not Found');
            expect(response.status).to.equal(404);
        });
        cy.visit({
            url: 'http://127.0.0.1:8000/notfound',
            failOnStatusCode: false
        });
        cy.contains('Page not found');
    });

    it('lists the contents of the server on the root URI', function() {
        cy.get('h1').should('have.text', '/');
        cy.get('a').should(($a) => {
            expect($a).to.have.length(3);
            expect($a.first()).to.contain('cat_pics/');
            expect($a[1]).to.contain('random/');
            expect($a.last()).to.contain('lorem_ipsum.txt');
        });
    });

    it('shows lorem_ipsum.txt file\'s content', function() {
        cy.get('a').contains('lorem_ipsum.txt').click();
        cy.url().should('include', '/lorem_ipsum.txt');
        cy.get('h1').should('not.contain', 'Page not found');
        cy.get('body').contains('Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, pretium quis, sem. Nulla consequat massa quis enim. Donec pede justo, fringilla vel, aliquet nec, vulputate eget, arcu.\n');
    });

    it('list cat_pics dir\'s contents on the page', function() {
        cy.get('a').contains('cat_pics').click();
        cy.url().should('include', '/cat_pics');
        cy.get('h1').should('have.text', '/cat_pics');
        cy.get('a').should(($a) => {
            expect($a).to.have.length(3);
            expect($a.first()).to.contain('2janu.jpg');
            expect($a[1]).to.contain('ella.jpg');
            expect($a.last()).to.contain('janu.jpg');
        });
    });
});
