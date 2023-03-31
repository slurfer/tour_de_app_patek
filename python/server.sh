#!/bin/sh
nginx &
# flask run --host=0.0.0.0 >> /usr/share/nginx/html/python-log.log 2>&1
flask run --host=0.0.0.0