from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)
acessos = []

@app.route('/')
def redirecionar():
    return render_template('mapa.html')

@app.route('/registrar', methods=['POST'])
def registrar_gps():
    data = request.get_json()
    ip = request.headers.get('X-Forwarded-For', request.remote_addr).split(',')[0].strip()

    try:
        geo_info = requests.get(f"http://ipinfo.io/{ip}/json").json()
        city = geo_info.get('city', 'Desconhecida')
        region = geo_info.get('region', 'Desconhecida')
        country = geo_info.get('country', 'Desconhecido')
    except Exception:
        city = region = country = 'Desconhecido'

    acessos.append({
        'ip': ip,
        'lat': data.get('lat'),
        'lon': data.get('lon'),
        'city': city,
        'region': region,
        'country': country
    })

    return jsonify({"status": "registrado"})

@app.route('/acessos')
def listar_acessos():
    return jsonify(acessos)

if __name__ == '__main__':
    app.run(debug=True, port=5002)
