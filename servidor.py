from flask import Flask, request, redirect, jsonify, render_template
import datetime

app = Flask(__name__)
acessos = []

@app.route('/')
def solicitar_localizacao():
    return render_template('coleta.html')

@app.route('/registrar', methods=['POST'])
def registrar():
    data = request.get_json()
    ip = request.headers.get('X-Forwarded-For', request.remote_addr).split(',')[0].strip()

    acesso = {
        'ip': ip,
        'lat': data.get('lat'),
        'lon': data.get('lon'),
        'precisa': data.get('precisa', False),
        'timestamp': datetime.datetime.now().isoformat()
    }
    acessos.append(acesso)
    return jsonify({'status': 'ok'})

@app.route('/acessos')
def mostrar_acessos():
    return render_template("acessos.html", acessos=acessos)

@app.route('/mapa')
def exibir_mapa():
    return render_template("mapa.html", acessos=acessos)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5002)
