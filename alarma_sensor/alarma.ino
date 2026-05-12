// Definición de pines
const int PIR_PIN = 2;    // Sensor de movimiento
const int LED_ROJO = 13;  // Alerta
const int LED_VERDE = 3;  // Sistema OK

void setup() {
  Serial.begin(9600);
  
  pinMode(PIR_PIN, INPUT);
  pinMode(LED_ROJO, OUTPUT);
  pinMode(LED_VERDE, OUTPUT);
  
  // Al arrancar, el verde se enciende (Sistema Vigilando)
  digitalWrite(LED_VERDE, HIGH);
  digitalWrite(LED_ROJO, LOW);
}

void loop() {
  int estado = digitalRead(PIR_PIN);
  
  if (estado == HIGH) {
    // ¡Movimiento detectado!
    digitalWrite(LED_VERDE, LOW);   // Apaga verde
    digitalWrite(LED_ROJO, HIGH);  // Enciende rojo
    
    Serial.println("ALERTA");      // Envía aviso a Python
    delay(4000);                   // Mantiene la alerta 4 segundos
  } else {
    // Todo tranquilo
    digitalWrite(LED_VERDE, HIGH);
    digitalWrite(LED_ROJO, LOW);
  }
  delay(100);
}
