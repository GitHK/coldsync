FROM python:3.7.3-alpine

COPY . /app
WORKDIR /app

RUN pip install -e .
