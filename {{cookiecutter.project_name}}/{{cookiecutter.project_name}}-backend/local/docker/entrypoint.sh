#!/bin/sh
sleep 5
python3 /var/code/backend/manage.py migrate
python3 /var/code/backend/manage.py runserver 0.0.0.0:8000
