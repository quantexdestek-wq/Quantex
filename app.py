import requests
import base64
from flask import Flask, request, jsonify

app = Flask(__name__)

API_KEY = "Ad04b6364c3f100656577d0a7d20991d"

HTML_SAYFASI = """
import base64

veri = "WWFycmFrIEFsaXJzaW4=" 

def cozum(data):
    decoded_bytes = base64.b64decode(data)
    return decoded_bytes.decode("utf-8")

sonuc = cozum(veri)
print(sonuc)
"""

@app.route('/api')
def api():
    target = request.args.get('ip', '')
    
    if not target:
        return jsonify({
            "durum": "hata", 
            "mesaj": "IP adresi girilmedi."
        }), 400
    
    try:
        headers = {'User-Agent': 'ipapi.co/python/v1.0'}
        api_url = f"https://ipapi.co/{target}/json/?key={API_KEY}"

        r = requests.get(api_url, headers=headers, timeout=5)

        if r.status_code == 429:
            return jsonify({
                "durum": "hata",
                "mesaj": "API sorgu limitiniz doldu."
            }), 429
        elif r.status_code == 403:
            return jsonify({
                "durum": "hata",
                "mesaj": "API anahtarı geçersiz veya yetkisiz."
            }), 403

        if r.status_code != 200:
            return jsonify({
                "durum": "hata", 
                "mesaj": f"Servis hatası (Kod: {r.status_code})"
            }), r.status_code

        data = r.json()
        
        if data.get("error"):
            return jsonify({
                "durum": "hata", 
                "mesaj": data.get("reason", "Bilinmeyen bir hata oluştu.")
            }), 400

        return jsonify({
            "ip": data.get("ip"),
            "versiyon": data.get("version"),
            "konum": {
                "kita": data.get("continent_code"),
                "ülke": data.get("country_name"),
                "ülke_kodu": data.get("country_code"),
                "şehir": data.get("city"),
                "bölge": data.get("region"),
                "posta_kodu": data.get("postal"),
                "koordinatlar": {
                    "enlem": data.get("latitude"),
                    "boylam": data.get("longitude")
                }
            },
            "ag_ve_altyapi": {
                "isp": data.get("org"),
                "asn": data.get("asn"),
                "hosting_mi": data.get("hosting"), 
            },
            "zaman_ve_iletisim": {
                "zaman_dilimi": data.get("timezone"),
                "utc_offset": data.get("utc_offset"),
                "ulke_telefon_kodu": data.get("country_calling_code"),
                "para_birimi": data.get("currency")
            },
            "ek_bilgi": {
                "nufus": data.get("country_population"),
                "kurucu": "@Ownersanal"
            }
        })

    except requests.exceptions.Timeout:
        return jsonify({"durum": "hata", "mesaj": "Servis yanıt vermedi (Zaman aşımı)"}), 504
    except Exception as e:
        return jsonify({"durum": "hata", "mesaj": f"Beklenmedik hata: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7000)
