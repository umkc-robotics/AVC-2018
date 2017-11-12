#include <SPI.h>
#include <Wire.h>
#include "StartButton.h"
#include "Adafruit_GFX.h"
#include "Adafruit_SSD1306.h"

#define START_BUTTON_PIN 2

// LCD DEFINITION
Adafruit_SSD1306 display(-1);
// BUTTON DEFINITION
StartButton button;

void setup() {
	button = StartButton(START_BUTTON_PIN);
	initializeDisplay();
	initializeButton();
	Serial.begin(9600);
}

void loop() {
	if (button.wasPressed()) {
		Serial.println("GOOD PRESSED!");
		showText("PRESSED!");
		button.reset();
		delay(200);
		showText("");
	}
}

void initializeDisplay() {
	display.begin(SSD1306_SWITCHCAPVCC, 0x3C);
	display.display();
	display.clearDisplay();
}

// display text on OLED display
void showText(String text) {
	display.setTextSize(1);
	display.setTextColor(WHITE);
	display.setCursor(0,0);
	display.println(text);
	display.display();
	display.clearDisplay();
}

void initializeButton() {
	attachInterrupt(digitalPinToInterrupt(START_BUTTON_PIN),buttonFunction,CHANGE);
}

void buttonFunction() {
	button.checkButton();
}
