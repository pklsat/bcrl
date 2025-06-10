# 概要
battery control by reinforcement lerningをサブモジュールとしてWeb/APIサーバーを構築したリポジトリです。
https://github.com/SmartGridLab/battery-control-by-reinforcement-learning

このリポジトリではサブモジュール内の内容は変更しないでください。
サブモジュールは```git submodule update --remote```で更新してください。
サブモジュールを更新したら.gitフォルダ内の定義ファイルのサブモジュール参照先が変更されるので変更をコミットしてからpushしてください。
仕様はdocuments参照。

# 初回Clone
サブモジュールも含めてclone
```
git clone --recurse-submodules git@github.com:pklsat/bcrl.git
```

# build
## 開発環境
起動
```
docker-compose --profile dev up -d --build
```
停止
```
docker-compose --profile dev down -v
```
## テスト環境
起動
```
docker-compose --profile test up -d --build
```
停止
```
docker-compose --profile test down -v
```

## 本番環境
起動
```
docker-compose --profile production up -d --build
```
停止
```
docker-compose --profile production down -v
```

## サブモジュールの更新
すべてのリモートブランチを更新
```
git submodule update --remote
```

## サブモジュールの変更を取り消し
main.pyを実行した後にできるcsvなどを初期化したいとき
```
cd bcrl
git restore . 
sudo git clean -fd
git submodule update --init --recursive
```

## 現在参照しているサブモジュールのブランチ・コミットIDを確認
```
cd bcrlapi
git submodule status
```

## メモ
### 初回リポジトリ作成時に実施
```
mkdir bcrl
cd bcrl
git init
git submodule add git@github.com:SmartGridLab/battery-control-by-reinforcement-learning.git bcrlapp
git remote add origin git@github.com:pklsat/bcrl.git
git push -u origin main
```