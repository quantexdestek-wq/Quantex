from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)

# Senin yazdığın harika arayüz tasarımı (Sadece JS fetch URL'si uyarlandı)
HTML_SAYFASI = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Siber IP Sorgu Paneli</title>
    <style>
        :root {
            --primary: #00d2ff;
            --secondary: #3a7bd5;
            --bg: #0f172a;
            --card: #1e293b;
            --text: #f8fafc;
        }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, var(--bg), #1e1b4b);
            color: var(--text);
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            overflow: hidden;
        }
        .container {
            background: var(--card);
            padding: 2.5rem;
            border-radius: 20px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
            width: 100%;
            max-width: 450px;
            text-align: center;
            border: 1px solid rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
        }
        h2 {
            margin-bottom: 1.5rem;
            font-weight: 600;
            background: linear-gradient(to right, var(--primary), var(--secondary));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .input-group {
            position: relative;
            margin-bottom: 1.5rem;
        }
        input {
            width: 80%;
            padding: 12px 20px;
            border-radius: 12px;
            border: 2px solid #334155;
            background: #0f172a;
            color: white;
            font-size: 1rem;
            transition: all 0.3s ease;
            outline: none;
        }
        input:focus {
            border-color: var(--primary);
            box-shadow: 0 0 15px rgba(0, 210, 255, 0.3);
        }
        button {
            width: 100%;
            padding: 12px;
            border-radius: 12px;
            border: none;
            background: linear-gradient(45deg, var(--primary), var(--secondary));
            color: white;
            font-weight: bold;
            font-size: 1rem;
            cursor: pointer;
            transition: transform 0.2s, box-shadow 0.2s;
        }
        button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 20px rgba(0, 210, 255, 0.4);
        }
        button:active {
            transform: translateY(0);
        }
        #resultBox {
            margin-top: 2rem;
            padding: 15px;
            background: rgba(15, 23, 42, 0.6);
            border-radius: 12px;
            border-left: 4px solid var(--primary);
            min-height: 50px;
            display: none;
            text-align: left;
            font-family: 'Courier New', Courier, monospace;
            word-break: break-all;
            line-height: 1.5;
        }
        .loader {
            display: none;
            margin: 10px auto;
            border: 3px solid #f3f3f3;
            border-top: 3px solid var(--primary);
            border-radius: 50%;
            width: 20px;
            height: 20px;
            animation: spin 1s linear infinite;
        }
        @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
    </style>
</head>
<body>

<div class="container">
    <h2>IP Sorgu İstasyonu</h2>
    <div class="input-group">
        <input type="text" id="ipAddress" placeholder="IP Adresi Girin (Örn: 8.8.8.8)">
    </div>
    <button onclick="performLookup()">Sorgula</button>
    <div class="loader" id="loader"></div>
    <div id="resultBox"></div>
</div>

<script>
    async function performLookup() {
        const ip = document.getElementById('ipAddress').value;
        const resultBox = document.getElementById('resultBox');
        const loader = document.getElementById('loader');

        if (!ip) {
            alert("Lütfen bir IP adresi girin!");
            return;
        }

        resultBox.style.display = "none";
        loader.style.display = "block";

        try {
            // Artık kendi Python sunucumuzdaki /sorgula endpoint'ine istek atıyoruz
            const response = await fetch(`/sorgula?ip=${encodeURIComponent(ip)}`);
            const data = await response.text();

            loader.style.display = "none";
            resultBox.style.display = "block";
            resultBox.innerText = data;
        } catch (error) {
            loader.style.display = "none";
            resultBox.style.display = "block";
            resultBox.innerText = "Hata: Sunucuya ulaşılamadı!";
        }
    }
</script>
</body>
</html>
"""

# Ana sayfaya girildiğinde HTML'i göster
@app.route('/')
def index():
    return render_template_string(HTML_SAYFASI)

# Butona basıldığında IP sorgusunu yapıp sonucu döndür
@app.route('/sorgula')
def sorgula():
    hedef_ip = request.args.get('ip', '')
    if not hedef_ip:
        return "Hata: IP adresi boş!"
    
    try:
        url = f"http://ip-api.com/json/{hedef_ip}"
        response = requests.get(url, timeout=5)
        data = response.json()

        if data.get("status") == "success":
            sonuc = (
                f"IP Adresi : {data.get('query')}\n"
                f"Ülke      : {data.get('country')}\n"
                f"Şehir     : {data.get('city')}\n"
                f"Bölge     : {data.get('regionName')}\n"
                f"ISP       : {data.get('isp')}\n"
                f"Kurum     : {data.get('org', 'Bilinmiyor')}"
            )
            return sonuc
        else:
            return f"Hata: {data.get('message', 'Geçersiz IP veya sorgu hatası.')}"

    except requests.exceptions.RequestException:
        return "Hata: API'ye ulaşılamadı."
    except Exception:
        return "Hata: Beklenmeyen bir hata oluştu."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
