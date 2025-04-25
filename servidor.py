from flask import Flask, request, render_template, jsonify
import datetime

app = Flask(__name__)

acessos = []

@app.route('/')  # Esta será a rota visitada via QR Code
def coletar():
    return render_template('coleta.html')  # Agora renderiza a coleta!

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

@app.route('/mapa')  # Agora o mapa está acessível por /mapa
def mapa():
    return render_template('mapa.html', acessos=acessos)

@app.route('/acessos')
def listar_acessos():
    return render_template('acessos.html', acessos=acessos)

if __name__ == '__main__':
    app.run(debug=True)
