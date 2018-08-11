#include <string.h> 

const int NUM_RESISTORS = 2;

const int LEDS[6] = {2, 3, 4, 5, 8, 9};
String incoming = "";
int lit = 0;

void setup() {
    for(int i = 0; i < sizeof(LEDS); i++) {
        pinMode(LEDS[i], OUTPUT);
    }
	reset();
	Serial.begin(9600);
}

void loop() {
    while (Serial.available() > 0) {
        int inChar = Serial.read();

        // if you get a newline, print the string, then the string's value:
        if (inChar == '\n') {
            if(incoming == "reset") {
                reset();
                Serial.println("reset");
            } else {
                int led = incoming.toInt();
                addLit(led);
            }
            // clear the string for new input:
            incoming = "";
        } else {
            incoming += (char)inChar;
        }
    }
}

void reset() {
    for(int i = 0; i < sizeof(LEDS); i++) {
        digitalWrite(LEDS[i], LOW); 
    }
    lit = 0;
}

void addLit(int led) {
    if(lit < NUM_RESISTORS) {
        digitalWrite(LEDS[led], HIGH);
        lit++;
        if(lit == NUM_RESISTORS) {
            Serial.println("ready");
        }
    }
}
