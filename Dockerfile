FROM python:3.7.3-alpine

RUN apk update && apk add curl

# Add kubectl to container
RUN curl -LO https://storage.googleapis.com/kubernetes-release/release/$(curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt)/bin/linux/amd64/kubectl
RUN chmod +x ./kubectl
RUN mv ./kubectl /usr/local/bin

COPY . /app
WORKDIR /app

RUN pip install -e .
