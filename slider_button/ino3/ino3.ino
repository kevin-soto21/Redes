const int LED_SISTEMA = 3; 
const int LED_RED = 6;
const int BTN_SISTEMA = 2;
const int BTN_RED = 4;

int estadoLed1 = 0;
int estadoLed2 = 0;

void setup() {
  Serial.begin(9600);
  pinMode(LED_SISTEMA, OUTPUT);
  pinMode(LED_RED, OUTPUT);
  pinMode(BTN_SISTEMA, INPUT_PULLUP);
  pinMode(BTN_RED, INPUT_PULLUP);
}

void loop() {
  if (Serial.available() > 0) {
    String data = Serial.readStringUntil('\n');
    data.trim();
    if (data.startsWith("LED1:")) {
      int v = data.substring(5).toInt();
      analogWrite(LED_SISTEMA, v);
      estadoLed1 = (v > 0) ? 1 : 0;
    } else if (data.startsWith("LED2:")) {
      int v = data.substring(5).toInt();
      analogWrite(LED_RED, v);
      estadoLed2 = (v > 0) ? 1 : 0;
    }
  }

  if (digitalRead(BTN_SISTEMA) == LOW) {
    estadoLed1 = !estadoLed1; 
    digitalWrite(LED_SISTEMA, estadoLed1 ? HIGH : LOW);
    Serial.println(estadoLed1 ? "BTN1_ACTIVE" : "BTN1_OFF");
    delay(250); 
  }

  if (digitalRead(BTN_RED) == LOW) {
    estadoLed2 = !estadoLed2; 
    digitalWrite(LED_RED, estadoLed2 ? HIGH : LOW);
    Serial.println(estadoLed2 ? "BTN2_ACTIVE" : "BTN2_OFF");
    delay(250); 
  }
}
