from flask import render_template, request

import requests
from app import webapp
from app import DBUtile

@webapp.route("/ConfigForm", methods=['GET'])
def config_form():
    return render_template("configure/form.html")

@webapp.route("/SetConfig", methods=['POST'])
def set_configure():
    capacity = request.form.get('capacity')
    policy = request.form.get('policy')
    
    # check if the capacity is valid
    if capacity.isdigit():
        db = DBUtile.DBUtil()
        db.set_config(capacity, policy)
        return render_template("configure/success.html")
    else:
        return render_template("configure/error.html")

@webapp.route("/ClearMem", methods=['POST'])
def clear_mem():
    # clear all keys in memcache
    response = requests.post("http://localhost:5001/clear")   
    print(response.text)
    return render_template("configure/success.html")

