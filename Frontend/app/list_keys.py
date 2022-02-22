from flask import render_template

from app import webapp
from app import DBUtile

@webapp.route("/list_keys", methods=['GET'])
def list_keys():
    # get key data
    db = DBUtile.DBUtil()
    cursor = db.get_all_list()
    return render_template("list.html", cursor=cursor)

