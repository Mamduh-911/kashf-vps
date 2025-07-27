from flask import Flask, request, jsonify
import subprocess
import uuid
import os

app = Flask(__name__)

@app.route('/scan', methods=['POST'])
def scan():
    data = request.get_json()
    target_url = data.get('url')
    if not target_url:
        return jsonify({'error': 'Missing URL'}), 400

    scan_id = str(uuid.uuid4())
    os.makedirs(f"scans/{scan_id}", exist_ok=True)

    results = []

    # Run sqlmap
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
            "status": "✅ فحص SQL Injection تم",
            "severity": "High",
            "description": "فحص تلقائي لثغرات SQLi باستخدام sqlmap"
        })
    except Exception as e:
        results.append({
            "tool": "SQLMap",
            "status": f"❌ خطأ: {str(e)}",
            "severity": "Low",
            "description": "لم يتم الفحص بـ sqlmap"
        })

    # Run nuclei
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
                "severity": "Medium",
                "description": nuclei_output
            })
        else:
            results.append({
                "tool": "Nuclei",
                "status": "✅ تم الفحص، لا توجد ثغرات",
                "severity": "Info",
                "description": "لم يتم اكتشاف أي ثغرات معروفة"
            })
    except Exception as e:
        results.append({
            "tool": "Nuclei",
            "status": f"❌ خطأ: {str(e)}",
            "severity": "Low",
            "description": "لم يتم الفحص بـ nuclei"
        })

    return jsonify({"results": results})
