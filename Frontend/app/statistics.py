from flask import render_template

from app import webapp
from app import DBUtile

@webapp.route("/statistics", methods=['GET'])
def get_statistics():
    db1 = DBUtile.DBUtil()
    db2 = DBUtile.DBUtil()
    cursor = db1.get_history()
    current = db2.get_current()
    
    return render_template("statistics.html", cursor=cursor, current=current)