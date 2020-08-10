#!/bin/bash

umask 000
nginx
python manage.py db init
python manage.py db migrate
python manage.py db upgrade
uwsgi --ini app.ini --py-autoreload 1 --die-on-term