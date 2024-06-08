FROM python:latest

RUN mkdir /code
WORKDIR /code

COPY proyectoSegura/requirements.txt /code/requirements.txt

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

RUN mkdir /start 

COPY ./proyectoSegura /code
COPY ./proyectoSegura/start.sh /start

RUN chmod +x /start/start.sh

CMD  ["bash","/start/start.sh"]