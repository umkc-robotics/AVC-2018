#ifndef CONTROLAVC_H
#define CONTROLAVC_H

#include "Arduino.h"
#include <Servo.h>

class ControlAVC {
private:
	Servo ESC;
	Servo STR;
	const int THROTTLE_DEADZONE = 100; //minimum throttle for wheel spin is 76
	const int TURN_DEADZONE = 0;
	const int NEUTRAL = 1500;
	const int MAX_ABS_THROTTLE = 200;
	const int MAX_ABS_INPUT = 500;
	const int MAX_ANGLE = 27;
	const int MIN_COMMAND_THROTTLE = 0;
	const int MAX_COMMAND_THROTTLE = 99;
	int current_throttle;
	int current_steering;
public:
	ControlAVC() {};
	// attach servos
	void attachThrottle(int pin, int min_delay, int max_delay);
	void attachSteering(int pin, int min_delay, int max_delay);
	// getters
	int get_current_throttle() { return current_throttle; };
	int get_current_steering() { return current_steering; };
	// update servo values
	void performMovement();
	// set values for throttle
	void setForwardThrottle(int throttle);
	void setBackwardThrottle(int throttle);
	void stopThrottle();
	void brake();
	// set values for steering
	void setTurnAngle(int angle);
	void straightenWheels();
	// reset values to neutral
	void reset() { stopThrottle(); straightenWheels(); };
};

#endif
