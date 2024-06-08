#!/bin/bash
sleep 15; cd /code; python3 manage.py makemigrations; python3 manage.py migrate; gunicorn --bind :8000 proyectoSegura.wsgi:application --reload