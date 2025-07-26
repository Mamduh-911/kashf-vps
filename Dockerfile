# استخدام صورة أوبنتو حديثة
FROM ubuntu:22.04

# تثبيت الأدوات الضرورية
RUN apt-get update && apt-get install -y curl unzip

# تحميل وتثبيت dalfox
RUN curl -L https://github.com/hahwul/dalfox/releases/download/v2.9.0/dalfox_2.9.0_linux_amd64.tar.gz -o /tmp/dalfox.tar.gz \
    && tar -xzf /tmp/dalfox.tar.gz -C /usr/local/bin \
    && chmod +x /usr/local/bin/dalfox \
    && rm /tmp/dalfox.tar.gz

# تحقق من تثبيت dalfox
RUN dalfox --version

# تعيين الأمر الافتراضي
ENTRYPOINT ["dalfox"]
CMD ["--help"]
