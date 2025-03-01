# 1️⃣ Python の公式イメージを使用
FROM python:3.9-slim

# 2️⃣ 必要なパッケージをインストール
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# 3️⃣ 作業ディレクトリをプロジェクトルート (`emory/`) に設定
WORKDIR /emory  

# 4️⃣ `requirements.txt` をコピー
COPY backend/requirements.txt backend/  

# 5️⃣ 依存関係をインストール
RUN pip install --no-cache-dir -r backend/requirements.txt

# 6️⃣ プロジェクト全体をコピー
COPY . .  

# 7️⃣ Flask を起動
CMD ["python", "backend/run.py"]
