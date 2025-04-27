FROM python:3.13-slim

WORKDIR /fastapi

# キャッシュを利用するためにCOPYを分割
COPY ./requirements.txt /fastapi/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /fastapi/requirements.txt

COPY . /fastapi

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]