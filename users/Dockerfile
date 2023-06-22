FROM ubuntu:20.04
# FROM python:3.8-slim-buster

COPY . /home/app

ARG DEBIAN_FRONTEND=noninteractive

ENV TZ=America/Bogota

RUN apt-get update && apt-get install -y gnupg2

RUN apt-get install curl -y \
&& apt install software-properties-common -y \
&& apt-get install libxml2-dev libxslt1-dev -y 


RUN apt-key adv --recv-keys --keyserver keyserver.ubuntu.com 0xcbcb082a1bb943db && curl -LsS https://downloads.mariadb.com/MariaDB/mariadb_repo_setup | bash

RUN apt-get install apt-transport-https -y \
&& apt-get update -y \
&& apt-get upgrade -y 

RUN apt-get install build-essential -y \
&& apt-get install libmariadb3 -y \
&& apt-get install libmariadb-dev -y 

RUN apt-get install -y python3.9 \
&& apt install -y python3-pip


RUN pip install -r /home/app/requirements.txt

# RUN python3.8 /home/app/manage.py runserver 8002

# CMD ["gunicorn","--bind","0.0.0.0:8002","sp_service_users.wsgi","-t","600"]
