#include <Servo.h>

Servo servo1;
const int SERVO_PIN = 9;   // Señal del servo en D9

int angulo_actual = 90;

void setup() {
  Serial.begin(115200);
  servo1.attach(SERVO_PIN);

  servo1.write(angulo_actual);
  delay(300);

  Serial.println("OK Arduino Servo listo");
}

void moverDirecto(int ang) {
  ang = constrain(ang, 0, 180);
  servo1.write(ang);
  angulo_actual = ang;
}

void moverSuave5s(int objetivo) {
  objetivo = constrain(objetivo, 0, 180);

  const float duracion = 5.0;  // segundos
  const int steps = 100;
  const int dt_ms = (int)((duracion * 1000.0) / steps);

  int inicio = angulo_actual;

  for (int k = 1; k <= steps; k++) {
    float a = inicio + (objetivo - inicio) * ((float)k / (float)steps);
    servo1.write((int)(a + 0.5));
    delay(dt_ms);
  }

  angulo_actual = objetivo;
}

void loop() {
  if (!Serial.available()) return;

  String line = Serial.readStringUntil('\n');
  line.trim();
  if (line.length() == 0) return;

  // Acepta: "90" o "A 90" o "S 90"
  char cmd = 'A';
  int ang = 90;

  int sp = line.indexOf(' ');
  if (sp == -1) {
    ang = line.toInt();
    cmd = 'A';
  } else {
    cmd = toupper(line.charAt(0));
    ang = line.substring(sp + 1).toInt();
  }

  ang = constrain(ang, 0, 180);

  if (cmd == 'S') {
    moverSuave5s(ang);
    Serial.print("OK smooth5s angle=");
    Serial.println(ang);
  } else {
    moverDirecto(ang);
    Serial.print("OK angle=");
    Serial.println(ang);
  }
}
