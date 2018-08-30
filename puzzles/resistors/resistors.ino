#include <string.h>
#include <FastLED.h>

#define NUM_LEDS 11
#define DATA_PIN 6

CRGB leds[NUM_LEDS];

const int NUM_RESISTORS = 2;

String incoming = "";
int lit = 0;

void setup() {
    FastLED.addLeds<NEOPIXEL, DATA_PIN>(leds, NUM_LEDS);
    reset();
    Serial.begin(9600);
    Serial.setTimeout(50);
}

void loop() {
    while (Serial.available() > 0) {
        int inChar = Serial.read();

        // if you get a newline, print the string, then the string's value:
        if (inChar == '\n') {
            if(incoming == "reset") {
                reset();
                Serial.println("reset");
                Serial.println("RESISTORS");
            } else if(lit == NUM_RESISTORS) {
                int led = incoming.toInt();
                leds[led*2] = CRGB::Green;
                FastLED.show();
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
    for(int i = 0; i < NUM_LEDS; i += 2) {
        leds[i] = CRGB::Green; 
    }
    FastLED.show();
    lit = 0;
}

void addLit(int led) {
    if(lit < NUM_RESISTORS) {
        leds[led*2] = CRGB::Red;
        FastLED.show();
        lit++;
        if(lit == NUM_RESISTORS) {
            Serial.println("ready");
        }
    }
}
