# List of all flight modes in iNav


The default flight mode is [`RATE`](/iNavFlight/inav/wiki/Modes#default-flight-mode--no-mode-selected-) (also sometimes called ACRO), this is activated when none of the `actual flight modes` are turned on.

`Actual flight modes`

|  Mode name | Description |
|  ------ | ------ |
|  [`ANGLE`](/iNavFlight/inav/wiki/Modes#angle) | Stabilized mode with self leveling and restricted banking angles |
|  [`HORIZON`](/iNavFlight/inav/wiki/Modes#horizon)  | Stabilized mode with self leveling but without restricted banking angles |
|  [`NAV POSHOLD`](/iNavFlight/inav/wiki/Navigation-modes#poshold---horizontal-position-hold) | Used to hold position in 2d space with GPS. Combine with ALTHOLD to get 3d position lock |
|  [`NAV RTH`](/iNavFlight/inav/wiki/Navigation-modes#rth---return-to-home) | Used for Return-to-home. Does not need any other mode selected. |
|  [`NAV WP`](/iNavFlight/inav/wiki/Navigation-modes#wp---autonomous-waypoint-mission) | Used to fly WAYPOINT mission. Does not need any other mode selected. |
|  [`MANUAL`](/iNavFlight/inav/wiki/Modes#manual) | Used with fixed-wings to control everything manually. ( Direct servo control ). Was called `PASSTHROUGH` mode up to version 1.8.1 |

`Flight modes that alter behavior in combination with one of the above`


|  Mode name | Description |
|  ------ | ------ |
|  [`NAV ALTHOLD`](/iNavFlight/inav/wiki/Navigation-modes#althold---altitude-hold) | Used to hold altitude. recommend to use in combination with `angle` mode or `nav poshold` |
|  [`TURN ASSIST`](/iNavFlight/inav/wiki/Modes#turn-assist)  | Makes copter do Yaw turns on parallel to the ground plane regardless of tilt. |
|  [`AIR MODE`](/iNavFlight/inav/wiki/Modes#air-mode) | Keeps PID controller active at zero throttle |
|  [`SURFACE`](/iNavFlight/inav/wiki/Modes#surface) | Used to follow terrain, needs a rangefinder ( example sonar ). Not implemented properly and should not be used. |
|  [`HEADING HOLD`](/iNavFlight/inav/wiki/Modes#heading-hold) | Holds current heading using yaw rotation (rudder). Can be used with and without compass. |
|  [`HEADFREE`](/iNavFlight/inav/wiki/Modes#headfree) | Head Free - When enabled yaw has no effect on pitch/roll inputs |
|  [`HEADADJ`](/iNavFlight/inav/wiki/Modes#headadj) | Heading Adjust - Sets a new yaw origin for HEADFREE mode |


`Modes that can be enabled to activate function or other features.`

|  Mode name | Description |
|  ------ | ------ |
|  [`ARM`](/iNavFlight/inav/wiki/Modes#arm) | Used to switch arm aircraft |
|  [`CAMSTAB`](/iNavFlight/inav/wiki/Modes#CAMSTAB) | CAMera STABilisation. Used to stabilize SERVO GIMBAL outputs |
|  [`BEEPER`](/iNavFlight/inav/wiki/Modes#BEEPER) | Used to activate beeper |
|  [`LEDLOW`](/iNavFlight/inav/wiki/Modes#ledlow) | Turns LEDs OFF|
|  [`OSD SW`](/iNavFlight/inav/wiki/Modes#osd-sw) | Turns on and off OSD overlay |
|  [`TELEMETRY`](/iNavFlight/inav/wiki/Modes#telemetry) | Normally telemetry is always enabled, using this mode allows you to turn telemetry on and off at will |
|  [`BLACKBOX`](/iNavFlight/inav/blob/master/docs/Blackbox.md) | Normally blackbox is logging as soon as you arm, using this mode blackbox will only log flight data when the mode is active. ) |
|  [`FAILSAFE`](/iNavFlight/inav/wiki/Modes#failsafe) | Used to manually initate FAILSAFE |
|  [`HOME RESET`](/iNavFlight/inav/wiki/Navigation-modes) | Used to set a new home position at the current aircraft position. |
|  [`GCS NAV`](/iNavFlight/inav/wiki/Navigation-modes) | Used to allow ground station to control aircraft to do stuff like `Follow me` |
|  [`FLAPERON`](/iNavFlight/inav/wiki/Modes#flaperon) | Used to activate flaperons on fixed-wing aircraft. |
|  [`NAV LAUNCH`](/iNavFlight/inav/wiki/Modes#nav-launch) | Used to detect and automatic launch fixed-wing aircraft. |
|  [`SERVO AUTOTRIM`](/iNavFlight/inav/wiki/Modes#servo-autotrim) | Used to trim midpoint for servos to maintain straight flight |
|  [`AUTOTUNE`](/iNavFlight/inav/wiki/Modes#autotune) | Automatically tune fixed-wing PIFF gains. |
