FROM python:latest

RUN apt-get update
#RUN apt install ca-certificates curl gnupg
#RUN install -m 0755 -d /etc/apt/keyrings
#RUN curl -fsSL https://download.docker.com/linux/debian/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg
#RUN chmod a+r /etc/apt/keyrings/docker.gpg
#RUN echo "deb [arch=amd64 signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/debian bookworm stable\ndeb-src [arch=amd64 signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/debian bookworm stable" > /etc/apt/sources.list.d/docker.list
 
#RUN apt install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin -y

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

RUN groupadd -g 998 docker
RUN useradd -u 1001 limitado -ms /bin/bash
RUN chown limitado:limitado -R /tareas
RUN chown limitado:limitado -R /code/db/migrations

RUN usermod -aG docker limitado


USER limitado

CMD  ["bash","/start/start.sh"]
