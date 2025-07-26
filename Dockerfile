FROM golang:1.21-alpine as builder

# تثبيت المتطلبات
RUN apk add --no-cache git curl unzip

# تحميل مصدر dalfox وتجميعه
RUN git clone https://github.com/hahwul/dalfox.git /go/src/dalfox && \
    cd /go/src/dalfox && \
    go build -o dalfox

# مرحلة التشغيل
FROM python:3.10-slim

# تثبيت الأدوات الأساسية
RUN apt-get update && apt-get install -y \
    curl unzip git gcc build-essential \
    default-libmysqlclient-dev libssl-dev libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# نسخ dalfox من مرحلة التجميع
COPY --from=builder /go/src/dalfox/dalfox /usr/local/bin/dalfox

# تثبيت nuclei
RUN curl -s https://api.github.com/repos/projectdiscovery/nuclei/releases/latest \
    | grep "browser_download_url.*linux_amd64.zip" \
    | cut -d '"' -f 4 \
    | wget -i - -O nuclei.zip && \
    unzip nuclei.zip && mv nuclei /usr/local/bin/ && chmod +x /usr/local/bin/nuclei

# تثبيت sqlmap
RUN git clone --depth 1 https://github.com/sqlmapproject/sqlmap.git /opt/sqlmap

# إنشاء مجلد التطبيق
WORKDIR /app
COPY . /app

# تثبيت Flask
RUN pip install flask

# إعداد sqlmap في PATH
ENV PATH="/opt/sqlmap:$PATH"

# تشغيل التطبيق
CMD ["python", "app.py"]
