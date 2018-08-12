#!/usr/bin/env bash
python3 manage.py migrate
uwsgi --http :8080 --wsgi-file /src/linklab_backend/wsgi.py --static-map /static=/src/static/ --master --processes 4 --threads 2
