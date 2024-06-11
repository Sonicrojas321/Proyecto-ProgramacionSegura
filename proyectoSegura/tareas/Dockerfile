FROM python:latest

RUN mkdir /revision
WORKDIR /revision

COPY ./evaluador.py /revision/evaluador.py
COPY ./inyectar.py /revision/inyectar.py
 
COPY ./entrada.txt /revision/entrada.txt
COPY ./respuesta.py /revision/respuesta.py

RUN chmod +x /revision/inyectar.py
RUN chmod +x /revision/evaluador.py

CMD  ["python","evaluador.py","respuesta.py","entrada.txt"]