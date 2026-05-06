import requests
from flask import Flask, request, make_response

app = Flask(__name__)

HTML_SAYFASI = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Siber IP Sorgu</title>
    <style>
        body { background: #0f172a; color: white; font-family: sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
        .box { background: #1e293b; padding: 2rem; border-radius: 15px; text-align: center; border: 1px solid #334155; }
        input { padding: 10px; border-radius: 5px; border: none; width: 200px; outline: none; }
        button { padding: 10px 20px; background: #00d2ff; border: none; border-radius: 5px; cursor: pointer; font-weight: bold; margin-left: 5px; }
        #res { margin-top: 20px; text-align: left; white-space: pre-wrap; font-family: monospace; color: #00d2ff; min-height: 50px; }
    </style>
</head>
<body>
    <div class="box">
        <h2>IP Sorgu İstasyonu</h2>
        <input type="text" id="ip" placeholder="8.8.8.8">
        <button onclick="sorgu()">Sorgula</button>
        <div id="res"></div>
    </div>
    <script>
        async function sorgu() {
            const ip = document.getElementById('ip').value;
            const res = document.getElementById('res');
            if(!ip) return;
            res.innerText = "Sorgulanıyor...";
            try {
                const response = await fetch('/api?ip=' + encodeURIComponent(ip));
                const data = await response.text();
                res.innerText = data;
            } catch (e) {
                res.innerText = "Hata oluştu!";
            }
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    response = make_response(HTML_SAYFASI)
    response.headers['Content-Type'] = 'text/html; charset=utf-8'
    return response

@app.route('/api')
def api():
    target = request.args.get('ip', '')
    if not target:
        return "IP adresi girilmedi."
    try:
        r = requests.get(f"http://ip-api.com/json/{target}", timeout=5)
        data = r.json()
        if data.get("status") == "success":
            return f"IP: {data.get('query')}\nÜlke: {data.get('country')}\nŞehir: {data.get('city')}\nISP: {data.get('isp')}"
        return "Hata: Geçersiz IP"
    except:
        return "Bağlantı hatası!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
