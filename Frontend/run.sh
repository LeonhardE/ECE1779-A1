#!/bin/bash

gunicorn --bind 0.0.0.0:5000 --workers=3 --worker-class gevent wsgi:webapp