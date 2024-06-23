#!/bin/bash
sleep 15; cd /code; python manage.py makemigrations; python manage.py migrate; gunicorn --bind :8000 proyectoSegura.wsgi:application --reload