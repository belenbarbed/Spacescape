#include <string.h>

String incoming = "";

const int DOOR = 13;

void setup() {
    Serial.begin(9600);
    Serial.setTimeout(50);
    pinMode(DOOR, OUTPUT);
    reset();
}

void loop() {
    while (Serial.available() > 0) {
        int inChar = Serial.read();

        if (inChar == '\n') {
            if(incoming == "reset") {
                reset();
                Serial.println("reset");
                Serial.println("RELAY");
            } else if(incoming == "closeDoor") {
                closeDoor();
            } else if(incoming == "openDoor") {
                openDoor();
            }
            // clear the string for new input:
            incoming = "";
        } else {
            incoming += (char)inChar;
        }
    }
}

void closeDoor() {
    digitalWrite(DOOR, LOW);
}

void openDoor() {
    digitalWrite(DOOR, HIGH);
}

void reset() {
    openDoor();
}
