FROM python:3.11-alpine AS builder

WORKDIR /usr/src/app

RUN apk add --no-cache build-base

COPY requirements.txt ./
RUN pip install --prefix=/install -r requirements.txt

FROM python:3.11-alpine

WORKDIR /usr/src/app

COPY --from=builder /install /usr/local

COPY . .

EXPOSE 5000
EXPOSE 8765 

CMD ["python", "main.py"]
