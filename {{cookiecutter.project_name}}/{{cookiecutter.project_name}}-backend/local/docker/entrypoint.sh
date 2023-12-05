#!/bin/sh
sleep 5
python /var/code/backend/manage.py migrate
python /var/code/backend/manage.py runserver 0.0.0.0:8000
