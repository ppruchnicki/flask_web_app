## Quick start
1. First create db  `python3 app.py db init`
2. Create migrations `python3 app.py db migrate`
3. Upgrade db `python3 app.py db upgrade`
4. `flask run`

## Upgrade db model
If you want to upgrade previosly created and used db ( after changes to the structure).
1. Close the app
2. `python3 app.py db migrate`
3. `python3 app.py db upgrade`
4. `flask run`