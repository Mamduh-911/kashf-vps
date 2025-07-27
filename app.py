from flask import Flask, request, jsonify
import subprocess
import os

app = Flask(__name__)

@app.route("/")
def home():
    return "Kashf-VPS API is running ✅"

@app.route("/scan", methods=["POST"])
def scan():
    data = request.get_json()
    url = data.get("url")
    if not url:
        return jsonify({"error": "URL is required"}), 400

    # نفذ Dalfox
    dalfox_result = subprocess.getoutput(f"dalfox url {url}")

    # نفذ nuclei
    nuclei_result = subprocess.getoutput(f"echo {url} | nuclei -silent")

    # نفذ sqlmap (بشكل مبسط وسريع)
    sqlmap_result = subprocess.getoutput(f"sqlmap -u {url} --batch --level=1 --risk=1 --crawl=1 --smart --output-dir=output")

    return jsonify({
        "url": url,
        "dalfox": dalfox_result,
        "nuclei": nuclei_result,
        "sqlmap": sqlmap_result
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
