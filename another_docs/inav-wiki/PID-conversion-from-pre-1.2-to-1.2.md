With INAV 1.2, PID scaling and default values has changed to match Cleanflight/Betaflight LuxFloat and MWRewrite PID controllers.

When migrating from ***pre 1.2*** to 1.2, use following conversion:

## ROLL/PICH/YAW

`INAV 1.2 P_gain = Pre_1.2_P_gain / 1.3`

`INAV 1.2 I_gain = Pre_1.2_I_gain / 2.5`

`INAV 1.2 D_gain = Pre_1.2_D_gain / 2.1`

## LEVEL

`INAV 1.2 LEVEL P = Pre_1.2_LEVEL_P / 6.1`

Level `I` (LowPassFilter cutoff frequency) and `D` (Horizon transition point) did not changed.

Or use [this Google Docs spreadsheet](https://docs.google.com/spreadsheets/d/133vfzz6_38W5nUmoRNuP7ZX9V1E-8IG6x0FxuxkBuQg/edit?pref=2&pli=1#gid=0) to recompute tune from INAV 1.1