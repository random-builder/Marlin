
### code in M43.cpp

```cpp
// view lpc1768 pwm state
void tester_report(uint8_t this_pin) {
    SERIAL_ECHOLNPGM("TESTER START");
    //
    bool pin_has_pwm = LPC176x::pin_has_pwm(this_pin);
    bool pin_pwm_enabled = LPC176x::pin_pwm_enabled(this_pin);
    uint8_t pin_get_pwm_channel = LPC176x::pin_get_pwm_channel(this_pin);
    //
    SERIAL_ECHOLNPAIR("this_pin: ", this_pin);
    SERIAL_ECHOLNPAIR("pin_has_pwm: ", pin_has_pwm);
    SERIAL_ECHOLNPAIR("pin_pwm_enabled: ", pin_pwm_enabled);
    SERIAL_ECHOLNPAIR("pin_get_pwm_channel: ", pin_get_pwm_channel);
    //
    SERIAL_ECHOLNPGM("TESTER FINISH");
}

void GcodeSuite::M43() {
  if (parser.seen('A')) return tester_report(P3_25);
  if (parser.seen('B')) return tester_report(P3_26);
  // ...
}
```

### M43 A

```
Send: M43 A
Recv: TESTER START
Recv: this_pin: 121
Recv: pin_has_pwm: 1
Recv: pin_pwm_enabled: 1
Recv: pin_get_pwm_channel: 1
Recv: TESTER FINISH
Recv: ok
```

### M43 B

```
Send: M43 B
Recv: TESTER START
Recv: this_pin: 122
Recv: pin_has_pwm: 1
Recv: pin_pwm_enabled: 1
Recv: pin_get_pwm_channel: 2
Recv: TESTER FINISH
Recv: ok
```
