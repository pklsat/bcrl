# 概要
python製のhttpクライアント。APIサーバに対して非同期でリクエストを送信する。
sequence.jsonにリクエストの順番を定義し、実行時に引数として指定する。
sequence.jsonの"req_body"のvalueをrequest_data.jsonのkeyとしてリクエストボディを定義する。

- ディレクトリ構成
```
clientmock/
  app/
    ├── __init__.py
    ├── main.py
    ├── request_data.json
    ├── sequence.json
    ├── sequence2.json
    ...
  Dockerfile
```

# 実行
```bash
# シーケンスファイルを指定して実行
main.py sequence.json
```