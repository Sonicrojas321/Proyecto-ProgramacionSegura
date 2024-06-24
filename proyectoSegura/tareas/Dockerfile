FROM python:latest

RUN mkdir /tareas

WORKDIR /tareas

RUN useradd limitado -ms /bin/bash

USER limitado

CMD  ["python","mysocket.py"]
