FROM python:3.11-slim

# تثبيت الأدوات
RUN apt-get update && apt-get install -y curl git unzip
RUN git clone --depth=1 https://github.com/sqlmapproject/sqlmap.git /opt/sqlmap
RUN curl -L https://github.com/hahwul/dalfox/releases/download/v2.12.0/dalfox-linux-amd64.zip -o /tmp/dalfox.zip \
 && unzip /tmp/dalfox.zip -d /usr/local/bin && chmod +x /usr/local/bin/dalfox
RUN curl -s https://api.github.com/repos/projectdiscovery/nuclei/releases/latest \
 | grep linux_amd64.zip | cut -d '"' -f 4 | wget -i - -O nuclei.zip \
 && unzip nuclei.zip && mv nuclei /usr/local/bin/ && chmod +x /usr/local/bin/nuclei

# تثبيت Python dependencies
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py .

CMD ["gunicorn", "app:app", "--bind=0.0.0.0:8000"]
