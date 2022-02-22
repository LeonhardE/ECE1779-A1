from flask import render_template, request
import requests
import base64
from app import webapp
from app import DBUtile

import os

@webapp.route('/SearchForm', methods=['GET'])
def search_form():
    return render_template("search/form.html")

@webapp.route('/search', methods=['POST'])
def search_img():
    
    key = request.form.get("key")
    # Get from memcache
    data = dict(key=key)
    response = requests.post("http://localhost:5001/get", data=data)    
    if response.json() == "MISS":
        # key not in memcache
        # read from local file system
        db = DBUtile.DBUtil()
        cursor = db.get_location(key)
        address=""
        for loc in cursor:
            address = loc[0]
        # check if key is valid
        if address == "":
            return render_template("search/notfound.html")
        # put key and image into memcache
        image_string = ""
        with open(address, "rb") as image:
            image_string = base64.b64encode(image.read())
        data = dict(key=key, value=image_string)
        response = requests.post("http://localhost:5001/put", data=data)
        print(response.text)
        # render page
        return render_template("search/view.html", address=address[4:])
    else:
        # key in memcache
        # use the value in cache
        imagestring = response.json()
        return render_template("search/viewcache.html", image=imagestring)


