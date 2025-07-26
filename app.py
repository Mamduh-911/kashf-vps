from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

@app.route('/')
def index():
    return "🚀 Kashf-VPS API is running!"

@app.route('/scan/xss', methods=['POST'])
def scan_xss():
    target = request.json.get('url')
    if not target:
        return jsonify({"error": "URL is required"}), 400
    try:
        result = subprocess.check_output(['dalfox', 'url', target], stderr=subprocess.STDOUT)
        return jsonify({"tool": "dalfox", "output": result.decode()}), 200
    except subprocess.CalledProcessError as e:
        return jsonify({"error": e.output.decode()}), 500

@app.route('/scan/sql', methods=['POST'])
def scan_sql():
    target = request.json.get('url')
    if not target:
        return jsonify({"error": "URL is required"}), 400
    try:
        result = subprocess.check_output(['sqlmap', '-u', target, '--batch', '--level=1'], stderr=subprocess.STDOUT)
        return jsonify({"tool": "sqlmap", "output": result.decode(errors='ignore')}), 200
    except subprocess.CalledProcessError as e:
        return jsonify({"error": e.output.decode(errors='ignore')}), 500

@app.route('/scan/lfi', methods=['POST'])
def scan_lfi():
    target = request.json.get('url')
    if not target:
        return jsonify({"error": "URL is required"}), 400
    try:
        result = subprocess.check_output(['nuclei', '-u', target, '-t', 'vulnerabilities/'], stderr=subprocess.STDOUT)
        return jsonify({"tool": "nuclei", "output": result.decode(errors='ignore')}), 200
    except subprocess.CalledProcessError as e:
        return jsonify({"error": e.output.decode(errors='ignore')}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
