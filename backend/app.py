import json
import os
import csv
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
MYSQL_USER_PASSWORD = "MayankRao16Cornell.edu"
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
def sql_search(episode):
    query_sql = f"""SELECT * FROM episodes WHERE LOWER( title ) LIKE '%%{episode.lower()}%%' limit 10"""
    keys = ["id","title","descr"]
    data = mysql_engine.query_selector(query_sql)
    return json.dumps([dict(zip(keys,i)) for i in data])

def search_similarity(data, queries):
    arr = []
    inputs = queries.split(',')
    dic = {}
    region_dic = {}
    region_dic['WEST'] = set(['WA','OR','ID','MT','WY','CA','NV','UT','AZ','NM','CO'])
    region_dic['MIDWEST'] = set(['ND','SD','NE','KS','MN','IA','MO','WI','IL','IN','MI','IN','OH'])
    region_dic['NORTHEAST'] = set(['PA','NY','NJ','VT','NH','ME','MA','CT','RI'])
    region_dic['SOUTH'] = set(['TX','OK','AR','LA','MS','TN','KY','AL','GA', 'FL','WV',
                               'NC','VA','MD','DE','NC','SC'])
    for i in inputs:
        if len(i) == 2:
            dic['state'] = i
        else:
            dic['city'] = i
    s = set()
    for colleges in data:
        if 'city' in colleges and'city' in dic and colleges['city'].lower() == queries.lower() and int(colleges['tot_enroll'])>1000:
            if colleges['name'] not in s:
                arr.append(({'title': colleges['name'], 'website': colleges['website'],'enrolled': colleges['tot_enroll']}))
                s.append(colleges['name'])
        if queries == colleges['state']:
            arr.append(({'title': colleges['name'], 'website': colleges['website'],'enrolled': colleges['tot_enroll']}))
    newlist = sorted(arr, key=lambda d: d['title']) 
    return newlist
@app.route("/")
def home():
    return render_template('base.html',title="sample html")

@app.route("/colleges")
def episodes_search():
    text = request.args.get("title")
    with open('colleges.json','r') as f:
        data = json.load(f)
    result = search_similarity(data, text)
    return result

# app.run(debug=True)