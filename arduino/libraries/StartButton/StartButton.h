#ifndef STARTBUTTON_H
#define STARTBUTTON_H

#include "Arduino.h"


class StartButton {
private:
	int button_pin;
	// button state variables
	volatile bool was_pressed = false;
	volatile unsigned long previous_time_pressed = 0;
	volatile unsigned long current_time_pressed = 0;
	volatile unsigned long min_press = 120;
	volatile unsigned long max_press = 1500;
	volatile bool was_actually_just_pressed = false;
	volatile bool was_actually_just_badly_pressed = false;
public:
	StartButton() {};
	StartButton(int pin);
	StartButton(int pin, unsigned long min, unsigned long max);
	// Interrupt function
	void checkButton();
	// Reset pressed state (set it to false)
	void reset() { was_actually_just_pressed = false; };
	// Check if button was pressed
	bool wasPressed() { return was_actually_just_pressed; };
	// SETTERS:
	void setMinPress(unsigned long min) { min_press = min; };
	void setMaxPress(unsigned long max) { max_press = max; };
};

#endif
