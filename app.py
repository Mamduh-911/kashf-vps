from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

@app.route('/scan')
def scan():
    url = request.args.get('url')
    if not url:
        return jsonify({"error": "Missing 'url' param"}), 400
    results = []

    # Dalfox
    try:
        out = subprocess.check_output(["dalfox", "url", url, "--silent", "--json"], stderr=subprocess.STDOUT, timeout=60)
        results.append({"tool": "dalfox", "result": out.decode()})
    except Exception as e:
        results.append({"tool": "dalfox", "error": str(e)})

    # SQLMap
    try:
        out = subprocess.check_output(["python3", "/opt/sqlmap/sqlmap.py", "-u", url, "--batch", "--output-dir=/tmp"], stderr=subprocess.STDOUT, timeout=120)
        results.append({"tool": "sqlmap", "result": out.decode()[:1000]})
    except Exception as e:
        results.append({"tool": "sqlmap", "error": str(e)})

    # Nuclei
    try:
        out = subprocess.check_output(["nuclei", "-u", url, "-json"], stderr=subprocess.STDOUT, timeout=60)
        results.append({"tool": "nuclei", "result": out.decode()})
    except Exception as e:
        results.append({"tool": "nuclei", "error": str(e)})

    return jsonify({"target": url, "scans": results})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000)
