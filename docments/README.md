# 仕様
まずは正常系を作る。
## APIサーバとAPPサーバとのI/F
APPサーバとAPIサーバのI/Fはファイルの入出力とする。コンテナ間でdocker volumeを共有し、I/Fとするファイルはsharedボリューム内にまとめる。  
コンテナ内では共有ディレクトリは以下のように見える。
```
/shared/bcrlapi/
        request/
            {uuid}.json
            status.json
        response/
            {uuid}.json
```

データフローはsystem components.drawio.svgおよびsequence.md参照。


## statusのパラメータ
以下のように定義する。
- Pending: 処理待ち
- Processing: 処理中
- Completed: 処理完了

## TBD
- status.jsonの排他制御
- 蓄積するデータの定期アーカイブ・削除
- 並列処理したいリクエスト数
- job履歴の件数

# テスト用mock
テスト用にbcrlmock(APPサーバ)とclientmockを作成する。
詳細は各mockを参照。

# 検討過程
## APPサーバの仕様
- APIがたたかれる頻度：5分に1回
- 処理時間：1リクエストあたり数分

## APIサーバの実装検討
APIの実行頻度が低く、処理速度はそんなに必要ないので案3を採用。
### 案1：APPサーバをそのままAPIサーバ化する
研究室のメンバーでAPIサーバを実装する。APIサーバの改修でAPPサーバに影響が出やすい。APIサーバをスケールしにくい。
- 実装難易度：×
- 運用：×
- 処理速度：〇

### 案2：APIサーバは分離するが、APPサーバにもAPI実装する
APIサーバを独立させることでスケールしやすくなる。APPサーバにAPIを実装することのハードルが高そう。
- 実装難易度：△
- 運用：〇
- 処理速度：△

### 案3：APIサーバは分離し、APPサーバとのI/Fをファイルの入出力にする
I/Fをファイルの入出力にすることでAPPサーバ側の実装難易度を下げる。処理速度で劣る。
- 実装難易度：〇
- 運用：〇
- 処理速度：×

## APPサーバの監視間隔
短すぎるとCPUを食いそうなので、とりあえず1分間隔で監視する。
性能に応じて変更する。

# APPサーバに実装してほしい部分
- bcrlmockの実装
    - main.py
        - リクエストのデータ/shared/bcrlapi/request/{uuid}.jsonを読み込む
        - 実行結果のレスポンスを/shared/bcrlapi/response/{uuid}.jsonに書き込む
    - status_monitor.py(bcrlmock)の実装
        - 定期的にstatus.jsonを読み込み、statusがPendingのリクエストを取得する
        - status.jsonのuuidのstatusをPendingからProcessingに変更し、main.pyを実行する
        - 処理が完了したらstatus.jsonのuuidのstatusをProcessingからCompletedに変更する

# APIの非同期化
リクエストの応答に数分かかるため、APIを分割して非同期化する。
1. リクエストを出して、進捗状況を取得するAPI
2. 進捗状況を取得するAPI
3. 結果を取得するAPI

# status.jsonの更新時間
status.json を書き直す際の処理時間は以下の通り。  

| ジョブ件数 | 書き込み所要時間 |
| ------ | -------------- |
| 10     | 約 **0.0003 秒** |
| 100    | 約 **0.0027 秒** |
| 1,000  | 約 **0.022 秒**  |
| 5,000  | 約 **0.13 秒**   |
| 10,000 | 約 **0.23 秒**   |
| 20,000 | 約 **0.43 秒**   |

ユーザが100人が30分に1回のジョブの実行頻度で、１日あたり4800回のジョブを実行することを想定すると、１日でstatus.jsonをアーカイブして更新する必要がありそう。  
履歴の管理のために日付ごとにstatus.jsonを分けて参照できるようにしたい。