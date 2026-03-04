function enviarBrillo(numLed, valor) {
    // Esta sola función sabe a qué LED le hablas gracias al 'numLed'
    fetch('/set_led', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ led: numLed, value: valor })
    })
    .then(response => response.json())
    .then(data => console.log("Servidor:", data.resp));
}
