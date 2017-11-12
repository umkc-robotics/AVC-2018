#include "StartButton.h"

#define START_BUTTON_PIN 2



StartButton button;

void setup() {
	button = StartButton(START_BUTTON_PIN);
	attachInterrupt(digitalPinToInterrupt(START_BUTTON_PIN),buttonFunction,CHANGE);
	Serial.begin(9600);
}

void loop() {
	if (button.wasPressed()) {
		Serial.println("GOOD PRESSED!");
		button.reset();
	}
}

void buttonFunction() {
	button.checkButton();
}
