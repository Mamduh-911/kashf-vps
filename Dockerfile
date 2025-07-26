# استخدم صورة ألباين خفيفة
FROM alpine:latest

# تثبيت curl فقط لأنه مطلوب للتحميل
RUN apk add --no-cache curl

# تحميل ملف dalfox التنفيذي ووضعه في /usr/local/bin مع صلاحية التنفيذ
RUN curl -L https://github.com/hahwul/dalfox/releases/download/v2.12.0/dalfox-linux-amd64 -o /usr/local/bin/dalfox && \
    chmod +x /usr/local/bin/dalfox

# يمكنك هنا تحديد نقطة البداية (اختياري)
ENTRYPOINT ["/usr/local/bin/dalfox"]
