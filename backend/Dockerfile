# 1️⃣ Python の公式イメージを使用
FROM python:3.9-slim

# 2️⃣ 必要なパッケージをインストール（mysqlclient のビルドに必要）
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    build-essential \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# 3️⃣ 作業ディレクトリを指定
WORKDIR /emory

# 4️⃣ `requirements.txt` をコピー
COPY backend/requirements.txt ./backend/

# 5️⃣ 依存関係をインストール
RUN pip install --no-cache-dir -r backend/requirements.txt

# 6️⃣ ソースコードをコピー
COPY . .

# 7️⃣ Flask の起動コマンドを設定
CMD ["sh", "-c", "sleep 5 && python backend/run.py"]
