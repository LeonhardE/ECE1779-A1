from flask import render_template, request

from app import webapp
from app import DBUtile

@webapp.route("/statistics", methods=['GET'])
def get_statistics():
    db = DBUtile.DBUtil()
    cursor = db.get_statistics()
    
    return render_template("statistics.html", title="Current Statistics", cursor=cursor)