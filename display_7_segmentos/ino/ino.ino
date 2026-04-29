// Display de 7 segmentos cátodo común
// Pines del Arduino conectados a los segmentos: a, b, c, d, e, f, g
int segmentos[] = {2, 3, 4, 5, 6, 7, 8};

// Tabla de números del 0 al 9
// 1 = segmento encendido
// 0 = segmento apagado
byte numeros[10][7] = {
  {1, 1, 1, 1, 1, 1, 0}, // 0
  {0, 1, 1, 0, 0, 0, 0}, // 1
  {1, 1, 0, 1, 1, 0, 1}, // 2
  {1, 1, 1, 1, 0, 0, 1}, // 3
  {0, 1, 1, 0, 0, 1, 1}, // 4
  {1, 0, 1, 1, 0, 1, 1}, // 5
  {1, 0, 1, 1, 1, 1, 1}, // 6
  {1, 1, 1, 0, 0, 0, 0}, // 7
  {1, 1, 1, 1, 1, 1, 1}, // 8
  {1, 1, 1, 1, 0, 1, 1}  // 9
};

void setup() {
  Serial.begin(9600);

  for (int i = 0; i < 7; i++) {
    pinMode(segmentos[i], OUTPUT);
  }

  mostrarNumero(0);

  Serial.println("OK:READY");
}

void loop() {
  if (Serial.available() > 0) {
    String dato = Serial.readStringUntil('\n');
    dato.trim();

    if (dato == "0" || dato == "1" || dato == "2" || dato == "3" || dato == "4" ||
        dato == "5" || dato == "6" || dato == "7" || dato == "8" || dato == "9") {
      
      int numero = dato.toInt();
      mostrarNumero(numero);

      Serial.print("OK:");
      Serial.println(numero);
    } else {
      Serial.println("COMANDO_INVALIDO");
    }
  }
}

void mostrarNumero(int numero) {
  for (int i = 0; i < 7; i++) {
    digitalWrite(segmentos[i], numeros[numero][i]);
  }
}
