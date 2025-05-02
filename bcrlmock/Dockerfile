FROM python:3.13-slim

COPY ./requirements.txt /bcrlmock/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /bcrlmock/requirements.txt

COPY . /bcrlmock