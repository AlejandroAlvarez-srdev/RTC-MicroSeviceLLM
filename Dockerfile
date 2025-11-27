FROM python:3.11-bookworm

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update -y && \
    apt-get install -y --no-install-recommends \
        ffmpeg \
        libsndfile1 \
        ca-certificates || \
    (apt-get update -y --fix-missing && \
     apt-get install -y --no-install-recommends ffmpeg libsndfile1 ca-certificates) && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

# Instalar numpy primero
RUN pip install --no-cache-dir numpy==1.26.4

# Instalar lo demás
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app
COPY tests ./tests

ENV PORT=8080

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
