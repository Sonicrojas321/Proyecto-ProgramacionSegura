FROM python:latest

RUN apt-get update

RUN mkdir /code
WORKDIR /code

COPY proyectoSegura/requirements.txt /code/requirements.txt

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

RUN mkdir /start 

COPY ./proyectoSegura /code
COPY ./proyectoSegura/start.sh /start

RUN chmod +x /start/start.sh

RUN mkdir /tareas

RUN useradd limitado -s /bin/bash
RUN chown limitado:limitado -R /tareas

#RUN usermod -aG docker limitado

USER limitado

CMD  ["bash","/start/start.sh"]