const NUM_RESISTORS = 2;
int incoming[NUM_RESISTORS]

int LED_PIN_0 = 2;
int LED_PIN_1 = 3;
int LED_PIN_2 = 4;
int LED_PIN_3 = 5;
int LED_PIN_4 = 6;
int LED_PIN_5 = 7;

void setup() {
	pinMode(LED_PIN_0, OUTPUT);
	pinMode(LED_PIN_1, OUTPUT);
	pinMode(LED_PIN_2, OUTPUT);
	pinMode(LED_PIN_3, OUTPUT);
	pinMode(LED_PIN_4, OUTPUT);
	pinMode(LED_PIN_5, OUTPUT);

	for (int i = 2; i < 8; i++) {
		digitalWrite(i, LOW);
	}

	Serial.begin(9600);
}

void loop() {
    if (Serial.available() == 2) {
        incoming[0] = (int)Serial.read();
        incoming[1] = (int)Serial.read();
        digitalWrite(incoming[0]+2, HIGH); 
        digitalWrite(incoming[1]+2, HIGH); 
        Serial.println("ready");
    }
	delay(200);
}