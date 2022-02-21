# syntax=docker/dockerfile:1
FROM ubuntu:20.04
WORKDIR /code
RUN apt-get update && apt-get install -y python3-pip --fix-missing
RUN alias python=python3
COPY requirements.txt req.txt
RUN pip3 install -r req.txt
EXPOSE 8000
COPY . .
