FROM python:3.11-bookworm

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=8000

WORKDIR /app

# Dependencias del sistema
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        ffmpeg \
        libsndfile1 \
    && rm -rf /var/lib/apt/lists/*

# Dependencias Python
COPY requirements.txt /app/

RUN python -m pip install --upgrade pip && \
    pip install --no-cache-dir "torch==2.2.2+cpu" --index-url https://download.pytorch.org/whl/cpu && \
    pip install --no-cache-dir -r requirements.txt --no-deps



# Código de la app
COPY app /app/app
COPY tests /app/tests

EXPOSE 8000

CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT}"]
