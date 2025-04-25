from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)
acessos = []

@app.route('/')
def home():
    return render_template("mapa.html")

@app.route('/registrar', methods=['POST'])
def registrar():
    data = request.json
    ip = request.headers.get('X-Forwarded-For', request.remote_addr).split(',')[0].strip()

    acesso = {
        'ip': ip,
        'lat': data.get('lat', 0),
        'lon': data.get('lon', 0),
        'city': data.get('city', 'Desconhecida'),
        'region': data.get('region', 'Desconhecida'),
        'country': data.get('country', 'Desconhecido'),
    }

    acessos.append(acesso)
    return jsonify({"status": "ok"}), 200

@app.route('/acessos')
def listar_acessos():
    return jsonify(acessos)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5002)
