#!/bin/sh

./bin/run-common.sh
./manage.py collectstatic --noinput -c
gunicorn masterfirefoxos.wsgi:application -b 0.0.0.0:80 -w 2 --log-file -
