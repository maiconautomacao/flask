import qrcode

# Substitua pela URL gerada pelo ngrok
url_render = "https://8260-187-86-249-142.ngrok-free.app"

# Criação do QR Code
qr = qrcode.make(url_render)

# Salvar o QR Code em um arquivo de imagem
qr.save("qrcode.png")
