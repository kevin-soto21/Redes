const slider = document.getElementById("angle");
const angleNum = document.getElementById("angleNum");
const statusEl = document.getElementById("status");

// Elementos nuevos para el Caso de Estudio
const bitacoraEl = document.getElementById("bitacora");
const ledV = document.getElementById("ledV");
const ledR = document.getElementById("ledR");
const ledA = document.getElementById("ledA");

const btn0 = document.getElementById("btn0");
const btn90 = document.getElementById("btn90");
const btn180 = document.getElementById("btn180");

const btnDirect = document.getElementById("btnDirect");
const btnSmooth = document.getElementById("btnSmooth");

const servoVideo = document.getElementById("servoVideo");

let modeSmooth5s = true;

function setStatus(t) { statusEl.textContent = t; }
function clamp(v, lo, hi) { return Math.max(lo, Math.min(hi, v)); }

/**
 * NUEVA FUNCIÓN: Actualiza los LEDs en pantalla y registra en bitácora
 */
function actualizarEstadoDispositivo(angulo, mensaje) {
  // 1. Lógica de LEDs Visuales
  ledV.classList.remove("active");
  ledR.classList.remove("active");
  ledA.classList.remove("active");

  if (angulo == 0) ledV.classList.add("active");
  else if (angulo == 90) ledR.classList.add("active");
  else if (angulo == 180) ledA.classList.add("active");

  // 2. Registro en Bitácora
  const ahora = new Date().toLocaleTimeString();
  const nuevaEntrada = document.createElement("div");
  nuevaEntrada.className = "log-entry";
  nuevaEntrada.innerHTML = `<strong>[${ahora}]</strong> Ángulo: ${angulo}° | ${mensaje}`;
  
  // Insertar al inicio de la bitácora
  if (bitacoraEl) {
    bitacoraEl.prepend(nuevaEntrada);
  }
}

function syncUI(angle) {
  angle = clamp(parseInt(angle, 10) || 0, 0, 180);
  slider.value = angle;
  angleNum.value = angle;
}

function playSyncVideo() {
  if (!servoVideo) return;
  try {
    servoVideo.pause();
    servoVideo.currentTime = 0;
    const p = servoVideo.play();
    if (p && typeof p.catch === "function") p.catch(() => {});
  } catch (_) {}
}

async function sendAngle(angle) {
  angle = clamp(parseInt(angle, 10) || 0, 0, 180);

  setStatus("Enviando...");
  try {
    const res = await fetch("/api/servo", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ angle: angle, smooth5s: modeSmooth5s })
    });

    if (res.status === 401) {
      window.location.href = "/login";
      return;
    }

    const data = await res.json();

    if (data.ok) {
      setStatus(`OK: ${data.resp}`);
      
      // ACTUALIZACIÓN PARA EL CASO DE ESTUDIO
      actualizarEstadoDispositivo(angle, data.resp);

      if (modeSmooth5s) {
        // El video se sincroniza con el movimiento de 5s
        setTimeout(playSyncVideo, 120);
      }
    } else {
      setStatus(`Error: ${data.resp || data.error || "desconocido"}`);
    }
  } catch (e) {
    setStatus(`Error: ${e}`);
  }
}

// Eventos de control
slider.addEventListener("input", () => syncUI(slider.value));
slider.addEventListener("change", () => sendAngle(slider.value));

angleNum.addEventListener("change", () => {
  syncUI(angleNum.value);
  sendAngle(angleNum.value);
});

// Botones de acceso rápido
btn0.addEventListener("click", () => { syncUI(0); sendAngle(0); });
btn90.addEventListener("click", () => { syncUI(90); sendAngle(90); });
btn180.addEventListener("click", () => { syncUI(180); sendAngle(180); });

// Selección de modos
btnDirect.addEventListener("click", () => {
  modeSmooth5s = false;
  setStatus("Modo: directo");
});

btnSmooth.addEventListener("click", () => {
  modeSmooth5s = true;
  setStatus("Modo: suave 5s (video)");
});

// Inicialización
syncUI(90);
sendAngle(90);
