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
        cy.request('/notfound').as('response');
        cy.get('@response').should((response) => {
            expect(response.statusText).to.equal('Not Found');
            expect(response.status).to.equal(404);
        });
        cy.contains('Page not found');
    });
});
