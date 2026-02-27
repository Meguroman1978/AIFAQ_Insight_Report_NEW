FROM python:3.11-slim

WORKDIR /app

# システム依存関係のインストール
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Pythonパッケージのインストール
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# バックエンドコードをコピー
COPY backend/ ./backend/

# フロントエンドをコピー
COPY frontend/ ./frontend/

# 一時ディレクトリ作成
RUN mkdir -p /tmp/aifaq_uploads /tmp/aifaq_reports

# 非rootユーザーで実行
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app /tmp/aifaq_uploads /tmp/aifaq_reports
USER appuser

WORKDIR /app/backend

# ポート設定
EXPOSE 8000

# アプリケーション起動
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
