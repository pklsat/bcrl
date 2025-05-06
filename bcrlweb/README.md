# 概要
react + vite + nginxのwebアプリケーション

# ビルド
```bash
cd bcrapi
# 起動
docker-compose --profile production up -d --build
# 停止
docker-compose --profile production down
```

# アクセス
- ジョブ一覧画面
http://localhost:4002/

# 参考
- [Vite](https://ja.vitejs.dev/)
- [React](https://ja.reactjs.org/)

