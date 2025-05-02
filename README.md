# 概要
battery control by reinforcement lerningをサブモジュールとしてWeb/APIサーバーを構築したリポジトリです。
https://github.com/SmartGridLab/battery-control-by-reinforcement-learning

このリポジトリではサブモジュール内の内容は変更しないでください。
サブモジュールは```git submodule update --remote```で更新してください。
サブモジュールを更新したら.gitフォルダ内の定義ファイルのサブモジュール参照先が変更されるので変更をコミットしてからpushしてください。
仕様はdocuments参照。

# 初回Clone
```
# サブモジュールも含めてclone
git clone --recurse-submodules git@github.com:pklsat/bcrlapi.git
```

# build
```
# テスト用ビルド
docker-compose --profile mock up -d
# コンテナの停止
docker-compose --profile mock stop
# コンテナとボリュームの削除
docker-compose --profile mock down -v

#　本番環境用ビルド
docker-compose --profile production up -d
# コンテナの停止
docker-compose --profile mock stop
# コンテナとボリュームの削除
docker-compose --profile production down -v

# イメージのリビルド
docker-compose build  
```

## サブモジュールの更新
```
# すべてのリモートブランチを更新
git submodule update --remote
```

## サブモジュールの変更を取り消し
main.pyを実行した後にできるcsvなどを初期化したいときに
```
# サブモジュールの変更を取り消す
cd bcrl
git restore . 
# Untracked filesを削除する
sudo git clean -fd

# .gitmoduleで指定されたバージョンに戻す
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
mkdir bcrlapi
cd bcrlapi
git init
git submodule add git@github.com:SmartGridLab/battery-control-by-reinforcement-learning.git bcrl
git remote add origin git@github.com:pklsat/bcrlapi.git
git push -u origin main