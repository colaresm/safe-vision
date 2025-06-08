# Etapa 1: imagem com OpenCV + GoCV
FROM gocv/opencv:4.9.0 AS builder

WORKDIR /goapp
COPY stream-simulator/ /goapp
RUN go build -o simulator main.go

# Etapa 2: Rodar Python + binário Go
FROM python:3.12.0-slim

WORKDIR /app

# Copiar o binário Go compilado
COPY --from=builder /goapp/simulator /app/stream-simulator

# Copiar os arquivos Python
COPY main.py requirements.txt /app/
COPY templates/ /app/templates/
COPY models/ /app/models/

# Instalar dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Expõe porta da aplicação (ajuste se necessário)
EXPOSE 5000

# Executa Go em background e Python em primeiro plano
CMD ["sh", "-c", "./stream-simulator & python main.py"]
