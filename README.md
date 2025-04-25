
# 📍 Projeto de Localização e Redirecionamento via QR Code

Este projeto captura a geolocalização de visitantes (via GPS ou IP), armazena essas informações e redireciona automaticamente para um perfil do Instagram. Ideal para campanhas físicas com QR Code, feiras, ou marketing direto.

---

## 🗂 Estrutura de Diretórios

```
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
```

---

## ✅ Requisitos

- Python 3.7+
- Conta gratuita em [ipinfo.io](https://ipinfo.io/) para obter um token de API
- Conta gratuita em [render.com](https://render.com) para obter o link de direcionamento
- Conta gratuira em [GitHub](https://github.com) hospedar seu projeto e direcionamento para o render



Instale as dependências:

```bash
pip install -r requirements.txt
```

---

## 🚀 Instruções de Uso

### 1. Clone o repositório e inicie o Git

```bash
git init
git add .
git commit -m "Primeiro commit"
git remote add origin https://github.com/mateusflorenzano/localizacao-qrcode.git
git push -u origin master / main
git push
```

### 2. Configure seu token IPInfo

No arquivo `coleta.html` e/ou `coleta.js`, substitua:

```js
fetch('https://ipinfo.io/json?token=SEU_TOKEN_IPINFO')
```

Por:

```js
fetch('https://ipinfo.io/json?token=SEU_TOKEN_REAL')
```

---

### 3. Execute o Servidor

```bash
python servidor.py
```

A aplicação será iniciada em `http://localhost:5002/`.

---

### 4. Gere o QR Code

Edite o link do seu servidor em `gerar_qrcode.py`:

```python
url = "http://localhost:5002"
```

E execute:

```bash
python gerar_qrcode.py
```

O QR Code será salvo como `qrcode.png`.

---

## 🌐 Rotas Disponíveis

- `/` → Página de coleta e redirecionamento (coleta.html)
- `/registrar` → Recebe dados de localização (POST)
- `/acessos` → Lista os acessos (IP, localização)
- `/mapa` → Mapa com os pontos de acesso

---

## 📦 Requisitos do Projeto (`requirements.txt`)

```
Flask==2.1.1
requests==2.26.0
qrcode==6.1
```

---

## 🛠 Melhorias Futuras

- [ ] Armazenar dados em banco (SQLite ou PostgreSQL)
- [ ] Proteger a página de acessos com autenticação
- [ ] Adicionar informações de navegador/dispositivo
- [ ] Deploy gratuito com [Render](https://render.com) ou [Railway](https://railway.app)
