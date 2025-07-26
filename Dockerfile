docker run -it ubuntu:22.04 bash
apt-get update && apt-get install -y curl unzip
curl -L https://github.com/hahwul/dalfox/releases/download/v2.12.0/dalfox-linux-amd64.zip -o /tmp/dalfox.zip
unzip /tmp/dalfox.zip -d /usr/local/bin
chmod +x /usr/local/bin/dalfox
