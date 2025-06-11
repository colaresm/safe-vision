FROM python:3.10-slim

RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY stream_simulator/stream_simulator.py /app/


COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8081

CMD ["python", "stream_simulator.py"]
