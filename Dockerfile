FROM ubuntu:latest

RUN apt-get update -y && \
    apt-get install -y python-pip python-dev build-essential rabbitmq-server 

COPY . /app

COPY ./entrypoint.sh /app/entrypoint.sh

WORKDIR /app

RUN pip install -r requirements.txt

RUN pip install nose2[coverage_plugin]>=0.6.5

ENV BASEURL "https://service-homolog.digipix.com.br/v0b"

RUN [ "chmod", "+x", "/app/entrypoint.sh" ]