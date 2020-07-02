## Quick start
1. Install all dependencies in virtual environment `pipenv install --dev`
2. Run virtual environment `pipenv shell`
3. First create db  `python3 app.py db init`
4. Create migrations `python3 app.py db migrate`
5. Upgrade db `python3 app.py db upgrade`
6. `flask run`

## Upgrade db model
If you want to upgrade previosly created and used db ( after changes to the structure).
1. Close the app
2. `python3 app.py db migrate`
3. `python3 app.py db upgrade`
4. `flask run`
