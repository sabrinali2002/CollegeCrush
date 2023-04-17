import json
import os
import csv
import sys
from flask import Flask, render_template, request
from flask_cors import CORS
from helpers.MySQLDatabaseHandler import MySQLDatabaseHandler

# ROOT_PATH for linking with all your files.
# Feel free to use a config.py or settings.py with a global export variable
os.environ['ROOT_PATH'] = os.path.abspath(os.path.join("..", os.curdir))

# These are the DB credentials for your OWN MySQL
# Don't worry about the deployment credentials, those are fixed
# You can use a different DB name if you want to
MYSQL_USER = "root"
MYSQL_USER_PASSWORD = "Xuannhi230902!"
MYSQL_PORT = 3306
MYSQL_DATABASE = "colleges"

mysql_engine = MySQLDatabaseHandler(
    MYSQL_USER, MYSQL_USER_PASSWORD, MYSQL_PORT, MYSQL_DATABASE)

# Path to init.sql file. This file can be replaced with your own file for testing on localhost, but do NOT move the init.sql file
mysql_engine.load_file_into_db()

app = Flask(__name__)
CORS(app)

# Sample search, the LIKE operator in this case is hard-coded,
# but if you decide to use SQLAlchemy ORM framework,
# there's a much better and cleaner way to do this


# def sql_search(episode):
#     query_sql = f"""SELECT * FROM episodes WHERE LOWER( title ) LIKE '%%{episode.lower()}%%' limit 10"""
#     keys = ["id","title","descr"]
#     data = mysql_engine.query_selector(query_sql)
#     return json.dumps([dict(zip(keys,i)) for i in data])

# @app.route("/")
# def home():
#     return render_template('base.html',title="sample html")

# @app.route("/episodes")
# def episodes_search():
#     text = request.args.get("title")
#     return sql_search(text)

def sql_search(state_city, size, sort):
    # region_dic = {}
    # region_dic['east'] = set(
    #     ['WA', 'OR', 'ID', 'MT', 'WY', 'CA', 'NV', 'UT', 'AZ', 'NM', 'CO'])
    # region_dic['midwest'] = set(
    #     ['ND', 'SD', 'NE', 'KS', 'MN', 'IA', 'MO', 'WI', 'IL', 'IN', 'MI', 'IN', 'OH'])
    # region_dic['west'] = set(
    #     ['PA', 'NY', 'NJ', 'VT', 'NH', 'ME', 'MA', 'CT', 'RI'])
    # region_dic['south'] = set(['TX', 'OK', 'AR', 'LA', 'MS', 'TN', 'KY', 'AL', 'GA', 'FL', 'WV',
    #                            'NC', 'VA', 'MD', 'DE', 'NC', 'SC'])
    lst = []
    if size == 'small':
        query_sql = f"""SELECT * FROM colleges WHERE ((state = '{state_city}' OR city = '{state_city}') AND (tot_enroll < 5000))"""
    elif size == 'medium':
        query_sql = f"""SELECT * FROM colleges WHERE (state = '{state_city}' OR city = '{state_city}' AND (tot_enroll BETWEEN 5000 AND 15000))"""
    elif size == 'large':
        query_sql = f"""SELECT * FROM colleges WHERE (state = '{state_city}' OR city = '{state_city}' AND (tot_enroll > 15000))"""
    # if state in region_dic['east']:
    # elif state in region_dic['midwest']:
    # elif state in region_dic['west']:
    # elif state in region_dic['west']:
    data = mysql_engine.query_selector(query_sql)
    # query_sql_test = f"""SELECT * FROM data WHERE state = '{NY}'"""
    # data = mysql_engine.query_selector(query_sql_test)
    # print(list(data))
    for elem in list(data):
        name = elem[0]
        city = elem[1]
        state = elem[2]
        website = elem[5]
        enroll = elem[6]
        lst.append(({'title': name, 'location': city + ", "+state,
                   'enrolled': enroll, 'website': website}))
    if sort == "Alphabetical":
        lst = sorted(lst, key=lambda d: d['title'])
    # elif sort_input == "Location":  #maybe we could incorporate text comparison element here
    #     lst = sorted(arr, key=lambda d: d['location'])
    elif sort == "Enrollment Size":
        lst = sorted(lst, key=lambda d: int(d['enrolled']))
    return lst


@app.route("/")
def home():
    return render_template('base.html', title="sample html")


@app.route("/colleges")
def college_search():
    state_city = request.args.get("title")
    size = request.args.get("size")
    result = sql_search(state_city.upper(), size, request.args.get(
        "sort"))
    return result


app.run(debug=True)
