FROM python:3.13-slim

COPY ./requirements.txt /bcrlapi/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /bcrlapi/requirements.txt

COPY . /bcrlapi

