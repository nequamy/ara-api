Index:

- [AIR MODE](#air-mode)
- [ANGLE](#angle)
- [ARM](#arm)
- [BEEPER](#BEEPER)
- [BLACKBOX](#blackbox)
- [CAMSTAB](#CAMSTAB)
- [FAILSAFE](#failsafe)
- [FLAPERON](#flaperon)
- [HEADADJ](#headadj)
- [HEADFREE](#headfree)
- [HEADING HOLD](#heading-hold)
- [HORIZON](#horizon)
- [LEDLOW](#ledlow)
- [NAV LAUNCH](#nav-launch)
- [OSD SW](#osd-sw)
- [MANUAL](#manual) (called PASSTHROUGH mode up to version 1.8.1)
- [SERVO AUTOTRIM](#servo-autotrim)
- [SURFACE](#surface)
- [TELEMETRY](#telemetry)
- [TURN ASSIST](#turn-assist)
- [AUTOTUNE](#autotune)

## Default flight mode ( No mode selected )

The default flight mode does not self level the aircraft around the roll and the pitch axes. That is, the aircraft does not level on its own if you center the pitch and roll sticks on the radio. Rather, they work just like the yaw axis: the rate of rotation of each axis is controlled directly by the related stick on the radio, and by leaving them centered the flight controller will just try to keep the aircraft in whatever orientation it's in. This default mode is called "Rate" mode, also sometime called "Acro" (from "acrobatic") and is active whenever no auto-leveled mode is enabled.


## Mode details

### ALTHOLD

The altitude of the aircraft a the moment you activate this mode is fixed. 

### AIR MODE

In the standard mixer / mode, when the roll, pitch and yaw gets calculated and saturates a motor, all motors
will be reduced equally. When motor goes below minimum it gets clipped off.
Say you had your throttle just above minimum and tried to pull a quick roll - since two motors can't go
any lower, you essentially get half the power (half of your PID gain).
If your inputs would asked for more than 100% difference between the high and low motors, the low motors
would get clipped, breaking the symmetry of the motor balance by unevenly reducing the gain.
Airmode will enable full PID correction during zero throttle and give you ability for nice zero throttle
gliding and aerobatics. But also the cornering / turns will be much tighter now as there is always maximum
possible correction performed. Airmode can also be enabled to work at all times by always putting it on the
same switch like your arm switch or you can enable/disable it in air. Additional things and benefits: Airmode
will additionally fully enable Iterm at zero throttle. Note that there is still some protection on the ground
when throttle zeroed (below min_check) and roll/pitch sticks centered. This is a basic protection to limit
motors spooling up on the ground. Also the Iterm will be reset above 70% of stick input in acro mode to prevent
quick Iterm windups during finishes of rolls and flips, which will provide much cleaner and more natural stops
of flips and rolls what again opens the ability to have higher I gains for some.

### ANGLE

In this auto-leveled mode the roll and pitch channels control the angle between the relevant axis and the vertical, achieving leveled flight just by leaving the sticks centered.
Maximum banking angle is limited by `max_angle_inclination_rll` and `max_angle_inclination_pit`

### BLACKBOX

If you're recording to an onboard flash chip, you probably want to disable Blackbox recording when not required in order to save storage space. To do this, you can add a Blackbox flight mode to one of your AUX channels on the Configurator's modes tab. Once you've added a mode, Blackbox will only log flight data when the mode is active.

A log header will always be recorded at arming time, even if logging is paused. You can freely pause and resume logging while in flight.

See [`BLACKBOX`](/iNavFlight/inav/blob/master/docs/Blackbox.md) for more information

### FAILSAFE

Lets you activate flight controller failsafe with an aux channel.
Read [Failsafe page](https://github.com/iNavFlight/inav/wiki/Failsafe) for more info.

### FLAPERON

Activating it moves both ailerons down (or up) by predefined offset.

Configuration besides activating FLAPERON mode is pretty simple, and consists of just one CLI variable:
- `flaperon_throw_offset` defines throw range in us for both ailerons that will be applied when FLAPERON mode is activated. By default it 250 with max at 400.

Flaperon offset is by default is applied as a servo mixer input with ID=14 so using custom servo mixing you can configure FLAPERON mode to deflect any servos you need (including dedicated flaps).

### HEADADJ

It allows you to set a new yaw origin for HEADFREE mode.

### HEADFREE

In this mode, the "head" of the multicopter is always pointing to the same direction as when the feature was activated. This means that when the multicopter rotates around the Z axis (yaw), the controls will always respond according the same "head" direction.

With this mode it is easier to control the multicopter, even fly it with the physical head towards you since the controls always respond the same. This is a friendly mode to new users of multicopters and can prevent losing the control when you don't know the head direction. 

### HEADING HOLD

This flight mode affects only yaw axis and can be enabled together with any other flight mode. 
It helps to maintain current heading without pilots input and can be used with and without magnetometer support. When yaw stick is neutral position, Heading Hold mode tries to keep heading (azimuth if compass sensor is available) at a defined direction. When pilot moves yaw stick, Heading Hold is temporary disabled and is waiting for a new setpoint.

Heading hold only uses yaw control (rudder) so it won't work on a flying wing which has no rudder.

### HORIZON

This hybrid mode works exactly like the previous ANGLE mode with centered roll and pitch sticks (thus enabling auto-leveled flight), then gradually behaves more and more like the default RATE mode as the sticks are moved away from the center position. Which means it has no limitation on banking angle and can do flips.

### NAV LAUNCH
Airplane launch assistant

This flight mode is intended to provide assistance for launching the fixed-wing UAVs. Launch detection works by monitoring airplane acceleration - once it breaches the threshold for a certain amount of time launch sequence is started.

Gliders have different needs than motorized planes.  See below for note on glider launch setup.

The entire time `NAV LAUNCH` mode it will try and stabilize plane, it will target zero roll, zero yaw and predefined climb angle. The I-gain of the PIFF regulator is also disabled to prevent I-gain growing during launch until motor is started. When successful launch is detected it waits for preconfigured amount of time before starting motor.

`NAV LAUNCH` is automatically aborted after 5 seconds or by any pilot input on PITCH/ROLL stick. When it has aborted it goes to whichever selected mode, which can be Angle, Rate, Horizon, RTH or a waypoint mission (if no other mode is selected it will go to Rate mode).
 
It's safe to keep it activated the `NAV LAUNCH` mode during flight after the launch has being completed. Keep in mind that if you accidentally disarm while flying you need to disable `NAV LAUNCH` mode to being able to control the model again.

See iNav CLI for all available adjustable parameters, they start with `nav_fw_launch_`

Sequence for launching airplane using `NAV LAUNCH` mode looks like this:

1. Set switch to `NAV LAUNCH` mode prior to arming (note that it won't actually enable until arming)
1. ARM the plane. Motor should start spinning at min_throttle (if `MOTOR_STOP` is active, motor won't spin)
1. Put throttle stick to desired throttle value to be set **after** launch is finished. Motor should start spinning with  `nav_fw_launch_idle_thr`. Default is 1000 so it will respect `MOTOR_STOP` if active. Verify that motor don't respond to throttle stick motion.  Don't touch the pitch/roll stick!
1. Throw the airplane.  It must be thrown leveled, or thrown by slinging it by wingtip.
1. Motors will start at pre-configured `nav_fw_launch_thr` (default 1700) after `nav_fw_launch_motor_delay` (500ms)
1. Launch sequence will finish when pilot switch off the NAV LAUNCH mode or move the sticks.  

If it won't detect launch it's possible that you need to lower your threshold. Look at the CLI variables.

CAUTION: Motors will spin if you unset `NAV LAUNCH` mode after arming.

From version 1.9 `NAV LAUNCH` can be permanently enabled via the configurator or the CLI using `feature FW_LAUNCH` in this case `NAV LAUNCH` doesn't need to be enabled via a transmitter switch prior to arming.
If you want to launch the plane manually just move pitch/roll stick after you have armed the plane and you have back throttle control.
If you inadvertedly disarm mid-air before raising the throttle again (you should lower the throttle to arm again) move pitch/roll stick and you will have throttle control back.
  

**GLIDER / SLOPER SETUP**

For obtaining launch assistance for hand-thrown gliders, it's a bit tricky.  One possible solution is to setup the throttle as in input for switching modes.  At lowest throttle setting, disarm and enter passthru.  Just above minimal throttle, turn on Nav Launch, then just above that, Arm and activate Angle - all simultaneously "on" for launch.  

This will allow the FC to reset the launch sequence and be ready for toss with Angle activated after launch. 

Setup launch parameters appropriately:

`nav_fw_launch_climb_angle = XX 45?`

(Climb angle for launch sequence (degrees), is also restrained by global max_angle_inclination_pit)

`set nav_fw_launch_thr = 1700`

^^this command for a glider can be problematic.  Not obvious, since Airplanes change PID values for throttle based on `set tpa_rate = XXX` and `set tpa_breakpoint = XXXX`  (adjust accordingly).  Also, not well documented but PIDs are boosted at low throttles by 1.5X!!  Can cause unexplained behavior at launch.  For some gliders - having PID gains reduced for toss is beneficial (DLG launch may be fastest speed the glider travels)

`nav_fw_launch_velocity = XXX 300?` 

(Forward velocity threshold for swing-launch detection [cm/s])

One option is to add Horizon mode at very top end of throttle, to enable acro flying with ability to drop back to angle mode for emergency recovery.


### MANUAL
Direct servo control in fixed-wing. This mode was called PASSTHROUGH mode up to version 1.8.1.

In this mode there is no stabilization.

What FC does in PASSTHRU mode is: Motor mixing, Servo Mixing, Expo settings, Throws limiting (see the `manual_*_rate` settings). Note that Failsafe is still active in this mode and can override the controls.

### SERVO AUTOTRIM
In flight adjustment of servo midpoint for straight flight

The purpose of this mode is to set new midpoints for `SERVO_ELEVATOR`, `SERVO_FLAPERON_1`, `SERVO_FLAPERON_2` and `SERVO_RUDDER`.

This is so when switching into passthrough mode the plane will fly straight, its also to help the PIFF controller know where the plane is expected to fly straight.

How to use:

1. This is intended to use in air. 
2. Fly straight, choose what mode that suites you best. (`passthrough`, `angle` or `acro`)
3. Enable `SERVO AUTOTRIM` mode, and keep flying straight for 2 seconds. After 2 seconds it will set new midpoints based on average servo position during those 2 seconds.
4. If your are NOT happy with new midpoints disable `SERVO AUTOTRIM` mode and it will revert back to old settings. If you want to keep new midpoints keep `SERVO AUTOTRIM` turned on, land aircraft and disarm. New midpoints will be saved.

You may want to inspect your new midpoints after landing, if the servo offset is a lot you may alter your linkage mechanically and redo servo midpoint. 

This is not to be confused with tuning your aircraft for leveled flight in `ANGLE` mode, to do this you need to adjust your board alignment so straight flight for that aircraft is show the board being level ( 0 pitch and 0 roll ).

### AUTOTUNE

For detailed description go to https://github.com/iNavFlight/inav/blob/development/docs/Autotune%20-%20fixedwing.md

AUTOTUNE will attempt to tune roll and pitch P, I and FF gains on a fixed-wing airplane.

Autotune will monitor behavior of the airplane when you fly it and adjust P, I and FF gains to reach optimal performance.

How to use:

Fly in ANGLE mode. Enable AUTOTUNE mode. Do hard maneuvers on each axis separately. For roll - bank hard left/hard right. For pitch - fast climb, steep dive. Initially you probably will notice very soft response - make sure your flying field is big enough for slow turns.

The more maneuvers you will do - the better results AUTOTUNE will be able to reach.

AUTOTUNE will adjust gains constantly but it will take a snapshot of current gains every 5 seconds. When you disable AUTOTUNE gains from last snapshot will be restored. If you turn AUTOTUNE on and off before 5 seconds elapse - PIFF gains won't be changed.

Currently AUTOTUNE don't save gains to EEPROM - you have to save manually, using a [stick combo](https://github.com/iNavFlight/inav/blob/master/docs/Controls.md).

### TURN ASSIST

Normally YAW stick makes a turn around a vertical axis of the craft - this is why when you fly forward in RATE and do a 180-deg turn using only YAW you'll end up looking upwards and flying backwards. In ANGLE mode this also causes an effect known as a pirouetting where turn is not smooth the horizon line is not maintained.

In RATE mode pilot compensated for this effect by using both ROLL and YAW sticks to coordinate the rotation and keep attitude (horizon line).

TURN ASSISTANT mode calculates this additional ROLL command required to maintain a coordinated YAW turn effectively making YAW stick turn the aircraft around vertical axis relative to the ground.

In RATE mode it allows one to makes a perfect yaw-stick only turn without changing attitude of the machine. There might be slight drift due to not instant response of PID control, but still much easier to pilot for a RATE-mode beginners.

In ANGLE mode it also makes yaw turns smoother and completely pirouette-less. This is because TURN ASSIST introduces feed-forward control in pitch/roll and maintains attitude naturally and without delay.

From INAV 1.7 turn assist will work one planes, copy paste from pull request:

This extends TURN_ASSIST flight mode on airplanes - when doing a turn on an airplane it will calculate required yaw and pitch rate to keep airplane pointed at horizon.

TAS (from airspeed sensor) will be used for calculation if available - otherwise code will use cruise airspeed defined by fw_reference_airspeed.

## AUXILIARY CONFIGURATION

Spare auxiliary receiver channels can be used to enable/disable modes.  Some modes can only be enabled this way.

Configure your transmitter so that switches or dials (potentiometers) send channel data on channels 5 and upwards (the first 4 channels are usually occupied by the throttle, aileron, rudder, and elevator channels).

_e.g. You can configure a 3 position switch to send 1000 when the switch is low, 1500 when the switch is in the middle and 2000 when the switch is high._

Configure your TX/RX channel limits to use values between 1000 and 2000.  The range used by mode ranges is fixed to 900 to 2100.

When a channel is within a specified range the corresponding mode is enabled.

Use the GUI configuration tool to allow easy configuration when channel.

### CLI 

There is a CLI command, `aux` that allows auxiliary configuration.  It takes 5 arguments as follows:

* AUD range slot number (0 - 39)
* mode id (see mode list above)
* AUX channel index (AUX1 = 0, AUX2 = 1,... etc)
* low position, from 900 to 2100. Should be a multiple of 25.
* high position, from 900 to 2100. Should be a multiple of 25.

If the low and high position are the same then the values are ignored.

e.g.

Configure AUX range slot 0 to enable ARM when AUX1 is within 1700 and 2100.
 
```
aux 0 0 0 1700 2100
```

You can display the AUX configuration by using the `aux` command with no arguments.