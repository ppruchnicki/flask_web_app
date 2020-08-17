## Flask App
Simple demo app with basic CRUD functionality to handle notes/posts or todos logic.

## What's included?
* Blueprints
* Flask-Admin micro-framework for user and permissions management and CRUD functionality 
* Flask-Login for user authorization
* Flask-SQLAlchemy for databases
* Flask-Migrate for managing changes of database structure
* Flask-WTF for forms
* Flask-Mail for sending confirmation emails, reseting password
* Basic CRUD functionality for notes and todos
* Profile managment changing email and password using mail authorization with tokens

## Quick start
1. Install all dependencies in virtual environment `pipenv install`
2. Setup environment variables: `SECRET_KEY, MAIL_USER, MAIL_PASSWORD, SECURITY_PASSWORD_SALT'` (default email provider - gmail)
3. Run virtual environment `pipenv shell`
4. First create db  `python3 app.py db init`
5. Create migrations `python3 app.py db migrate`
6. Upgrade db `python3 app.py db upgrade`
7. `flask run`

## Upgrade db model
If you want to upgrade previosly created and used db ( after changes to the structure).
1. Close the app
2. `python3 app.py db migrate`
3. `python3 app.py db upgrade`
4. `flask run`
