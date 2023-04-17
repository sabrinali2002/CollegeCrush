import json
import os
from flask import Flask, render_template, request
from flask_cors import CORS
from helpers.MySQLDatabaseHandler import MySQLDatabaseHandler

# ROOT_PATH for linking with all your files. 
# Feel free to use a config.py or settings.py with a global export variable
os.environ['ROOT_PATH'] = os.path.abspath(os.path.join("..",os.curdir))

# These are the DB credentials for your OWN MySQL
# Don't worry about the deployment credentials, those are fixed
# You can use a different DB name if you want to
MYSQL_USER = "root"
<<<<<<< Updated upstream
MYSQL_USER_PASSWORD = "MayankRao16Cornell.edu"
=======
MYSQL_USER_PASSWORD = "Youyou0305!"
>>>>>>> Stashed changes
MYSQL_PORT = 3306
MYSQL_DATABASE = "kardashiandb"

mysql_engine = MySQLDatabaseHandler(MYSQL_USER,MYSQL_USER_PASSWORD,MYSQL_PORT,MYSQL_DATABASE)

# Path to init.sql file. This file can be replaced with your own file for testing on localhost, but do NOT move the init.sql file
mysql_engine.load_file_into_db()

app = Flask(__name__)
CORS(app)

# Sample search, the LIKE operator in this case is hard-coded, 
# but if you decide to use SQLAlchemy ORM framework, 
# there's a much better and cleaner way to do this
<<<<<<< Updated upstream
def sql_search(episode):
    query_sql = f"""SELECT * FROM episodes WHERE LOWER( title ) LIKE '%%{episode.lower()}%%' limit 10"""
    keys = ["id","title","descr"]
=======


def sql_search(state):
    query_sql = f"""SELECT * FROM colleges WHERE LOWER (state) LIKE '%%{state}%%'"""
    keys = ["name", "city", "state"]
>>>>>>> Stashed changes
    data = mysql_engine.query_selector(query_sql)
    return json.dumps([dict(zip(keys,i)) for i in data])

@app.route("/")
def home():
    return render_template('base.html',title="sample html")

<<<<<<< Updated upstream
@app.route("/episodes")
def episodes_search():
    text = request.args.get("title")
    return sql_search(text)
=======

# @app.route("/colleges")
# def college_search():
#     text = request.args.get("title")
#     with open("colleges.json", "r") as f:
#         data = json.load(f)
#     data2 = {}
#     result = search_similarity(
#         data,
#         text,
#         request.args.get("size"),
#         request.args.get("region"),
#         request.args.get("sort"),
#     )
#     return result


@app.route("/colleges")
def college_search():
    text = request.args.get("location")
    result = sql_search(text)
    return result
>>>>>>> Stashed changes

# app.run(debug=True)