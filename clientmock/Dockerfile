FROM python:3.13-slim

COPY ./requirements.txt /clientmock/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /clientmock/requirements.txt

COPY . /clientmock