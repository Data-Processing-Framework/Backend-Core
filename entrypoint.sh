#!/bin/sh

if [ "$DEBUG" = "1" ]; then
    while true; do sleep 10; done
else
    exec gunicorn --bind 0.0.0.0:5000 run:app -t 6000 -k gevent --worker-connections 20
fi
