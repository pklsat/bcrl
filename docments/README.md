# 現状の仕様
## APIは同期処理
同期処理で動かしている。

## APPサーバとのI/F
I/Fとするファイル群はdockerのsharedボリューム内にまとめる。  
APIサーバから見るとrequest.jsonに書き込み、APPサーバのデータ更新後response.jsonを読み込む形になると嬉しい。  
構成図上ではCSVからデータを収集して読み込むことにしているが、どのデータを取得するのかなど、仕様に関するやり取りが複雑になりすぎる。

例えばAPIに応じてapiディレクトリを増やして、その中にrequest.jsonとresponse.jsonを格納していく。  
この辺りはいくらでも工夫の仕様があるのでTBD、watchdogのベストプラクティスにもよる。　　

コンテナ内では以下のように見える。
```
/shared/bcrlapi/
    json/
        apiA/
            request.json
            response.json
        apiB/
            request.json
            response.json
    flag/
        existRequest.txt
        apiName.tst
```

データフローははsystem components.drawio.svgおよびsequence参照。

## APPサーバに実装してほしい部分
### フラグ管理する場合
- watchdogでフラグファイル/shared/bcrlapi/flag/frag.txtを監視する
- フラグが更新されたらリクエストのデータを/shared/bcrlapi/json/request.jsonに読み込む
- もしくは必要なデータを集めて/shared/bcrlapi/json/response.jsonを作ってくれるとすごくうれしい。(２回目)
- 処理が完了したらフラグファイルを更新する0→1
### 内部向けのAPIサーバを作る場合
- APIサーバを建てて、json形式でRESTAPIを実装
- requestのデータの処理、response用のデータの取得、responseの作成など一通り実装する

# TBD
一覧
- そもそもAPIを提供する必要はあるのか
- 非同期処理どうするか

# そもそもAPIを提供する必要はあるのか
ユーザがAPIのレスポンスを使ってリアルタイムで自動化するしたいのであればAPI化する価値はある。  
一方で１日数回実行するだけで、結果は分析に使ったり、手動で何かにインプットしたいだけならwebサーバ上でGUIを作ってログインしてもらい、データのインプット・アウトプットはGUI上操作して計算結果をcsvなりJSONなりで出力してあげればいい気がする。  
研究用サーバの処理時間が15分程度と非常に長いときがあるので、APIとしての/リアルタイム性はそこまで必要ないのではないか？

## 非同期処理どうするか
sequenceで検討