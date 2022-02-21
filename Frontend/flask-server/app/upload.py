from flask import render_template, request
from app import webapp
from app import DBUtile

import os

@webapp.route('/UploadForm', methods=['GET'])
def upload_form():
    return render_template("fileupload/form.html")

@webapp.route('/api/upload', methods=['POST'])
def upload_image():

    # Check if miss image
    if request.files['file'].getbuffer().nbytes == 0:
        return {
            "success": "false",
            "error": {
                "code": 404,
                "message": "Missing uploaded image"
            }
        }
    
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
    
    # ToDo: check if key exist in Memcache

    # Save the image
    new_image = request.files['file']
    fname = os.path.join('app/static', key)
    new_image.save(fname)
    # Write key and fname in MySQL if it is not in database yet
    db = DBUtile.DBUtil()
    keyset = db.get_all_key()
    if key not in keyset:
        db.put_image_key(key, fname)
    return {
        "success": "true"
    }


