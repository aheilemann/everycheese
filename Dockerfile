FROM python:3.8-slim-buster

# install dependencies
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y gcc && \
    apt-get clean

# set environment variables
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# set working directory
RUN mkdir /code
WORKDIR /code

#install requirements
RUN pip install --upgrade pip
RUN mkdir requirements
COPY requirements/base.txt /code/requirements/
COPY requirements/local.txt /code/requirements/
RUN pip install -r requirements/local.txt

#copy project
COPY . /code/
