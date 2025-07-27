from flask import Flask, request, jsonify, render_template
import subprocess
import uuid
import os

app = Flask(__name__, template_folder='templates', static_folder='static')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/scan', methods=['POST'])
def scan():
    data = request.get_json()
    target_url = data.get('url')
    if not target_url:
        return jsonify({'error': 'Missing URL'}), 400

    scan_id = str(uuid.uuid4())
    os.makedirs(f"scans/{scan_id}", exist_ok=True)

    results = []

    # SQLMAP
    try:
        sqlmap_cmd = [
            "sqlmap",
            "-u", target_url,
            "--batch",
            "--output-dir", f"scans/{scan_id}/sqlmap"
        ]
        subprocess.run(sqlmap_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=90)
        results.append({
            "tool": "SQLMap",
            "status": "✅ تم الفحص باستخدام SQL Injection",
            "severity": "عالية",
            "description": "تم تنفيذ فحص SQLi باستخدام أداة sqlmap."
        })
    except Exception as e:
        results.append({
            "tool": "SQLMap",
            "status": f"❌ خطأ: {str(e)}",
            "severity": "منخفضة",
            "description": "حدث خطأ أثناء تنفيذ sqlmap."
        })

    # NUCLEI
    try:
        nuclei_cmd = [
            "nuclei",
            "-u", target_url,
            "-o", f"scans/{scan_id}/nuclei.txt"
        ]
        subprocess.run(nuclei_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=60)
        with open(f"scans/{scan_id}/nuclei.txt", "r") as f:
            nuclei_output = f.read()

        if nuclei_output.strip():
            results.append({
                "tool": "Nuclei",
                "status": "✅ تم العثور على ثغرات",
                "severity": "متوسطة",
                "description": nuclei_output
            })
        else:
            results.append({
                "tool": "Nuclei",
                "status": "✅ لا توجد ثغرات معروفة",
                "severity": "معلوماتية",
                "description": "لم يتم العثور على نتائج من nuclei."
            })
    except Exception as e:
        results.append({
            "tool": "Nuclei",
            "status": f"❌ خطأ: {str(e)}",
            "severity": "منخفضة",
            "description": "حدث خطأ أثناء تنفيذ nuclei."
        })

    return jsonify({"results": results})
