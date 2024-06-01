#!/usr/bin/env/ bash
activado=''
while read line; do
	activado='1'
	export "$line"
done < <(ccdecrypt -c ./secrets.env.cpt)
test "$activado" || { echo "No se pasó correctamente la contraseña"; exit 1;}
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py runserver

gunicorn --bind :8000 inseguro.wsgi:application --reload