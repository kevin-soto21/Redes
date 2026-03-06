const slider = document.getElementById("angle");
const angleNum = document.getElementById("angleNum");
const statusEl = document.getElementById("status");

const btn0 = document.getElementById("btn0");
const btn90 = document.getElementById("btn90");
const btn180 = document.getElementById("btn180");

const btnDirect = document.getElementById("btnDirect");
const btnSmooth = document.getElementById("btnSmooth");

const servoVideo = document.getElementById("servoVideo");

let modeSmooth5s = true;

function setStatus(t) { statusEl.textContent = t; }
function clamp(v, lo, hi) { return Math.max(lo, Math.min(hi, v)); }

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
      if (modeSmooth5s) {
        setTimeout(playSyncVideo, 120);
      }
    } else {
      setStatus(`Error: ${data.resp || data.error || "desconocido"}`);
    }
  } catch (e) {
    setStatus(`Error: ${e}`);
  }
}

// Slider: input solo UI, change manda comando
slider.addEventListener("input", () => syncUI(slider.value));
slider.addEventListener("change", () => sendAngle(slider.value));

// Número: manda al cambiar
angleNum.addEventListener("change", () => {
  syncUI(angleNum.value);
  sendAngle(angleNum.value);
});

// Botones
btn0.addEventListener("click", () => { syncUI(0); sendAngle(0); });
btn90.addEventListener("click", () => { syncUI(90); sendAngle(90); });
btn180.addEventListener("click", () => { syncUI(180); sendAngle(180); });

// Modos
btnDirect.addEventListener("click", () => {
  modeSmooth5s = false;
  setStatus("Modo: directo");
});

btnSmooth.addEventListener("click", () => {
  modeSmooth5s = true;
  setStatus("Modo: suave 5s (video)");
});

// Inicial
syncUI(90);
sendAngle(90);
