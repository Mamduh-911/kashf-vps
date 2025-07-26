FROM python:3.10-slim

# تثبيت الأدوات الأساسية
RUN apt-get update && apt-get install -y \
    curl unzip git gcc build-essential \
    default-libmysqlclient-dev libssl-dev libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# تثبيت dalfox
# تثبيت dalfox تلقائياً من GitHub
RUN curl -s https://api.github.com/repos/hahwul/dalfox/releases/latest \
    | grep "browser_download_url.*linux-amd64.zip" \
    | cut -d '"' -f 4 \
    | wget -i - -O /tmp/dalfox.zip && \
    unzip /tmp/dalfox.zip -d /usr/local/bin && \
    chmod +x /usr/local/bin/dalfox*

# تثبيت nuclei
RUN curl -s https://api.github.com/repos/projectdiscovery/nuclei/releases/latest | \
    grep "browser_download_url.*linux_amd64.zip" | cut -d '"' -f 4 | wget -i - -O nuclei.zip && \
    unzip nuclei.zip && mv nuclei /usr/local/bin/ && chmod +x /usr/local/bin/nuclei

# تثبيت sqlmap
RUN git clone --depth 1 https://github.com/sqlmapproject/sqlmap.git /opt/sqlmap

# نسخ الملفات
WORKDIR /app
COPY . /app

# تثبيت Flask
RUN pip install flask

# إعداد alias لـ sqlmap
ENV PATH="/opt/sqlmap:$PATH"

# تشغيل التطبيق
CMD ["python", "app.py"]
