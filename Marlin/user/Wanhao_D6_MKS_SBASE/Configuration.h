//
// structured configuration; see #13752
//

#pragma once

#define SDSUPPORT

#define EEPROM_SETTINGS

// enable M43 - Debug Pins
//#define PINS_DEBUGGING

// enable M111 S32
//#define DEBUG_LEVELING_FEATURE

#undef  SERIAL_PORT
#define SERIAL_PORT -1 // USB to OctoPrint

#undef  SERIAL_PORT_2
#define SERIAL_PORT_2 0 // AUX-1 to TFT panel

#undef  MOTHERBOARD
#define MOTHERBOARD BOARD_MKS_SBASE

#define CUSTOM_MACHINE_NAME "Wanhao-D6/MKS-SBASE"

#define MACHINE_UUID user_render(USER_STAMP)

#undef  EXTRUDERS
#define EXTRUDERS 2

#undef  DEFAULT_NOMINAL_FILAMENT_DIA
#define DEFAULT_NOMINAL_FILAMENT_DIA 1.75

#undef  TEMP_SENSOR_0
#undef  TEMP_SENSOR_1
#undef  TEMP_SENSOR_BED
#undef  TEMP_SENSOR_CHAMBER
#define TEMP_SENSOR_0 20      // PT100 via aplifier
#define TEMP_SENSOR_1 20      // PT100 via aplifier
#define TEMP_SENSOR_BED 1     // 100k thermistor direct
#define TEMP_SENSOR_CHAMBER 1 // 100k thermistor direct

#undef  HEATER_0_MAXTEMP
#undef  HEATER_1_MAXTEMP
#define HEATER_0_MAXTEMP 350
#define HEATER_1_MAXTEMP 350

// note: set fan on during tune
// extruder #1
// auto-tune command: "M303 E0 C8 S300"
// extruder #2
// auto-tune command: "M303 E1 C8 S300"
#undef  PIDTEMP
#define PIDTEMP

// 24v 12ohm 50W, large block
//#undef  DEFAULT_Kp
//#undef  DEFAULT_Ki
//#undef  DEFAULT_Kd
//#define DEFAULT_Kp 17.68
//#define DEFAULT_Ki 0.73
//#define DEFAULT_Kd 107.24

// 24v 12ohm 50W, small block
#undef  DEFAULT_Kp
#undef  DEFAULT_Ki
#undef  DEFAULT_Kd
#define DEFAULT_Kp 12.09
#define DEFAULT_Ki 0.57
#define DEFAULT_Kd 63.74

// auto-tune command: "M303 E-1 C8 S100"
#undef  PIDTEMPBED
#define PIDTEMPBED

// Wanhao-D6 24v 2ohm 300W pcb
#undef  DEFAULT_bedKp
#undef  DEFAULT_bedKi
#undef  DEFAULT_bedKd
#define DEFAULT_bedKp 49.69
#define DEFAULT_bedKi 9.51
#define DEFAULT_bedKd 173.09

// faster filament load/unload
#undef  PREVENT_COLD_EXTRUSION
#undef  EXTRUDE_MINTEMP
#define PREVENT_COLD_EXTRUSION
#define EXTRUDE_MINTEMP 195

// using bowden with gearbox
#undef  PREVENT_LENGTHY_EXTRUDE
#undef  EXTRUDE_MAXLENGTH
#define PREVENT_LENGTHY_EXTRUDE
#define EXTRUDE_MAXLENGTH 600

// using direct drive gears
#undef  INVERT_E0_DIR
#undef  INVERT_E1_DIR
#define INVERT_E0_DIR true
#define INVERT_E1_DIR true

// using motion limit switches
#define USE_XMAX_PLUG
#define USE_YMAX_PLUG
#define USE_ZMAX_PLUG

// using active/powered switches
#undef  X_MIN_ENDSTOP_INVERTING
#undef  Y_MIN_ENDSTOP_INVERTING
#undef  Z_MIN_ENDSTOP_INVERTING
#undef  X_MAX_ENDSTOP_INVERTING
#undef  Y_MAX_ENDSTOP_INVERTING
#undef  Z_MAX_ENDSTOP_INVERTING
#define X_MIN_ENDSTOP_INVERTING true
#define Y_MIN_ENDSTOP_INVERTING true
#define Z_MIN_ENDSTOP_INVERTING true
#define X_MAX_ENDSTOP_INVERTING true
#define Y_MAX_ENDSTOP_INVERTING true
#define Z_MAX_ENDSTOP_INVERTING true

// using default MKS drivers
#define X_DRIVER_TYPE  DRV8825
#define Y_DRIVER_TYPE  DRV8825
#define Z_DRIVER_TYPE  DRV8825
#define E0_DRIVER_TYPE DRV8825
#define E1_DRIVER_TYPE DRV8825

#define DISTINCT_E_FACTORS

#undef  DEFAULT_AXIS_STEPS_PER_UNIT
#define DEFAULT_AXIS_STEPS_PER_UNIT   { 160, 160, 1600, 830, 830 }

#undef  DEFAULT_MAX_FEEDRATE
#define DEFAULT_MAX_FEEDRATE          { 500, 500, 25, 50, 50 }

#undef  DEFAULT_MAX_ACCELERATION
#define DEFAULT_MAX_ACCELERATION      { 9000, 9000, 100, 10000, 10000 }

#define S_CURVE_ACCELERATION

//
// HOMING
//

#define NO_MOTION_BEFORE_HOMING

#define Z_SAFE_HOMING
#define Z_SAFE_HOMING_X_POINT ((X_BED_SIZE) / 2)
#define Z_SAFE_HOMING_Y_POINT ((Y_BED_SIZE) / 2)

#undef  HOMING_FEEDRATE_XY
#undef  HOMING_FEEDRATE_Z
#define HOMING_FEEDRATE_XY (80*60)
#define HOMING_FEEDRATE_Z  (20*60)

#define Z_HOMING_HEIGHT  3
#define Z_AFTER_HOMING   9

//
// PROBE/BLTOUCH
//

// enable negative probe offset
#undef  MIN_SOFTWARE_ENDSTOP_Z

// using servo zero
#define Z_PROBE_SERVO_NR 0

// using dedicated probe pin
#undef  Z_MIN_PROBE_USES_Z_MIN_ENDSTOP_PIN

// probe version 2.x
#define BLTOUCH
#undef  BLTOUCH_HS_MODE
#undef  BLTOUCH_FORCE_SW_MODE
#undef  BLTOUCH_FORCE_MODE_SET

// fast/light plastic rod
#define BLTOUCH_DELAY 200
#define BLTOUCH_RESET_DELAY    BLTOUCH_DELAY + 100
#define BLTOUCH_DEPLOY_DELAY   BLTOUCH_DELAY + 100
#define BLTOUCH_STOW_DELAY     BLTOUCH_DELAY + 100

// probe position
// X: at center of the nozzle
// Y: far in back of the nozzle
// Z: deployed probe is below the nozzle
#undef  NOZZLE_TO_PROBE_OFFSET
#define NOZZLE_TO_PROBE_OFFSET { +0.0, +46.0, -1.0 } // X, Y, Z

// using full bed area
#undef  MIN_PROBE_EDGE
#define MIN_PROBE_EDGE 0

// remove heater noise
#define PROBING_HEATERS_OFF

#undef  Z_PROBE_LOW_POINT
#define Z_PROBE_LOW_POINT -2

#undef  Z_PROBE_SPEED_FAST
#undef  Z_PROBE_SPEED_SLOW
#define Z_PROBE_SPEED_FAST HOMING_FEEDRATE_Z
#define Z_PROBE_SPEED_SLOW (Z_PROBE_SPEED_FAST / 3)

// see src/module/probe.cpp
// note: ensure ~3 mm gap bed-vs-rod on deploy
#undef  Z_CLEARANCE_DEPLOY_PROBE
#undef  Z_CLEARANCE_BETWEEN_PROBES
#undef  Z_CLEARANCE_MULTI_PROBE
#undef  Z_AFTER_PROBING
#define Z_CLEARANCE_DEPLOY_PROBE   3 // Z Clearance for Deploy/Stow
#define Z_CLEARANCE_BETWEEN_PROBES 3 // Z Clearance between probe points
#define Z_CLEARANCE_MULTI_PROBE    3 // Z Clearance between multiple probes
#define Z_AFTER_PROBING            9 // Z position after probing is done

//
// LEVELING
//

#define AUTO_BED_LEVELING_UBL
#define ENABLE_LEVELING_FADE_HEIGHT
#define SEGMENT_LEVELED_MOVES
#define LEVELED_SEGMENT_LENGTH 5.0

#define RESTORE_LEVELING_AFTER_G28 false

#define MESH_INSET 0
#define GRID_MAX_POINTS_X 5
#define GRID_MAX_POINTS_Y 5

#define UBL_MESH_EDIT_MOVES_Z

//
// SERVO CONTROL
//

#define NUM_SERVOS 4

#undef  SERVO_DELAY
#define SERVO_DELAY { BLTOUCH_DELAY, 300, 300, 300 }
