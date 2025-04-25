from flask import Flask, request, render_template, jsonify
import datetime
import requests

app = Flask(__name__)

acessos = []

# Função para obter cidade, região e país a partir da latitude e longitude
def obter_localizacao_por_lat_lon(latitude, longitude):
    try:
        url = f"https://nominatim.openstreetmap.org/reverse?format=jsonv2&lat={latitude}&lon={longitude}"
        headers = {"User-Agent": "GeoApp/1.0"}
        resposta = requests.get(url, headers=headers)
        dados = resposta.json()

        cidade = dados.get("address", {}).get("city") or \
                 dados.get("address", {}).get("town") or \
                 dados.get("address", {}).get("village") or ""

        regiao = dados.get("address", {}).get("state", "")
        pais = dados.get("address", {}).get("country", "")

        return cidade, regiao, pais
    except Exception as e:
        print(f"[ERRO] Falha ao obter localização reversa: {e}")
        return "", "", ""

@app.route('/')  # Esta será a rota visitada via QR Code
def coletar():
    return render_template('coleta.html')  # Agora renderiza a coleta!

@app.route('/registrar', methods=['POST'])
def registrar():
    data = request.get_json()
    ip = request.headers.get('X-Forwarded-For', request.remote_addr).split(',')[0].strip()
    lat = data.get('lat')
    lon = data.get('lon')
    precisa = data.get('precisa', False)

    # Consulta a localização somente se não veio no corpo da requisição
    city, region, country = data.get('city'), data.get('region'), data.get('country')
    if not (city and region and country) and lat and lon:
        city, region, country = obter_localizacao_por_lat_lon(lat, lon)

    acesso = {
        'ip': ip,
        'lat': lat,
        'lon': lon,
        'precisa': precisa,
        'city': city,
        'region': region,
        'country': country,
        'timestamp': datetime.datetime.now().isoformat()
    }
    acessos.append(acesso)
    return jsonify({'status': 'ok'})

@app.route('/mapa')
def mapa():
    return render_template('mapa.html', acessos=acessos)

@app.route('/acessos')
def listar_acessos():
    return render_template('acessos.html', acessos=acessos)

if __name__ == '__main__':
    app.run(debug=True)
