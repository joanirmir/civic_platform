FROM python:3.8-slim-buster

# every python output is send to container log
ENV PYTHONUNBUFFERED=1
ENV RUN_IN_DOCKER=True
ENV DB_HOST=db

WORKDIR /django

COPY . .

RUN apt update &&\
    apt install -y gdal-bin libmagic1 postgis 
RUN pip install -r requirements.txt

