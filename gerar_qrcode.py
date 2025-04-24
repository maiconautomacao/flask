import qrcode

# Substitua pela URL gerada pelo ngrok
url_render = "https://flask-1-jl7h.onrender.com/"

# Criação do QR Code
qr = qrcode.make(url_render)

# Salvar o QR Code em um arquivo de imagem
qr.save("qrcode.png")
