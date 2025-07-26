FROM alpine:latest

RUN apk add --no-cache curl

RUN curl -L https://github.com/hahwul/dalfox/releases/download/v2.12.0/dalfox-linux-amd64 -o /usr/local/bin/dalfox && chmod +x /usr/local/bin/dalfox

ENTRYPOINT ["/usr/local/bin/dalfox"]
