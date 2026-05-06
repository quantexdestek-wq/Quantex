import requests
from flask import Flask, request, make_response

app = Flask(__name__)

HTML_SAYFASI = """
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
        return jsonify({"hata": "IP adresi girilmedi."}), 400
    
    try:
        r = requests.get(f"https://ipapi.co/{target}/json/", timeout=5)
        data = r.json()
        
        if data.get("error"):
            return jsonify({
                "durum": "hata",
                "mesaj": data.get("reason", "Geçersiz IP veya istek sınırı aşıldı.")
            }), 400

        return jsonify({
            "ip": data.get("ip"),
            "versiyon": data.get("version"),
            "konum": {
                "ülke": data.get("country_name"),
                "ülke_kodu": data.get("country_code"),
                "şehir": data.get("city"),
                "bölge": data.get("region"),
                "posta_kodu": data.get("postal"),
                "koordinat": {
                    "enlem": data.get("latitude"),
                    "boylam": data.get("longitude")
                }
            },
            "ag_bilgisi": {
                "asn": data.get("asn"),
                "isp": data.get("org")
            },
            "ekstra": {
                "para_birimi": data.get("currency"),
                "arama_kodu": data.get("country_calling_code"),
                "diller": data.get("languages"),
                "utc_offset": data.get("utc_offset")
            }
        })
    except Exception as e:
        return jsonify({"hata": "Bağlantı hatası!", "detay": str(e)}), 500     


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7000)
