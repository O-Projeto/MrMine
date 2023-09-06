#include <Servo.h>

Servo servoX;
Servo servoY;

void setup() {
  Serial.begin(115200);
  servoX.attach(2);  // Pin 2 para o servo X
  servoY.attach(3);  // Pin 3 para o servo Y
}

void loop() {
  if (Serial.available() > 0) {
    String comando = Serial.readStringUntil('\n');
    if (comando.startsWith("x") && comando.endsWith("y")) {
      // Extrair os valores de x e y do comando
      int valorX = comando.substring(1, comando.indexOf("y")).toInt();
      int valorY = comando.substring(comando.indexOf("y") + 1, comando.length() - 1).toInt();
      
      // Mover os servos para as coordenadas recebidas
      servoX.write(valorX);
      servoY.write(valorY);
    }
  }
}