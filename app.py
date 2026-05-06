import requests
import base64
from flask import Flask, request, jsonify

app = Flask(__name__)

API_KEY = "ad04b6364c3f100656577d0a7d20991d"

HTML_SAYFASI = """"""

@app.route('/api')
def api():
    target = request.args.get('ip', '')
    
    if not target:
        return jsonify({
            "durum": "hata", 
            "mesaj": "IP adresi girilmedi."
        }), 400
    
    try:
        api_url = f"http://api.ipapi.com/{target}?access_key={API_KEY}"
        r = requests.get(api_url, timeout=5)

        if r.status_code != 200:
            return jsonify({
                "durum": "hata", 
                "mesaj": f"Servis hatası (Kod: {r.status_code})"
            }), r.status_code

        data = r.json()
        
        if "error" in data:
            return jsonify({
                "durum": "hata", 
                "mesaj": data["error"].get("info", "API Hatası")
            }), 400

        return jsonify({
            "ip": data.get("ip"),
            "type": data.get("type"),
            "continent_code": data.get("continent_code"),
            "continent_name": data.get("continent_name"),
            "country_code": data.get("country_code"),
            "country_name": data.get("country_name"),
            "region_code": data.get("region_code"),
            "region_name": data.get("region_name"),
            "city": data.get("city"),
            "zip": data.get("zip"),
            "latitude": data.get("latitude"),
            "longitude": data.get("longitude"),
            "msa": data.get("msa"),
            "dma": data.get("dma"),
            "radius": data.get("radius"),
            "ip_routing_type": data.get("ip_routing_type"),
            "connection_type": data.get("connection_type"),
            "hostname": data.get("hostname"),
            "location": data.get("location"),
            "time_zone": data.get("time_zone"),
            "currency": data.get("currency"),
            "connection": data.get("connection"),
            "security": data.get("security"),
            "Kurucu": "@OwnerSanal"
        })

    except requests.exceptions.Timeout:
        return jsonify({"durum": "hata", "mesaj": "Servis zaman aşımına uğradı"}), 504
    except Exception as e:
        return jsonify({"durum": "hata", "mesaj": f"Sistem hatası: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7000)