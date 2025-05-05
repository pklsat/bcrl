# 概要
status.jsonを監視してmain.pyを実行するスクリプト。

# 実行
```bash
# 30秒ごとに実行
status_monitor.py 30
```

# APPサーバに実装してほしい部分
- bcrlmockの実装
    - main.py
        - リクエストのデータ/shared/bcrlapi/request/{uuid}.jsonを読み込む
        - 実行結果のレスポンスを/shared/bcrlapi/response/{uuid}.jsonに書き込む
    - status_monitor.py(bcrlmock)の実装
        - 定期的にstatus.jsonを読み込み、statusがPendingのリクエストを取得する
        - status.jsonのuuidのstatusをPendingからProcessingに変更し、main.pyを実行する
        - 処理が完了したらstatus.jsonのuuidのstatusをProcessingからCompletedに変更する
