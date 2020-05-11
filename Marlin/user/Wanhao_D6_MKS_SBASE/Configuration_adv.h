//
// structured configuration; see #13752
//

#pragma once

// BLTOUCH: work around issue #13368
#undef DEACTIVATE_SERVOS_AFTER_MOVE

#define EMERGENCY_PARSER

#define BINARY_FILE_TRANSFER

#define DIGIPOT_MCP4451
#define DIGIPOT_I2C_ADDRESS_A 0x2C
#define DIGIPOT_I2C_ADDRESS_B 0x2D

#undef  DIGIPOT_I2C_NUM_CHANNELS
#define DIGIPOT_I2C_NUM_CHANNELS 5

#undef  DIGIPOT_I2C_MOTOR_CURRENTS
#define DIGIPOT_I2C_MOTOR_CURRENTS { 1.2, 1.2, 1.2, 0.8, 0.8 }

// makes extruder crazy
#undef  LIN_ADVANCE
#define LIN_ADVANCE_K 0.22

#define CASE_LIGHT_ENABLE
#define CASE_LIGHT_DEFAULT_ON true
#define CASE_LIGHT_DEFAULT_BRIGHTNESS 255

#undef  HOMING_BUMP_MM
#undef  HOMING_BUMP_DIVISOR
#define HOMING_BUMP_MM      { 4, 4, 2 }
#define HOMING_BUMP_DIVISOR { 5, 5, 10 }

// note: verify jumpers
#undef  MICROSTEP_MODES
#define MICROSTEP_MODES { 32, 32, 32, 32, 32 }

#define MINIMUM_STEPPER_DIR_DELAY 1000

#define MINIMUM_STEPPER_PULSE 4

#define MAXIMUM_STEPPER_RATE 250000

#define ADAPTIVE_STEP_SMOOTHING

//
// nozzle temperature
//

#undef  WATCH_TEMP_PERIOD
#undef  WATCH_TEMP_INCREASE
#define WATCH_TEMP_PERIOD    40              // Seconds
#define WATCH_TEMP_INCREASE   2              // Celsius

#undef  THERMAL_PROTECTION_PERIOD
#undef  THERMAL_PROTECTION_HYSTERESIS
#define THERMAL_PROTECTION_PERIOD      60    // Seconds
#define THERMAL_PROTECTION_HYSTERESIS   4    // Celsius

//
// hotbed temperature
//

#undef  WATCH_BED_TEMP_PERIOD
#undef  WATCH_BED_TEMP_INCREASE
#define WATCH_BED_TEMP_PERIOD     80               // Seconds
#define WATCH_BED_TEMP_INCREASE    2               // Celsius

#undef  THERMAL_PROTECTION_BED_PERIOD
#undef  THERMAL_PROTECTION_BED_HYSTERESIS
#define THERMAL_PROTECTION_BED_PERIOD        60 // Seconds
#define THERMAL_PROTECTION_BED_HYSTERESIS     2 // Celsius

//
// chamber temperature
//

#undef  CHAMBER_MINTEMP
#undef  CHAMBER_MAXTEMP
#define CHAMBER_MINTEMP            10
#define CHAMBER_MAXTEMP            90

#undef  THERMAL_PROTECTION_CHAMBER_PERIOD
#undef  THERMAL_PROTECTION_CHAMBER_HYSTERESIS
#define THERMAL_PROTECTION_CHAMBER_PERIOD     60 // Seconds
#define THERMAL_PROTECTION_CHAMBER_HYSTERESIS 2  // Celsius

//
// runtime mini step of Z
//

#define BABYSTEPPING
#define BABYSTEP_INVERT_Z false
#define BABYSTEP_MULTIPLICATOR_Z  1
#define BABYSTEP_ALWAYS_AVAILABLE
#define BABYSTEP_ZPROBE_OFFSET
