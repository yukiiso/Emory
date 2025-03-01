# frontend/Dockerfile

# 使用するベースイメージ
FROM node:16

# 作業ディレクトリを指定
WORKDIR /app

# 必要なパッケージをインストール
COPY package*.json ./
RUN npm install

# アプリケーションのソースコードをコピー
COPY . .

# React アプリケーションをビルド
RUN npm run build
