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
    lst = []
    if size == 'small':
        query_sql = f"""SELECT * FROM colleges WHERE ((state = '{state_city}' OR city = '{state_city}') AND (tot_enroll < 5000))"""
    elif size == 'medium':
        query_sql = f"""SELECT * FROM colleges WHERE (state = '{state_city}' OR city = '{state_city}' AND (tot_enroll BETWEEN 5000 AND 15000))"""
    elif size == 'large':
        query_sql = f"""SELECT * FROM colleges WHERE (state = '{state_city}' OR city = '{state_city}' AND (tot_enroll > 15000))"""
    data = mysql_engine.query_selector(query_sql)
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


def sql_search2(region, size, sort):
    lst = []
    if size == 'small':
        if region == 'midwest':
            query_sql = f"""SELECT * FROM colleges WHERE ((state = 'IL' OR state = 'IN' OR state = 'MI'  OR state = 'OH' OR state = 'ND' OR state = 'SD' OR state = 'NE' OR state = 'KS' OR state = 'MN' OR state = 'IA' OR state = 'MO' OR state = 'WI') AND (tot_enroll < 5000))"""
        elif region == 'southwest':
            query_sql = f"""SELECT * FROM colleges WHERE ((state = 'TX' OR state = 'OK' OR state = 'NM' OR state ='AZ') AND (tot_enroll < 5000))"""
        elif region == 'west':
            query_sql = f"""SELECT * FROM colleges WHERE ((state = 'AK' OR state = 'HI' OR state = 'CO' OR state = 'WY' OR state = 'MT' OR state ='WA' OR state ='NV' OR state = 'CA' OR state = 'ID' or state = 'OR' OR state = 'UT') AND (tot_enroll < 5000))"""
        elif region == 'northeast':
            query_sql = f"""SELECT * FROM colleges WHERE ((state = 'DE' OR state = 'PA' OR state = 'NY' OR state = 'NJ' OR state = 'VT' OR state = 'NH' OR state = 'ME' OR state = 'MA' OR state = 'CT' OR state = 'RI' OR state = 'MD' ) AND (tot_enroll < 5000))"""
        elif region == 'southeast':
            query_sql = f"""SELECT * FROM colleges WHERE ((state = 'WV' OR state = 'VA' OR state = 'KY' OR state = 'TN' OR state = 'NC' OR state ='SC' OR state ='GA' OR state = 'AL' OR state = 'MS' or state = 'AR' OR state = 'LA' OR state='FL') AND (tot_enroll < 5000))"""
    elif size == 'medium':
        if region == "midwest":
            query_sql = f"""SELECT * FROM colleges WHERE ((state = 'IL' OR state = 'IN' OR state = 'MI'  OR state = 'OH' OR state = 'ND' OR state = 'SD' OR state = 'NE' OR state = 'KS' OR state = 'MN' OR state = 'IA' OR state = 'MO' OR state = 'WI') AND (tot_enroll BETWEEN 5000 AND 15000))"""
        elif region == "southwest":
            query_sql = f"""SELECT * FROM colleges WHERE ((state = 'TX' OR state = 'OK' OR state = 'NM' OR state ='AZ') AND (tot_enroll BETWEEN 5000 AND 15000))"""
        elif region == "west":
            query_sql = f"""SELECT * FROM colleges WHERE ((state = 'AK' OR state = 'HI' OR state = 'CO' OR state = 'WY' OR state = 'MT' OR state ='WA' OR state ='NV' OR state = 'CA' OR state = 'ID' or state = 'OR' OR state = 'UT') AND (tot_enroll BETWEEN 5000 AND 15000))"""
        elif region == "northeast":
            query_sql = f"""SELECT * FROM colleges WHERE ((state = 'DE' OR state = 'PA' OR state = 'NY' OR state = 'NJ'  OR state = 'VT' OR state = 'NH' OR state = 'ME' OR state = 'MA' OR state = 'CT' OR state = 'RI' OR state = 'MD' ) AND (tot_enroll BETWEEN 5000 AND 15000))"""
        elif region == "southeast":
            query_sql = f"""SELECT * FROM colleges WHERE ((state = 'WV' OR state = 'VA' OR state = 'KY' OR state = 'TN' OR state = 'NC' OR state ='SC' OR state ='GA' OR state = 'AL' OR state = 'MS' or state = 'AR' OR state = 'LA' OR state='FL') AND (tot_enroll BETWEEN 5000 AND 15000))"""
    elif size == 'large':
        if region == "midwest":
            query_sql = f"""SELECT * FROM colleges WHERE ((state = 'IL' OR state = 'IN' OR state = 'MI'  OR state = 'OH' OR state = 'ND' OR state = 'SD' OR state = 'NE' OR state = 'KS' OR state = 'MN' OR state = 'IA' OR state = 'MO' OR state = 'WI') AND (tot_enroll > 15000))"""
        elif region == "southwest":
            query_sql = f"""SELECT * FROM colleges WHERE ((state = 'TX' OR state = 'OK' OR state = 'NM' OR state ='AZ') AND (tot_enroll > 15000))"""
        elif region == "west":
            query_sql = f"""SELECT * FROM colleges WHERE ((state = 'AK' OR state = 'HI' OR state = 'CO' OR state = 'WY' OR state = 'MT' OR state ='WA' OR state ='NV' OR state = 'CA' OR state = 'ID' or state = 'OR' OR state = 'UT') AND (tot_enroll > 15000))"""
        elif region == "northeast":
            query_sql = f"""SELECT * FROM colleges WHERE ((state = 'DE' OR state = 'PA' OR state = 'NY' OR state = 'NJ'  OR state = 'VT' OR state = 'NH' OR state = 'ME' OR state = 'MA' OR state = 'CT' OR state = 'RI' OR state = 'MD' ) AND (tot_enroll > 15000))"""
        elif region == "southeast":
            query_sql = f"""SELECT * FROM colleges WHERE ((state = 'WV' OR state = 'VA' OR state = 'KY' OR state = 'TN' OR state = 'NC' OR state ='SC' OR state ='GA' OR state = 'AL' OR state = 'MS' or state = 'AR' OR state = 'LA' OR state='FL') AND (tot_enroll > 15000))"""
    data = mysql_engine.query_selector(query_sql)
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


def sql_search3(state_city, region, size, sort):
    lst = []
    if size == 'small':
        if region == 'midwest':
            query_sql = f"""SELECT * FROM colleges WHERE ((state = 'IL' OR state = 'IN' OR state = 'MI'  OR state = 'OH' OR state = 'ND' OR state = 'SD' OR state = 'NE' OR state = 'KS' OR state = 'MN' OR state = 'IA' OR state = 'MO' OR state = 'WI') AND (tot_enroll < 5000) AND (state = '{state_city}' OR city = '{state_city}'))"""
        elif region == 'southwest':
            query_sql = f"""SELECT * FROM colleges WHERE ((state = 'TX' OR state = 'OK' OR state = 'NM' OR state ='AZ') AND (tot_enroll < 5000))"""
        elif region == 'west':
            query_sql = f"""SELECT * FROM colleges WHERE ((state = 'AK' OR state = 'HI' OR state = 'CO' OR state = 'WY' OR state = 'MT' OR state ='WA' OR state ='NV' OR state = 'CA' OR state = 'ID' or state = 'OR' OR state = 'UT') AND (tot_enroll < 5000) AND (state = '{state_city}' OR city = '{state_city}'))"""
        elif region == 'northeast':
            query_sql = f"""SELECT * FROM colleges WHERE ((state = 'DE' OR state = 'PA' OR state = 'NY' OR state = 'NJ' OR state = 'VT' OR state = 'NH' OR state = 'ME' OR state = 'MA' OR state = 'CT' OR state = 'RI' OR state = 'MD' ) AND (tot_enroll < 5000) AND (state = '{state_city}' OR city = '{state_city}'))"""
        elif region == 'southeast':
            query_sql = f"""SELECT * FROM colleges WHERE ((state = 'WV' OR state = 'VA' OR state = 'KY' OR state = 'TN' OR state = 'NC' OR state ='SC' OR state ='GA' OR state = 'AL' OR state = 'MS' or state = 'AR' OR state = 'LA' OR state='FL') AND (tot_enroll < 5000) AND (state = '{state_city}' OR city = '{state_city}'))"""
    elif size == 'medium':
        if region == "midwest":
            query_sql = f"""SELECT * FROM colleges WHERE ((state = 'IL' OR state = 'IN' OR state = 'MI'  OR state = 'OH' OR state = 'ND' OR state = 'SD' OR state = 'NE' OR state = 'KS' OR state = 'MN' OR state = 'IA' OR state = 'MO' OR state = 'WI') AND (tot_enroll BETWEEN 5000 AND 15000) AND (state = '{state_city}' OR city = '{state_city}'))"""
        elif region == "southwest":
            query_sql = f"""SELECT * FROM colleges WHERE ((state = 'TX' OR state = 'OK' OR state = 'NM' OR state ='AZ') AND (tot_enroll BETWEEN 5000 AND 15000) AND (state = '{state_city}' OR city = '{state_city}'))"""
        elif region == "west":
            query_sql = f"""SELECT * FROM colleges WHERE ((state = 'AK' OR state = 'HI' OR state = 'CO' OR state = 'WY' OR state = 'MT' OR state ='WA' OR state ='NV' OR state = 'CA' OR state = 'ID' or state = 'OR' OR state = 'UT') AND (tot_enroll BETWEEN 5000 AND 15000) AND (state = '{state_city}' OR city = '{state_city}'))"""
        elif region == "northeast":
            query_sql = f"""SELECT * FROM colleges WHERE ((state = 'DE' OR state = 'PA' OR state = 'NY' OR state = 'NJ'  OR state = 'VT' OR state = 'NH' OR state = 'ME' OR state = 'MA' OR state = 'CT' OR state = 'RI' OR state = 'MD' ) AND (tot_enroll BETWEEN 5000 AND 15000) AND (state = '{state_city}' OR city = '{state_city}'))"""
        elif region == "southeast":
            query_sql = f"""SELECT * FROM colleges WHERE ((state = 'WV' OR state = 'VA' OR state = 'KY' OR state = 'TN' OR state = 'NC' OR state ='SC' OR state ='GA' OR state = 'AL' OR state = 'MS' or state = 'AR' OR state = 'LA' OR state='FL') AND (tot_enroll BETWEEN 5000 AND 15000) AND (state = '{state_city}' OR city = '{state_city}'))"""
    elif size == 'large':
        if region == "midwest":
            query_sql = f"""SELECT * FROM colleges WHERE ((state = 'IL' OR state = 'IN' OR state = 'MI'  OR state = 'OH' OR state = 'ND' OR state = 'SD' OR state = 'NE' OR state = 'KS' OR state = 'MN' OR state = 'IA' OR state = 'MO' OR state = 'WI') AND (tot_enroll > 15000) AND (state = '{state_city}' OR city = '{state_city}'))"""
        elif region == "southwest":
            query_sql = f"""SELECT * FROM colleges WHERE ((state = 'TX' OR state = 'OK' OR state = 'NM' OR state ='AZ') AND (tot_enroll > 15000) AND (state = '{state_city}' OR city = '{state_city}'))"""
        elif region == "west":
            query_sql = f"""SELECT * FROM colleges WHERE ((state = 'AK' OR state = 'HI' OR state = 'CO' OR state = 'WY' OR state = 'MT' OR state ='WA' OR state ='NV' OR state = 'CA' OR state = 'ID' or state = 'OR' OR state = 'UT') AND (tot_enroll > 15000) AND (state = '{state_city}' OR city = '{state_city}'))"""
        elif region == "northeast":
            query_sql = f"""SELECT * FROM colleges WHERE ((state = 'DE' OR state = 'PA' OR state = 'NY' OR state = 'NJ'  OR state = 'VT' OR state = 'NH' OR state = 'ME' OR state = 'MA' OR state = 'CT' OR state = 'RI' OR state = 'MD' ) AND (tot_enroll > 15000) AND (state = '{state_city}' OR city = '{state_city}'))"""
        elif region == "southeast":
            query_sql = f"""SELECT * FROM colleges WHERE ((state = 'WV' OR state = 'VA' OR state = 'KY' OR state = 'TN' OR state = 'NC' OR state ='SC' OR state ='GA' OR state = 'AL' OR state = 'MS' or state = 'AR' OR state = 'LA' OR state='FL') AND (tot_enroll > 15000) AND (state = '{state_city}' OR city = '{state_city}'))"""
    data = mysql_engine.query_selector(query_sql)
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
    region = request.args.get("location")
    print(region)
    if region == "":
        result = sql_search(state_city.upper(), size, request.args.get("sort"))
    elif state_city == "":
        result = sql_search2(region.lower(), size, request.args.get("sort"))
    elif region != "" and state_city != "":
        result = sql_search3(state_city.upper(),
                             region.lower(), size, request.args.get("sort"))
    return result


app.run(debug=True)
