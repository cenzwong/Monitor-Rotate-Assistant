# export FLASK_APP=app.py
# export FLASK_ENV=development # will reload itself on code changes
# export FLASK_APP=./app.py; export FLASK_ENV=development
# flask run
# flask run --host=0.0.0.0
# file name should be app.py or wsgi.py
# https://flask.palletsprojects.com/en/1.1.x/patterns/lazyloading/#converting-to-centralized-url-map


from flask import Flask
from flask import request
# from markupsafe import escape
import tempdb

app = Flask(__name__)
if __name__ == "__main__":
   app.run(host='0.0.0.0')

@app.route('/')
@app.route('/help')
def index():
    return "render_template(rootdoc)"

# tempdb
str_tempdb = "/tempdb"
app.add_url_rule(str_tempdb + "/set/<key>", view_func=tempdb.tempdb_set)
app.add_url_rule(str_tempdb + "/get/<key>", view_func=tempdb.tempdb_get)
app.add_url_rule(str_tempdb + "/clear/<key>", view_func=tempdb.tempdb_clear)
app.add_url_rule(str_tempdb + "/getAll", view_func=tempdb.tempdb_getAll)
app.add_url_rule(str_tempdb + "/clearAll", view_func=tempdb.tempdb_clearAll)
