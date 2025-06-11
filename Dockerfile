FROM python:3.10-slim

WORKDIR /safevisionapp

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . /safevisionapp

EXPOSE 5000

CMD ["python", "main.py"]
