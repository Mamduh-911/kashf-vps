FROM ubuntu:22.04

# تثبيت الأدوات اللازمة
RUN apt-get update && apt-get install -y curl unzip

# تحميل وتثبيت dalfox
RUN curl -L https://github.com/hahwul/dalfox/releases/download/v2.12.0/dalfox-linux-amd64.zip -o /tmp/dalfox.zip \
    && unzip /tmp/dalfox.zip -d /usr/local/bin \
    && chmod +x /usr/local/bin/dalfox
