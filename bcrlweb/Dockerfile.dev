# 開発用イメージ
FROM node:20

# 作業ディレクトリ
WORKDIR /app

# 依存関係を先にコピーしてインストール
COPY ./app/package*.json ./
RUN npm install

# 残りのファイルをコピー
COPY ./app .

# ポート指定（Viteデフォルト開発ポートは5273）
EXPOSE 5173

# Vite開発サーバを起動
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0", "--port", "5173"]