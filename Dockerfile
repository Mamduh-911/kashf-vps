FROM golang:1.20-alpine

RUN apk add --no-cache git curl

RUN go install github.com/hahwul/dalfox/v2@latest

ENV PATH="/go/bin:${PATH}"

ENTRYPOINT ["dalfox"]
