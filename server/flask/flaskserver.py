# -*- coding: utf-8 -*-
"""
Created on Tue Oct 25 14:49:32 2016

@author: Dave Ho
"""

#HOST&&PORT: http://127.0.0.1:5000/

import sqlite3
import flask
from flask import Flask
from flask import g
from flask import request
from flask import jsonify
from werkzeug.datastructures import ImmutableMultiDict
import ast

app = Flask(__name__)

DATABASE = 'database.db'

@app.route("/", methods=["GET", "POST"])
def hello():
    #if request.method == "GET":
    print "someone said get"
    return "JJ!"
    '''
    if request.method == "POST":
        content = request.get_json(silent=True)
        print content
        print "someone posted something"
        return ""
    '''

@app.route("/json", methods=['GET', 'POST'])
def json():
    dickeys = request.form.keys()
    dic = ast.literal_eval(dickeys[0])
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users VALUES('"+dic['phone']+"', '"+dic['phone']+"')")
    except sqlite3.IntegrityError:
        pass
    #c.execute("INSERT INTO users VALUES('"+dic['phone']+"', '"+dic['phone']+"')")
    # Needs try and except block
    c.execute('SELECT COUNT(pid) FROM path')
    count = c.fetchone()[0]
    c.execute("INSERT INTO path VALUES('"+str(count)+"', '"+dic['phone']+"', '"+dic['title']+"', '"+dic['zipCodeList'][0]+"')")   
    for i in range(0, len(dic['lat'])):
        c.execute("INSERT INTO points VALUES('"+str(count)+"', '"+str(dic['lat'][i])+"', '"+str(dic['lng'][i])+"', '"+str(i)+"')")
    for i in range(0, len(dic['markerMap'].keys())):
        key = sorted(dic['markerMap'].keys())[i]
        c.execute("INSERT INTO markers VALUES('"+str(count)+"', '"+str(dic['markerMap'][key]['lat'])+"', '"+str(dic['markerMap'][key]['lng'])+"', '"+dic['markerMap'][key]['description']+"', '"+dic['markerMap'][key]['image']+"')")
    conn.commit()
    conn.close()
    return request.json

@app.route("/getDetail", methods=["GET", "POST"])
def getDetail():
    if request.method == "GET":
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        # need to return titles back to android user from database
        """
        Android User Given: Zip Code of Current User Location
        What Server Needs to return: Given zip code of current user location, give back set of paths within that location using json
        """
        print "someone got some detail"
        return "You have gotten some detail"

@app.route("/getTitle", methods=["GET", "POST"])
def getTitle():
    if request.method == "GET":
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        # need to return full details back to android user from database
        """
        Android User Given: Phone + title of path selected
        What Server Needs to return: given phone and title of path return the dictionary json of that path
        """
        print "someone got some title"
        return "You have gotten some title"



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
    #app.run(host='0.0.0.0',port="80")