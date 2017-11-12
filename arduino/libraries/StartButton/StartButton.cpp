#include "StartButton.h"


StartButton::StartButton(int pin) {
	button_pin = pin;
	pinMode(button_pin, INPUT);
}

StartButton::StartButton(int pin, unsigned long min, unsigned long max) {
	StartButton::StartButton(pin);
	min_press = min;
	max_press = max;
}

void StartButton::checkButton() {
	current_time_pressed = millis();
	// make sure that button is pressed when checking if was not pressed before
	if (digitalRead(button_pin) == HIGH) {
		// if was not pressed, set previous time to current time, register as a press
		if (!was_pressed) {
			previous_time_pressed = current_time_pressed;
			was_pressed = true;
		}
		else {
			// do nothing, this is a bad input
		}
	}
	// make sure button is NOT pressed when checking if was pressed before
	else {
		// if was pressed 
		if (was_pressed) {
			// if between min and max time:
			if (current_time_pressed - previous_time_pressed >= min_press &&
				current_time_pressed - previous_time_pressed <= max_press) {
				// then it was ACTUALLY pressed
				was_actually_just_pressed = true;
			}
			else {
				// otherwise, this was a bad press
				was_actually_just_badly_pressed = true;
			}
			was_pressed = false;
		}
	}
}