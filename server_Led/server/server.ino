#include <Servo.h>

Servo servo1;
const int SERVO_PIN = 9;
const int LED_VERDE = 2; // Pin para 0 grados
const int LED_ROJO  = 3; // Pin para 90 grados
const int LED_AZUL  = 4; // Pin para 180 grados

int angulo_actual = 90;

void setup() {
  Serial.begin(115200);
  servo1.attach(SERVO_PIN);
  
  pinMode(LED_VERDE, OUTPUT);
  pinMode(LED_ROJO, OUTPUT);
  pinMode(LED_AZUL, OUTPUT);

  // --- PRUEBA DE HARDWARE (Se prenden 3 segundos al conectar) ---
  digitalWrite(LED_VERDE, HIGH);
  digitalWrite(LED_ROJO, HIGH);
  digitalWrite(LED_AZUL, HIGH);
  delay(3000); 
  digitalWrite(LED_VERDE, LOW);
  digitalWrite(LED_ROJO, LOW);
  digitalWrite(LED_AZUL, LOW);
  // -------------------------------------------------------------

  servo1.write(angulo_actual);
  actualizarLEDs(angulo_actual);
  
  Serial.println("OK: Sistema Centinela Listo");
}

void actualizarLEDs(int angulo) {
  // Apagamos todos primero para limpiar el estado
  digitalWrite(LED_VERDE, LOW);
  digitalWrite(LED_ROJO, LOW);
  digitalWrite(LED_AZUL, LOW);

  // Encendido por rangos (por si el slider no es exacto)
  if (angulo >= 0 && angulo <= 5) {
    digitalWrite(LED_VERDE, HIGH);
  } 
  else if (angulo >= 85 && angulo <= 95) {
    digitalWrite(LED_ROJO, HIGH);
  } 
  else if (angulo >= 175 && angulo <= 180) {
    digitalWrite(LED_AZUL, HIGH);
  }
}

void moverDirecto(int ang) {
  ang = constrain(ang, 0, 180);
  servo1.write(ang);
  angulo_actual = ang;
  actualizarLEDs(ang);
}

void moverSuave5s(int objetivo) {
  objetivo = constrain(objetivo, 0, 180);
  const float duracion = 5.0; 
  const int steps = 50; // Reducimos steps para suavidad sin trabar el buffer
  const int dt_ms = (int)((duracion * 1000.0) / steps);
  int inicio = angulo_actual;

  for (int k = 1; k <= steps; k++) {
    float a = inicio + (objetivo - inicio) * ((float)k / (float)steps);
    servo1.write((int)(a + 0.5));
    delay(dt_ms);
  }
  angulo_actual = objetivo;
  actualizarLEDs(objetivo);
}

void loop() {
  if (Serial.available() > 0) {
    String line = Serial.readStringUntil('\n');
    line.trim();
    if (line.length() == 0) return;

    char cmd = 'A';
    int ang = 90;
    int sp = line.indexOf(' ');

    if (sp == -1) {
      ang = line.toInt();
    } else {
      cmd = toupper(line.charAt(0));
      ang = line.substring(sp + 1).toInt();
    }

    if (cmd == 'S') {
      moverSuave5s(ang);
      Serial.print("CONFIRMACION: Movimiento Suave a ");
    } else {
      moverDirecto(ang);
      Serial.print("OK: Movimiento Directo a ");
    }
    Serial.println(ang);
  }
}
