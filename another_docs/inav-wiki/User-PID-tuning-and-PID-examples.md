## PID tuning

Do it one step at a time. - zero out I and D and tune P, then add D, then add I to flight drift. Fine-tune using blackbox or HD camera. 


Caution: The values set in CLI are displayed (and input) in a different format in the PID tab of Cleanflight!
 - P-values: factor of 10, e.g. set p_pitch = 55 is displayed 5,5 in the configurator 
 - I-values: factor of 1000, e.g. set i_pitch = 20 is displayed 0.0020 in the configurator 
 - D-values: factor of 1, e.g. set d_pitch = 70 is displayed 70in the configurator 


# PID examples

**iNav have changed scaling of PIDs after from version 1.2(merged to master 22.jun 2016) [Conversation chart](https://github.com/iNavFlight/inav/wiki/PID-conversion-from-pre-1.2-to-1.2)**

**Template multirotors:**

1. **Name of frame:**
1. Size of frame:
1. Weight:
1. Total thrust:
1. Battery infomation:
1. iNav version:

```
PID and other values from CLI
```


**Template fixedwing:**

1. **Name of plane:**
1. Mixer used:
1. iNav version:
1. Additional infomation you see fit if not stock airplane:

```
PID and other values from CLI
```

1. **Wing Wing Z-84:**
1. Mixer used: Flying Wing
1. iNav version: iNav 1.3.1(Pre release)
1. Additional infomation you see fit if not stock airplane:

```
set gyro_sync = ON
set gyro_sync_denom = 1

set gyro_lpf = 42HZ
set gyro_soft_lpf_hz = 40
set acc_soft_lpf_hz = 15
set dterm_lpf_hz = 30

set nav_fw_launch_accel = 1716
set nav_fw_launch_detect_time = 40
set nav_fw_launch_thr = 1500
set nav_fw_launch_motor_delay = 150
set naw_fw_launch_timeout = 5000
set naw_fw_launch_climb_angle = 10

set p_pitch = 20
set i_pitch = 30
set d_pitch = 15
set p_roll = 25
set i_roll = 30
set d_roll = 15
set p_yaw = 0
set i_yaw = 0
set d_yaw = 0
set p_level = 20
set i_level = 5
set d_level = 75
set max_angle_inclination_rll = 600
set max_angle_inclination_pit = 450

set rc_expo = 40
set tpa_rate = 33
set tpa_breakpoint = 1300
```




### Tricopters

  
### Quadcopter


### Hexacopters


### Various multirotors


### Fixed wing
