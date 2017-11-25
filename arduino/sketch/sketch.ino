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



// delay time
const int delayTime = 2;

// input parsing
const int maxValues = 1;
String command; // general command
String values[maxValues]; // stores values for command
String fullString; // string used for checksum
char checksumChar;
bool waitingForChecksum = false;
int addTo = 0; // 0 for command, 1 for value
// output
String response; // response returned to main program
byte actualChecksum = ' ';


String formatFullString(String command, String value = "");



void setup() {
	button = StartButton(START_BUTTON_PIN);
	initializeDisplay();
	initializeButton();
	Serial.begin(9600);
	Serial.println(formatFullString("ready"));
	showText("Ready!");
}


void loop() {
	// parse serial for commands
	parseSerial();
	//loop_button();
}

void parseSerial() {
	// if something in serial, parse it
	if(Serial.available()){

		while (Serial.available() > 0)
		{

			char readIn = (char)Serial.read();
			// process Serial if command is now over
			if (readIn == '\n') {
				processSerial();
			}
			else if (waitingForChecksum) {
				checksumChar = readIn;
				waitingForChecksum = false;
				continue;
			}
			else {
				if (readIn == '*') {
					waitingForChecksum = true;
					continue;
				}
				else {
					// if | character, increment addTo
					if (readIn == '|') {
						addTo += 1;
					}
					else {
						// add to command if no | reached yet
						if (addTo == 0) {
							command += readIn;
						}
						// add to proper value in array
						else if (addTo <= maxValues) {
							values[addTo-1] += readIn;
						}
						// if values exceed max, then stop listening to prevent problems
						else {
							processSerial();
						}
					}
					// add character to fullString
					fullString += readIn;
				}
			}
		}
	}
}

void processSerial() {
	showText("Processing serial input...");
	// verify checksum
	if (!hasValidChecksum()) {
		response = "n";
	}
	else {
		response = interpretCommand();
	}
	// send response
	Serial.println(response);
	// empty out command, fullString, and value strings
	command = "";
	fullString = "";
	addTo = 0;
	waitingForChecksum = false;
	for (int i = 0; i < maxValues; i++) {
		values[i] = "";
	}
	showText("Done processing input!");
}

String formatFullString(String command, String value = "") {
	String formatted_msg = command;
	// add value if provided
	if (value.length() != 0) {
		formatted_msg += '|';
		formatted_msg += value;
	}
	// add checksum
	char checksum_for_msg = (char)calculateChecksum(formatted_msg);
	formatted_msg += '*';
	formatted_msg += checksum_for_msg;
	return formatted_msg;
}

void sendWithChecksum(String command, String value = "") {
	// First, format message
	String formatted_msg = command;
	// add value if provided
	if (value.length() != 0) {
		formatted_msg += '|';
		formatted_msg += value;
	}
	// add checksum
	char checksum_for_msg = (char)calculateChecksum(formatted_msg);
	formatted_msg += '*';
	formatted_msg += checksum_for_msg;
	// Then, send through serial
	Serial.println(formatted_msg);
}

bool hasValidChecksum() {
	// not valid if checksum was not actually changed
	if (checksumChar == ' ') {
		return false;
	}
	// not valid if message is less than 2 characters
	if (fullString.length() < 1) {
		return false;
	}
	actualChecksum = calculateChecksum(fullString);
	// check if resulting byte equals final char
	return actualChecksum == checksumChar;

}

byte calculateChecksum(String message) {
	byte calculated_checksum = 0;
	// for every character but the last (checksum byte), do XOR
	for (int i = 0; i < message.length(); i++) {
		calculated_checksum ^= message[i];
	}
	calculated_checksum = (calculated_checksum % 94) + 33;

	return calculated_checksum;
}

String interpretCommand() {
	String responseString = "n";
	if (command == "gb") {
		responseString = formatFullString("gb",button.wasPressed() ? "1" : "0");
	}
	return responseString;
}

void loop_button() {
	if (button.wasPressed()) {
		showText("PRESSED!");
		//sendWithChecksum("gb");
		//button.reset();
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
