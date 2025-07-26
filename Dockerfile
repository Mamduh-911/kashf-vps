FROM python:3.10-slim

RUN apt-get update && apt-get install -y curl unzip git

# تثبيت Dalfox
RUN curl -L https://github.com/hahwul/dalfox/releases/download/v2.12.0/dalfox-linux-amd64 -o /usr/local/bin/dalfox && \
    chmod +x /usr/local/bin/dalfox

# نسخ السكربت وتشغيله
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt

CMD ["python", "app.py"]
