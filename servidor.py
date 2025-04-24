from flask import Flask, redirect, request, jsonify, render_template
import requests
import os

app = Flask(__name__)
acessos = []

@app.route('/')
def redirecionar_e_registrar():
    ip = request.headers.get('X-Forwarded-For', request.remote_addr).split(',')[0].strip()

    try:
        geo_info = requests.get(f'https://ipinfo.io/{ip}/json').json()
        loc = geo_info.get('loc')
        if loc:
            lat, lon = map(float, loc.split(','))
        else:
            lat, lon = None, None
    except Exception as e:
        print(f"Erro ao buscar localização: {e}")
        lat, lon = None, None
        geo_info = {}

    if lat is not None and lon is not None:
        acessos.append({
            'ip': ip,
            'lat': lat,
            'lon': lon,
            'city': geo_info.get('city', 'Desconhecida'),
            'region': geo_info.get('region', 'Desconhecida'),
            'country': geo_info.get('country', 'Desconhecido'),
        })

    return redirect("https://www.instagram.com/mateusflorenzano?igsh=ZmF5a2UyNml3Nmc0", code=302)

@app.route('/mapa')
def mapa():
    return render_template('mapa.html', acessos=acessos)

@app.route('/acessos')
def mostrar_acessos():
    return jsonify(acessos)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # para compatibilidade com Render
    app.run(debug=False, host='0.0.0.0', port=port)
