## 0. Setup hardware
Balance props and motors, install FC on a vibration-damping mount if possible.

## 1. Getting your flight controller ready.

* Flash newest iNav
* Do the advanced 6-point [sensor calibration](https://github.com/iNavFlight/inav/wiki/Sensor-calibration).
* Select your Mixer. iNav has removed a lot of mixes and requires custom mix for exotic setups, see [Custom mixes for exotic setups](https://github.com/iNavFlight/inav/wiki/Custom-mixes-for-exotic-setups#setups-that-can-be-implemented-with-custom-mixer)


## 2. Set your TX midpoints
Set trim on your TX to zero. Use subtrim to adjust your TX midpoints to be precisely 1500 when Roll/Pitch/Yaw sticks are centered. You can check the input values in the Receiver tab in cleanflight/iNav configurator.

## 3. Tune your copter's Pitch/Roll/Yaw/Level PIDs and other values

[Default values for different type of aircrafts](https://github.com/iNavFlight/inav/wiki/Default-values-for-different-type-of-aircrafts)

**THIS IS IMPORTANT.** Stock values does not fly good on example and 250 racing quad.

## 4. Trim copter to level flight
DO NOT USE TRIM on your Transmitter to stop your copter drifting. Use board alignment settings or accelerometer trim stick combos.
[How to trim your Accelerometer](http://tldrify.com/elw)

## 5. Setup and verify failsafe on TX and iNav
[Guide for setting up failsafe](https://github.com/iNavFlight/inav/wiki/Failsafe#setting-up-failsafe-with-return-to-home)

## 6. Determine and set hover throttle
Use blackbox or Configurator to figure out throttle stick position when your copter is hovering. Set **nav_mc_hover_thr** CLI variable to that value.
You can also tune this without blackbox. If your copter jumps/rises when you activate altitude hold, reduce your nav_mc_hover_thr setting by 100 or so. If your copter falls, increase it by 100, fine tune until there is no jump or fall when activating altitude hold.


## 7. Get to know the CLI values.
iNav offers a lot of customization through CLI variables. Its strongly recommended to read through [iNav CLI variables](https://github.com/iNavFlight/inav/wiki/iNav-CLI-variables)

Some important ones are:

**nav_user_control_mode** Defines how Pitch/Roll input from RC receiver affects flight in POSHOLD mode: ATTI - right stick controls attitude like in ANGLE mode; CRUISE - right stick controls velocity in forward and right direction.

//TODO Explain gyro_lpf