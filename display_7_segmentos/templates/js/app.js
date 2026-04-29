const botones = document.querySelectorAll("button");
const numeroSeleccionado = document.getElementById("numeroSeleccionado");
const mensaje = document.getElementById("mensaje");

botones.forEach(boton => {
    boton.addEventListener("click", () => {
        const numero = boton.getAttribute("data-numero");

        fetch("/set_number", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                number: numero
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                numeroSeleccionado.textContent = numero;
                mensaje.textContent = "Arduino respondió: " + data.message;
                mensaje.className = "correcto";
            } else {
                mensaje.textContent = data.message;
                mensaje.className = "error";
            }
        })
        .catch(error => {
            mensaje.textContent = "Error de comunicación con Flask";
            mensaje.className = "error";
            console.log(error);
        });
    });
});
