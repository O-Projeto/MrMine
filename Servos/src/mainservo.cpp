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
    servo1.attach(middle);
    servo2.attach(thumb);
    servo3.attach(fingerfinger);
    servo4.attach(pink);
    servo5.attach(pointing);
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
        int dataT = data.substring(0,3).toInt();
        int dataPOINT = data.substring(4,8).toInt();
        int dataM = data.substring(8,12).toInt();
        int dataFF = data.substring(12,16).toInt();
        int dataP = data.substring(16,20).toInt();
        
        
        servo5.write(abs(dataT));
        servo2.write(abs(dataPOINT));
        servo1.write(abs(dataM));
        servo3.write(abs(dataFF));
        servo4.write(abs(dataP));
        
        /*
        servo1.write(abs(0));
        
        servo1.write(abs(180));
        delay(1500);*/
        
        /*
        servo1.write(abs(20));
        servo2.write(abs(20));
        servo3.write(abs(20));
        servo4.write(abs(20)); 
        servo5.write(abs(20));
        delay(5000);
        servo1.write(abs(130));
        servo2.write(abs(130));
        servo3.write(abs(130));
        servo4.write(abs(130)); 
        servo5.write(abs(130));
        delay(5000);
        */

        //ESP_LOGI(&TAG, "dataPOINT:%d", dataPOINT);
    }
    
}