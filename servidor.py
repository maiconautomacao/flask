from flask import Flask, request, render_template, jsonify
import datetime
import requests

app = Flask(__name__)

# Lista para armazenar os acessos - Maicon Ferreira
acessos = []

# Função para obter cidade, região e país a partir da latitude e longitude - Maicon Ferreira
def obter_localizacao_por_lat_lon(latitude, longitude):
    try:
        url = f"https://nominatim.openstreetmap.org/reverse?format=jsonv2&lat={latitude}&lon={longitude}"
        headers = {"User-Agent": "GeoApp/1.0"}
        resposta = requests.get(url, headers=headers)
        dados = resposta.json()

        # Tentativa de extrair cidade de diferentes campos - Maicon Ferreira
        cidade = dados.get("address", {}).get("city") or \
                 dados.get("address", {}).get("town") or \
                 dados.get("address", {}).get("village") or ""

        regiao = dados.get("address", {}).get("state", "")
        pais = dados.get("address", {}).get("country", "")

        return cidade, regiao, pais
    except Exception as e:
        print(f"[ERRO] Falha ao obter localização reversa: {e}") 
        return "", "", ""

# Rota principal, visitada pelo QR Code - Maicon Ferreira
@app.route('/')
def coletar():
    return render_template('coleta.html')  # Página de coleta de localização - Maicon Ferreira

# Rota que registra o acesso com IP, localização e horário - Maicon Ferreira
@app.route('/registrar', methods=['POST'])
def registrar():
    data = request.get_json()
    ip = request.headers.get('X-Forwarded-For', request.remote_addr).split(',')[0].strip()
    lat = data.get('lat')
    lon = data.get('lon')
    precisa = data.get('precisa', False)

    # Se cidade, região e país não foram enviados, tenta obter via coordenadas - Maicon Ferreira
    city, region, country = data.get('city'), data.get('region'), data.get('country')
    if not (city and region and country) and lat and lon:
        city, region, country = obter_localizacao_por_lat_lon(lat, lon)

    # Armazena os dados do acesso - Maicon Ferreira
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
    return jsonify({'status': 'ok'})  # Resposta JSON para o frontend - Maicon Ferreira

# Rota que exibe o mapa com os acessos - Maicon Ferreira
@app.route('/mapa')
def mapa():
    return render_template('mapa.html', acessos=acessos)  # Mapa com marcadores dos acessos - Maicon Ferreira

# Rota que exibe os acessos em tabela - Maicon Ferreira
@app.route('/acessos')
def listar_acessos():
    return render_template('acessos.html', acessos=acessos)  # Lista tabular dos acessos - Maicon Ferreira

# Inicialização da aplicação - Maicon Ferreira
if __name__ == '__main__':
    app.run(debug=True, port=5002)  # Mudar para outra porta
