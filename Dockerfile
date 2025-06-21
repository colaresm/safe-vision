FROM python:3.11 AS builder

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --prefix=/install --no-cache-dir -r requirements.txt

FROM python:3.11-slim AS runtime

WORKDIR /app

RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

COPY --from=builder /install /usr/local

COPY . .

EXPOSE 5000

CMD ["python", "main.py"]
