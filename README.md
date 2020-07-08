## Quick start
1. Install all dependencies in virtual environment `pipenv install --dev`
2. Setup environment variables: `SECRET_KEY, MAIL_USER, MAIL_PASSWORD` (default email provider - gmail)
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
