#include <Servo.h>
#include <Arduino.h>

static const int thumb = 33;
static const int pointing = 25;
static const int middle = 26;
static const int fingerfinger = 27;
static const int pink = 14;


Servo servo1;
Servo servo2;
Servo servo3;
Servo servo4;
Servo servo5;


void setup() {
    Serial.begin(115200);
    servo1.attach(thumb);
    servo2.attach(pointing);
    servo3.attach(middle);
    servo4.attach(fingerfinger);
    servo5.attach(pink);
}

void loop() {
    for(int posDegrees = 0; posDegrees <= 180; posDegrees++) {
        servo1.write(posDegrees);
        servo2.write(posDegrees);
        servo3.write(posDegrees);
        servo4.write(posDegrees);
        servo5.write(posDegrees);
        Serial.println(posDegrees);
        delay(20);
    }

    for(int posDegrees = 180; posDegrees >= 0; posDegrees--) {
        servo1.write(posDegrees);
        servo2.write(posDegrees);
        servo3.write(posDegrees);
        servo4.write(posDegrees);
        servo5.write(posDegrees);
        Serial.println(posDegrees);
        delay(20);
    }
}