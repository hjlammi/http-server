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
        cy.get('h1').should('contain', '/');
        cy.get('a').should(($a) => {
            expect($a).to.have.length(3);
            expect($a.first()).to.contain('cat_pics/');
            expect($a[1]).to.contain('random/');
            expect($a.last()).to.contain('lorem_ipsum.txt');
        });
    });

    it('it shows lorem_ipsum.txt file\'s content', function() {
        cy.get('a').contains('lorem_ipsum.txt').click();
        cy.url().should('include', '/lorem_ipsum.txt');
        cy.get('h1').should('not.contain', 'Page not found');
        cy.get('body').contains('Lorem ipsum dolor sit amet');
    });
});
