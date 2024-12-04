# Rotation rates conversion

> _all config variables are scaled to CLI values, Configurators might use different scaling. If Configurator value is used, it is in square brackets []_

## Rotation rates in MultiWii/Baseflight/Cleanflight

MultiWii/Baseflight/Cleanflight uses arbitrary combination of `rc_rate` and axis rate to determine maximum rotation speed in degrees per second [dps]. By default, `rc_rate` is equal 90 [0,9] for ROLL and PITCH and 100 [1,0] for YAW. Mind that ***rc_rate*** for YAW is hardcoded and can not be changed!!

With default `rc_rate` values, old rates can be converted to maximum rotation speed at full stick deflection using following table:

> To simplify, we assume that `rc_rate` is equal 100 to match ROLL, PITCH and YAW. RC Rate scaling is linear, so to compute rotation on rc_rate 90, divide by 100 and multiply by 90.


| Rate | Rate in Configurator | Rotation speed [dps] |
| ---- | -------------------- | -------------------- |
| 0 | 0,00 | 200dps |
| 10 | 0,10 | 300dps |
| 20 | 0,20 | 400dps |
| 30 | 0,30 | 500dps |
| 40 | 0,40 | 600dps |
| 50 | 0,50 | 700dps |

This can be computed using following equation:

` rotation_in_dps = (rate + 20) * 10`

## Rotation rates in INAV 1.2

INAV 1.2 changes how rates (rotation speed at maximum stick deflection) is stored. Instead of arbitrary combination of `rc_rate` and axis rate, INAV stores rates as `rate_in_dps / 10`. Also `rc_rate`, as not needed, is removed.

| Rate | Rate in Configurator | Rotation speed [dps] |
| ---- | -------------------- | -------------------- |
| 0 | 0,00 | invalid |
| 9 | 0,09 | 90dps |
| 10 | 0,10 | 100dps |
| 20 | 0,20 | 200dps |
| 40 | 0,40 | 400dps |
| 50 | 0,50 | 500dps |

Example: "set yaw_rate = 3" defines a rotation rate of 30dps on YAW axis that UAV will try to archive on max. stick deflection.  
Latest INAV Configurator detects INAV 1.2 and allows to enter rates scaled to degrees per second

//TODO: explain how rates work in servo setups (airplanes mainly).

## Conversion

| Old Rate | INAV 1.2 New Rate |
| ---- | -------------------- |
| 0 | 20 |
| 10 | 30 |
| 20 | 40 |
| 30 | 50 |
| 40 | 60 |
| 50 | 70 |

```new_rate = old_rate + 20```