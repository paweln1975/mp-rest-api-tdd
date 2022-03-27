# mp-rest-api-tdd
Mastering Python - with REST API and TDD approach

In order to run the project:
1. install docker
2. install docker-compose
3. start all tests by running a command:
   ```
   docker-compose run --rm app sh -c "python manage.py test && flake8"
   ```
4. start the application by running a command:
   ```
    docker-compose up
   ```
5. go to URLs:
  - [Admin panel](http://127.0.0.1:8000/admin)
  - [User app](http://127.0.0.1:8000/api/user)
  - [Recipe app](http://127.0.0.1:8000/api/recipe)

