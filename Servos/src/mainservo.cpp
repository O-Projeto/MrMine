#include "Servo.h"
#include <Arduino.h>
#include "esp_log.h"
#include <typeinfo>


static char* TAG = "MAINSERVO";

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

String data;


void setup() {
    Serial.begin(115200);
    Serial.setTimeout(10);
    servo1.attach(thumb);
    servo2.attach(pointing);
    servo3.attach(middle);
    servo4.attach(fingerfinger);
    servo5.attach(pink);
}

void loop() {
    // for(int posDegrees = 0; posDegrees <= 180; posDegrees++) {
    //     servo1.write(posDegrees);
    //     servo2.write(posDegrees);
    //     servo3.write(posDegrees);
    //     servo4.write(posDegrees);
    //     servo5.write(posDegrees);
    //     Serial.println(posDegrees);
    //     delay(20);
    // }

    // for(int posDegrees = 180; posDegrees >= 0; posDegrees--) {
    //     servo1.write(posDegrees);
    //     servo2.write(posDegrees);
    //     servo3.write(posDegrees);
    //     servo4.write(posDegrees);
    //     servo5.write(posDegrees);
    //     Serial.println(posDegrees);
    //     delay(20);
    // }

    if (Serial.available() ) {
        //data = Serial.readString();
        //data.trim();
        data = Serial.readStringUntil('\n');
        


        Serial.println("data" + data);
        int dataT = data.substring(0,4).toInt();
        Serial.println(dataT);
        int dataPOINT = data.substring(5,9).toInt();
        int dataM = data.substring(10,14).toInt();
        int dataFF = data.substring(15,19).toInt();
        int dataP = data.substring(20,25).toInt();
        
        
        
        servo1.write(abs(dataT));
        servo2.write(abs(dataPOINT));
        servo3.write(abs(dataM));
        servo4.write(abs(dataFF));
        servo5.write(abs(dataP));
        ESP_LOGI(&TAG, "dataPOINT:%d", dataPOINT);
    }
}