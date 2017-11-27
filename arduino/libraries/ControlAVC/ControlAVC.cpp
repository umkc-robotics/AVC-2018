#include "ControlAVC.h"


void ControlAVC::attachThrottle(int pin, int min_delay, int max_delay) {
	ESC.attach(pin, min_delay, max_delay);
	current_throttle = NEUTRAL;
	ESC.write(current_throttle);
}

void ControlAVC::attachSteering(int pin, int min_delay, int max_delay) {
	STR.attach(pin, min_delay, max_delay);
	current_steering = NEUTRAL;
	STR.write(current_steering);	
}

void ControlAVC::performMovement() {
	ESC.write(current_throttle);
	STR.write(current_steering);
}

void ControlAVC::setForwardThrottle(int throttle) {
	throttle = constrain(throttle, MIN_COMMAND_THROTTLE, MAX_COMMAND_THROTTLE);
	if (throttle != 0) {
		current_throttle = map(throttle, MIN_COMMAND_THROTTLE, MAX_COMMAND_THROTTLE, NEUTRAL+THROTTLE_DEADZONE, NEUTRAL+MAX_ABS_THROTTLE);
	}
	else {
		current_throttle = NEUTRAL;
	}
	ESC.write(current_throttle);
}

void ControlAVC::setBackwardThrottle(int throttle) {
	throttle = constrain(throttle, MIN_COMMAND_THROTTLE, MAX_COMMAND_THROTTLE);
	if (throttle != 0) {
		current_throttle = map(throttle, MIN_COMMAND_THROTTLE, MAX_COMMAND_THROTTLE, NEUTRAL-THROTTLE_DEADZONE, NEUTRAL-MAX_ABS_THROTTLE);
	}
	else {
		current_throttle = NEUTRAL;
	}
	// if actually told to go backwards, use special movement
	if (current_throttle != NEUTRAL) {
		ESC.write(current_throttle);
		ESC.write(NEUTRAL);
		ESC.write(current_throttle);
	}
	else {
		ESC.write(current_throttle);
	}
}

void ControlAVC::stopThrottle() {
	current_throttle = NEUTRAL;
	ESC.write(current_throttle);
}

void ControlAVC::brake() {
	ESC.write(NEUTRAL-THROTTLE_DEADZONE);
}

void ControlAVC::setTurnAngle(int angle) {
	angle = constrain(angle, -MAX_ANGLE, MAX_ANGLE);
	if (angle > 0) {
		current_steering = map(angle, 1, MAX_ANGLE, NEUTRAL-TURN_DEADZONE, NEUTRAL-MAX_ABS_INPUT);
	}
	else if (angle < 0)  {
		current_steering = map(angle, -1, -MAX_ANGLE, NEUTRAL+TURN_DEADZONE, NEUTRAL+MAX_ABS_INPUT);
	}
	else {
		current_steering = NEUTRAL;
	}
	STR.write(current_steering);
}

void ControlAVC::straightenWheels() {
	current_steering =  NEUTRAL;
	STR.write(current_steering);
}
