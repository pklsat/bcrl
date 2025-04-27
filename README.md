# 概要
battery control by reinforcement lerningをサブモジュールとしてWeb/APIサーバーを構築したリポジトリです。
https://github.com/SmartGridLab/battery-control-by-reinforcement-learning

このリポジトリではサブモジュール内の内容は変更しないでください。
サブモジュールは```git submodule update --remote```で更新してください。
サブモジュールを更新したら.gitフォルダ内の定義ファイルのサブモジュール参照先が変更されるので変更をコミットしてからpushしてください。

# build～pushまで
./build_docker.sh

## 初回Clone
```
# サブモジュールも含めてclone
git clone --recurse-submodules git@github.com:pklsat/bcrlapi.git
```

## サブモジュールの更新
```
# すべてのブランチを更新
git submodule update --remote
```

## サブモジュールの変更を取り消し
main.pyを実行した後にできるcsvなどを初期化したいときに
```
# Untracked filesを削除する
sudo git clean -fd
```

## 現在参照しているサブモジュールのブランチ・コミットIDを確認
```
cd bcrlapi
git submodule status
```

## メモ
### 初回リポジトリ作成時に実施
```
git clone git@github.com:pklsat/bcrlapi.git
git submodule add git@github.com:SmartGridLab/battery-control-by-reinforcement-learning.git bcrl
```