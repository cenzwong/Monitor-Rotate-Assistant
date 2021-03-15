# export FLASK_APP=app.py
# export FLASK_ENV=development # will reload itself on code changes
# flask run
# flask run --host=0.0.0.0
# file name should be app.py or wsgi.py
# https://flask.palletsprojects.com/en/1.1.x/patterns/lazyloading/#converting-to-centralized-url-map

from flask import request


temp_db = {}

def tempdb_set(key):
    # show the user profile for that user
    temp_db[key] = request.args.get('data')
    return temp_db[key]

def tempdb_get(key):
    # show the user profile for that user
    if key in temp_db:
        return temp_db[key]
    else:
        return ""

def tempdb_clear(key):
    # show the user profile for that user
    return temp_db.pop(key, "")

def tempdb_getAll():
    print(str(temp_db))
    return str(temp_db)

def tempdb_clearAll():
    if request.args.get("yes") == "":
        temp_db.clear()
        return str(temp_db)
    
    return "Please confirm with ?yes"
