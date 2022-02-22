from flask import render_template, request
import requests
from app import webapp
from app import DBUtile

import os

@webapp.route('/UploadForm', methods=['GET'])
def upload_form():
    return render_template("fileupload/form.html")

@webapp.route('/upload', methods=['POST'])
def upload_image():

    key = request.form.get("key")

    # Save the image
    new_image = request.files['file']
    fname = os.path.join('app/static/images', key)
    new_image.save(fname)
    # Invalidate key in Memcache
    data = dict(key=key)
    response = requests.post("http://localhost:5001/invalidateKey", data=data)
    print(response.text)
    # Write key and fname in MySQL if it is not in database yet
    db = DBUtile.DBUtil()
    keyset = db.get_all_key()
    flag = True
    for item in keyset:
        if key in item:
            flag = False
    if flag:
        db.put_image_key(key, fname)
    return render_template("fileupload/success.html")


