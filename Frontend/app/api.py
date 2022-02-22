from flask import request
import requests
import base64
from app import webapp
from app import DBUtile

import os

@webapp.route('/api/upload', methods=['POST'])
def upload_interface():

    # Check if miss image
    if request.files.get('file') == None or request.files['file'].getbuffer().nbytes == 0:
        return {
            "success": "false",
            "error": {
                "code": 404,
                "message": "Missing uploaded image"
            }
        }
    
    key = request.form.get("key")
    # Check if miss key
    if key == '' or key == None:
        return {
            "success": "false",
            "error": {
                "code": 404,
                "message": "Missing image key"
            }
        }

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
    return {
        "success": "true"
    }

@webapp.route('/api/list_keys', methods=['POST'])
def list_keys_interface():
    db = DBUtile.DBUtil()
    cursor = db.get_all_key()
    keylist = []
    for item in cursor:
        keylist.append(item[0])
    return {
        "success": "true",
        "keys": keylist
    }

@webapp.route('/api/key/<key_value>', methods=['POST'])
def retrieve_image_interface(key_value):
    db = DBUtile.DBUtil()
    cursor = db.get_location(key_value)
    address=""
    for loc in cursor:
        address = loc[0]
    # check if key is valid
    if address == "":
        return {
            "success": "false",
            "error": {
                "code": 404,
                "message": "Invalid key value"
            }
        }
    # put key and image into response
    image_string = ""
    with open(address, "rb") as image:
        image_string = base64.encodebytes(image.read()).decode('utf-8')
    return {
        "success": "true",
        "content": image_string
    }

