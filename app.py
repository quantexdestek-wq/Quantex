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
        return "Hata: IP adresi girilmedi."
    
    try:
        fields = "status,message,country,countryCode,regionName,city,zip,lat,lon,timezone,isp,org,as,query,reverse,proxy"
        r = requests.get(f"http://ip-api.com/json/{target}?fields={fields}", timeout=5)
        data = r.json()
        
        if data.get("status") == "success":
            return (
                f"Sorgu: {data.get('query')}\n"
                f"Ters DNS: {data.get('reverse', 'Yok')}\n"
                f"Ülke: {data.get('country')} ({data.get('countryCode')})\n"
                f"Bölge/Şehir: {data.get('regionName')} / {data.get('city')}\n"
                f"Posta Kodu: {data.get('zip')}\n"
                f"Koordinat: {data.get('lat')}, {data.get('lon')}\n"
                f"Saat Dilimi: {data.get('timezone')}\n"
                f"ISP: {data.get('isp')}\n"
                f"Organizasyon: {data.get('org')}\n"
                f"AS Bilgisi: {data.get('as')}\n"
                f"Proxy/VPN: {'Evet' if data.get('proxy') else 'Hayır'}"
            )
        return f"Hata: {data.get('message', 'Geçersiz IP')}"
    except Exception as e:
        return f"Bağlantı hatası oluştu!"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7000)