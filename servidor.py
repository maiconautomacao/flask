from flask import Flask, request, render_template, jsonify
import datetime

app = Flask(__name__)

acessos = []

@app.route('/')
def home():
    return render_template('mapa.html', acessos=acessos)

@app.route('/registrar', methods=['POST'])
def registrar():
    data = request.get_json()
    ip = request.headers.get('X-Forwarded-For', request.remote_addr).split(',')[0].strip()

    acesso = {
        'ip': ip,
        'lat': data.get('lat'),
        'lon': data.get('lon'),
        'precisa': data.get('precisa', False),
        'city': data.get('city', ''),
        'region': data.get('region', ''),
        'country': data.get('country', ''),
        'timestamp': datetime.datetime.now().isoformat()
    }
    acessos.append(acesso)
    return jsonify({'status': 'ok'})

@app.route('/acessos')
def listar_acessos():
    return render_template('acessos.html', acessos=acessos)

@app.route('/mapa')
def exibir_mapa():
    return render_template("mapa.html", acessos=acessos)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5002)
