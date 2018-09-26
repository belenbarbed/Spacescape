#include <string.h>

String incoming = "";

const int LIGHTS = 10;

int MAX_BRIGHTNESS = 255;

void setup() {
    Serial.begin(9600);
    Serial.setTimeout(50);
    pinMode(LIGHTS, OUTPUT);
    reset();
}

void loop() {
    while (Serial.available() > 0) {
        int inChar = Serial.read();

        if (inChar == '\n') {
            if(incoming == "reset") {
                reset();
                Serial.println("reset");
                Serial.println("LIGHTS");
            } else if(incoming == "fade") {
                fade();
            } else if(incoming == "dim") {
                dim();
            } else if(incoming == "flash") {
                flash();
            }
            // clear the string for new input:
            incoming = "";
        } else {
            incoming += (char)inChar;
        }
    }
}

void fade() {
    for(int i = 30; i <= MAX_BRIGHTNESS; i++) {
        analogWrite(LIGHTS, i);
        delay(20);
    }
}

void dim() {
    for(int i = MAX_BRIGHTNESS; i >= 30; i--) {
        analogWrite(LIGHTS, i);
        delay(1);
    }
}

void flash() {
    analogWrite(LIGHTS, 30);
    delay(400);
    analogWrite(LIGHTS, 150);
    delay(100);
    analogWrite(LIGHTS, 30);
    delay(200);
    analogWrite(LIGHTS, 150);
    delay(300);
    analogWrite(LIGHTS, 30);
    delay(500);
    analogWrite(LIGHTS, 150);
    delay(1000);
    analogWrite(LIGHTS, MAX_BRIGHTNESS);
}

void reset() {
    analogWrite(LIGHTS, 255);
}
