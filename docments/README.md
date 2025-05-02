# 仕様
まずは正常系を作る。
## APPサーバとのI/F
APPサーバとAPIサーバのI/Fはファイルの入出力とする。I/Fとするファイル群はdockerのsharedボリューム内にまとめる。  

UUIDをリクエストIDとして使用する。  
APPサーバとのI/FはAPIからみて出力をrequest/{uuid}.json、入力をresponse/{uuid}.jsonとする。
リクエスト毎にUUIDを生成し、リクエストの内容をrequest/{uuid}.jsonに書き込む。
{uuid}.jsonファイル内にAPI名を含めることでAPIを特定する。
また、リクエストの内容をstatus.jsonに書き込む。
response/{uuid}.jsonはAPPサーバが処理を終えた後に書き込まれ、APIサーバから非同期に読み込まれる。

コンテナ内では以下のように見える。
```
/shared/bcrlapi/
        request/
            {uuid}.json
            status.json
        response/
            {uuid}.json
```

データフローはsystem components.drawio.svgおよびsequence参照。

## APPサーバのcron
status.jsonに対して１分間隔で監視する。
status.jsonはAPPサーバの状態を示すjsonファイルで、以下のような内容を持つ。
```json
{
    "jobs": [
        {
            "uuid": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
            "api": "soc",
            "status": "pending",
            "request_date": "2023-10-01T00:00:00+09:00"
        },
        ...
    ]
}
```

statusのパラメータは以下のように定義する。
- pending: 処理待ち
- processing: 処理中
- done: 処理完了

cronからstatusパラメータを監視し、pendingのuuidを取得する。
からprocessingに変更されたらAPPサーバの処理を開始する。
statusのチェックは上から順に行い、pendingのuuidがあればそのuuidを使用する。

リクエストで増えていくデータはすべて1週間分残して、それ以上をデイリーで削除する。

# テスト用mock
テスト用にAPPサーバmockとクライアントmockを作成する。
詳細はmock.mdを参照。

# 検討過程
APIの実行頻度が低く、処理速度はそんなに必要ないので案3を採用。
## 案1：APPサーバをそのままAPIサーバ化する
研究室のメンバーでAPIサーバを実装する。APIサーバの改修でAPPサーバに影響が出やすい。APIサーバをスケールしにくい。
- 実装難易度：×
- 運用：×
- 処理速度：〇

## 案2：APIサーバは分離するが、APPサーバにもAPI実装する
APIサーバを独立させることでスケールしやすくなる。APPサーバにAPIを実装することのハードルが高そう。
- 実装難易度：△
- 運用：〇
- 処理速度：△

## 案3：APIサーバは分離し、APPサーバとのI/Fをファイルの入出力にする
I/Fをファイルの入出力にすることでAPPサーバ側の実装難易度を下げる。処理速度で劣る。
- 実装難易度：〇
- 運用：〇
- 処理速度：×

## APPサーバの仕様
1. APIがたたかれる頻度：5分に1回
2. 処理時間：1リクエストあたり数分
3. 並列処理したいリクエスト数：TBD
4. job履歴の件数：TBD

## APPサーバのcronの監視間隔
短すぎるとCPUを食いそうなので、とりあえず1分間隔で監視する。
性能に応じて変更する。

# APPサーバに実装してほしい部分
- cronでstatus.jsonを監視して、pendingのuuidを取得する
- uuidを取得したら、status.jsonのuuidのstatusをpendingからprocessingに変更する
- リクエストのデータを/shared/bcrlapi/request/{uuid}.jsonを読み込む
- main.pyを実行する
- main.pyの実行結果を/shared/bcrlapi/response/{uuid}.jsonに書き込む
- 処理が完了したらstatus.jsonのuuidのstatusをprocessingからdoneに変更する

# APIの非同期化
リクエストの応答に数分かかるため、APIを分割して非同期化する。
1. リクエストを出して、進捗状況を取得するAPI
2. 進捗状況を取得するAPI
3. 結果を取得するAPI

# status.jsonの更新時間
status.json をファイル全体として書き直す際の処理時間（ローカルでの実測）は以下の通り
| ジョブ件数  | 書き込み所要時間       |
| ------ | -------------- |
| 10     | 約 **0.0003 秒** |
| 100    | 約 **0.0027 秒** |
| 1,000  | 約 **0.022 秒**  |
| 5,000  | 約 **0.13 秒**   |
| 10,000 | 約 **0.23 秒**   |
| 20,000 | 約 **0.43 秒**   |


# TBD
## リクエストの管理方法
- リクエストIDをローカルの辞書で管理  
実装は楽だが、ローカルの容量を食うのでスケールができない。
リクエストは処理が終わるまで待たせて、レスポンスは処理結果を返す。
- backgroundタスク :star: 非同期をやるならこれがよさそう  
リクエストは即時応答してリクエストIDと処理状態のみ返却、処理結果は別のURIで取得させる。  
前提となる応答時間を踏まえるとこれがいい気がする。  
ユーザはレスポンスのデータをどう使うのか次第で、レスポンスの処理を自動化させたい人達にとっては使いにくくなる。  
結果を見たいだけならwebサーバで画面を作ってデータはそこからcsvなりJSONなりで出力してあげればいい気がする。  
APIとしてはrequestをjobkick用と結果取得用に分けて2回取得してもらうこともできる。  
- Queueを使う  
実装難易度が高い。管理が大変そう。
- DBを使う  
実装難易度が高い。管理が大変そう。