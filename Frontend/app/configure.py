from flask import render_template, request

from app import webapp
from app import DBUtile

@webapp.route("/ConfigForm", methods=['GET'])
def config_form():
    return render_template("configure/form.html")

@webapp.route("/SetConfig", methods=['POST'])
def set_configure():
    capacity = request.form.get('capacity')
    policy = request.form.get('policy')

    db = DBUtile.DBUtil()
    cursor = db.set_config(capacity, policy)
    return "OK"