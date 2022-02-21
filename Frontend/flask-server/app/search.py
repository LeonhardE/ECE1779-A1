from flask import render_template, request
from app import webapp
from app import DBUtile

import os

@webapp.route('/SearchForm', methods=['GET'])
def search_form():
    return render_template("search/form.html")

@webapp.route('/search', methods=['POST'])
def search_img():
    
    key = request.form.get("key")
    # Check if miss key
    if key == '':
        return {
            "success": "false",
            "error": {
                "code": 404,
                "message": "Missing image key"
            }
        }
    
    
    # get image location
    db = DBUtile.DBUtil()
    cursor = db.get_location(key)
    for loc in cursor:
        address = loc[0]
        print(address)
    return render_template("search/view.html", address=address[4:])


