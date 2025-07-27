FROM python:3.11-slim

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

# تثبيت الأدوات الخارجية
RUN apt-get update && apt-get install -y curl unzip git default-jdk build-essential

# Dalfox
RUN curl -L https://github.com/hahwul/dalfox/releases/download/v2.12.0/dalfox-linux-amd64.zip -o /tmp/dalfox.zip \
    && unzip /tmp/dalfox.zip -d /usr/local/bin \
    && chmod +x /usr/local/bin/dalfox

# nuclei
RUN curl -s https://api.github.com/repos/projectdiscovery/nuclei/releases/latest \
    | grep "browser_download_url.*linux_amd64.zip" \
    | cut -d '"' -f 4 \
    | wget -qi - -O nuclei.zip \
    && unzip nuclei.zip -d /usr/local/bin \
    && chmod +x /usr/local/bin/nuclei

# sqlmap
RUN git clone --depth 1 https://github.com/sqlmapproject/sqlmap.git /opt/sqlmap
ENV PATH="/opt/sqlmap:$PATH"

CMD ["python", "app.py"]
