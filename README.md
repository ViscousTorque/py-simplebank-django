# py-simplebank-backend

# TODOs
* Tests!! so far testing with vs code postman plugin
  * unit tests - now wired up to run the first
    * fix UpdateUser
    * add more :-)
  * API tests
* some APIs:
  * complete create transfer
    * update the balance, create enrties
  * renew_access_token
* add frontend - will use Vue.js
  * keep separate from DRF for future scalability
    * views
      * create_user / create_account
      * view balance
      * transfer balance
    * put into a subtree and separate repo
* Refactoring
  * use Django jwt instead of custom - extend obj with a couple of fields
  * general and app urls.py
* sort terraform for deployment
* add github workflow
  * deploy
* test deployment in AWS
* Read up a little on Django documentation:
  * https://drf-spectacular.readthedocs.io/en/latest/readme.html
* Read more on Django rest framework:
  * https://www.django-rest-framework.org/

# Setup

* Ubuntu 24.04
* vs code
* Python
    * python3 -m venv venv
    * source venv/bin/activate
    * pip install --upgrade pip
    * pip install -r requirements.txt
* create .env file and add DJANGO_SECRET_KEY
* make startLocalEnv
* Login in to pgadmin4 (http://localhost:8000) Django doesnt add the user!
    * Add new user: CREATE USER simplebank WITH PASSWORD 'simplebankSecret';
* make create-db
* make migrations
```
make migrations
python manage.py makemigrations
Migrations for 'accounts':
  apps/accounts/migrations/0001_initial.py
    + Create model Account
  apps/accounts/migrations/0002_initial.py
    + Add field owner to account
    ~ Alter unique_together for account (1 constraint(s))
Migrations for 'transactions':
  apps/transactions/migrations/0001_initial.py
    + Create model Entry
    + Create model Transfer
Migrations for 'authentication':
  apps/authentication/migrations/0001_initial.py
    + Create model Session
  apps/authentication/migrations/0002_initial.py
    + Add field username to session
Migrations for 'users':
  apps/users/migrations/0001_initial.py
    + Create model User
    + Create model VerifyEmail
```
* make migrate
```
python manage.py migrate
Operations to perform:
  Apply all migrations: accounts, auth, authentication, contenttypes, transactions, users
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying contenttypes.0002_remove_content_type_name... OK
  Applying auth.0001_initial... OK
  Applying auth.0002_alter_permission_name_max_length... OK
  Applying auth.0003_alter_user_email_max_length... OK
  Applying auth.0004_alter_user_username_opts... OK
  Applying auth.0005_alter_user_last_login_null... OK
  Applying auth.0006_require_contenttypes_0002... OK
  Applying auth.0007_alter_validators_add_error_messages... OK
  Applying auth.0008_alter_user_username_max_length... OK
  Applying auth.0009_alter_user_last_name_max_length... OK
  Applying auth.0010_alter_group_name_max_length... OK
  Applying auth.0011_update_proxy_permissions... OK
  Applying auth.0012_alter_user_first_name_max_length... OK
  Applying users.0001_initial... OK
  Applying accounts.0001_initial... OK
  Applying accounts.0002_initial... OK
  Applying authentication.0001_initial... OK
  Applying authentication.0002_initial... OK
  Applying transactions.0001_initial... OK
  ```
  * make create-superuser
```
Username: viscoustorque
Email: viscoustorque@example.com
Password: 
Password (again): 
Superuser created successfully.
```
* make server

## Documentation
Use:
```
make documentation
```
To inspect on local machine:
```
cd doc
python -m http.server 7000
'''
Browser, open : http://localhost:7000/openapi.html

## Running Tests

### In docker compose
* docker compose up --build
* docker compose down

### In vs code or using the browser
You need 2 terminals
* make startLocalEnv
* make server
* make frontend 

* Use browser and http://localhost:3000
* Configure tests in vs code panel to pytest and select component tests, use test explorer to run the tests

## Notes:

* https://docs.djangoproject.com/en/5.1/
* python manage.py shell
```Python 3.12.3 (main, Feb  4 2025, 14:48:35) [GCC 13.3.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
(InteractiveConsole)
>>> from django.apps import apps
>>> apps.get_app_config('users').models
{'user_groups': <class 'apps.users.models.User_groups'>, 'user_user_permissions': <class 'apps.users.models.User_user_permissions'>, 'user': <class 'apps.users.models.User'>, 'verifyemail': <class 'apps.users.models.VerifyEmail'>}
>>> 
```

### Setting up Django unit tests
Starting with some unit tests ... Django needs to create its db!
Provide the user with correct permissions to create db
```
docker run -it --rm --network bank-network postgres   psql -h postgres -U admin -d postgres   -c "ALTER USER
 simplebank CREATEDB;"
Password for user admin: 
ALTER ROLE
```
