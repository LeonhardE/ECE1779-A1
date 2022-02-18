import atexit
import base64
from io import BytesIO
from PIL import Image

from apscheduler.schedulers.background import BackgroundScheduler
from app import webapp, memcache
from flask import json
from flask import render_template, url_for, request

scheduler = BackgroundScheduler({'apscheduler.timezone': 'EST'})
scheduler.add_job(func=memcache.write_statistics, trigger="interval", seconds=5)

# shut down the scheduler when terminating
atexit.register(lambda: scheduler.shutdown())

@webapp.route('/')
def main():
    scheduler.start()

    return render_template("main.html")


@webapp.route('/get', methods=['POST'])
def get():
    key = request.form.get('key')

    value = memcache.get(key)
    if value != -1:
        response = webapp.response_class(
            response=json.dumps(value),
            status=200,
            mimetype='application/json'
        )
    else:
        response = webapp.response_class(
            response=json.dumps("MISS"),
            status=200,
            mimetype='application/json'
        )

    print(memcache)
    return response


@webapp.route('/put', methods=['POST'])
def put():
    key = request.form.get('key')

    value = request.form.get('value')
    if memcache.put(key, value) != -1:
        response = webapp.response_class(
            response=json.dumps("OK"),
            status=200,
            mimetype='application/json'
        )
    else:
        response = webapp.response_class(
            response=json.dumps("OUT_OF_CAPACITY"),
            status=400,
            mimetype='application/json'
        )

    print(memcache)
    return response


@webapp.route('/clear', methods=['POST'])
def clear():
    memcache.clear()

    response = webapp.response_class(
        response=json.dumps("OK"),
        status=200,
        mimetype='application/json'
    )

    return response


@webapp.route('/invalidateKey', methods=['POST'])
def invalidateKey():
    key = request.form.get('key')

    if memcache.invalidate_key(key) != -1:
        response = webapp.response_class(
            response=json.dumps("OK"),
            status=200,
            mimetype='application/json'
        )
    else:
        response = webapp.response_class(
            response=json.dumps("UNKNOWN_KEY"),
            status=400,
            mimetype='application/json'
        )

    return response


@webapp.route('/refreshConfiguration', methods=['POST'])
def refreshConfiguration():
    memcache.refresh_config()

    response = webapp.response_class(
        response=json.dumps("OK"),
        status=200,
        mimetype='application/json'
    )

    return response


# test functionalities
@webapp.route('/testPut', methods=['POST'])
def testPut():
    key = request.form.get('key')

    image = request.files['myImg']
    image_string = base64.b64encode(image.read())
    if memcache.put(key, image_string) != -1:
        response = webapp.response_class(
            response=json.dumps("OK"),
            status=200,
            mimetype='application/json'
        )
    else:
        response = webapp.response_class(
            response=json.dumps("OUT_OF_CAPACITY"),
            status=400,
            mimetype='application/json'
        )

    print(memcache)
    return response


@webapp.route('/testGet', methods=['POST'])
def testGet():
    key = request.form.get('key')

    if memcache.get(key) != -1:
        image_string = memcache.get(key).decode("utf-8")
        # image = Image.open(BytesIO(base64.b64decode(image_string)))
        # image.show()

        print(memcache)
        return render_template("main.html", image=image_string)

    print(memcache)
    return render_template("main.html")
