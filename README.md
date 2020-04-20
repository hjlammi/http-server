# HTTP server

### Prerequisites
- Python 3.8
- pipenv
- entr

### Running the server in the local environment
- Activate virtualenv in the root folder and install dependencies:
```shell
pipenv shell

pipenv install
```
- Start the server with the command:
```shell
find server -name '*.py' | entr -c -r -s 'python -m server.core tests/webroot'
```
The server will serve the folder that is given to it as a command line argument. On the above line the server will serve 'tests/webroot' folder.

### Running the tests
- Run unit tests from the application root folder with the command:
```shell
find server/ tests/ -name "*.py" -not -path "*/node_modules/*" | entr -c -s 'python -m pytest -s -vv'
```
- Start Cypress from the tests/acceptance folder with the command:
```shell
npx cypress open
```
The above command will open a Cypress window with integration tests folder in it. From the folder click server_spec.js file and the Cypress test will open and run in a browser.
