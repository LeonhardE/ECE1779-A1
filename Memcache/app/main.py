import atexit

from apscheduler.schedulers.background import BackgroundScheduler
from app import webapp, memcache
from flask import json
from flask import render_template, url_for, request

# https://stackoverflow.com/questions/21214270/how-to-schedule-a-function-to-run-every-hour-on-flask
scheduler = BackgroundScheduler(daemon=True)
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
