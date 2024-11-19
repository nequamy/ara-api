# Setting up Failsafe for RTH

## Foreword

The goal is to configure both your flight controller and radio receiver so that failsafe does as you expect in every situation.

For failsafe to work optimally iNav needs to know it's in a failsafe event and not just doing regular RTH. This is necessary for example to correctly handle loss of GPS while returning to home.

This assumes you have regular GPS modes like `RTH` working **already**.

## Configuration of receiver

You have two options on how to configure receiver.

### Option one

Set receiver to send out `NO PULSES` on a failsafe event.

### Option two

1. In `Modes` tab select a switch for "Failsafe"

1. Set your switches and sticks of your radio to the following conditions:

    -  `Throttle: approx. 0% (no throttle)`
    -  `Aileron: 50% (no input, stick center)`
    -  `Rudder: 50% (no input, stick center)`
    -  `Elevator: 50% (no input, stick center)`
    -  `Failsafe mode: activated`
    -  `Arm switch: Disarmed (If you use stick arming you can skip this)`

1. Configure failsafe on your receiver to the above conditions on link loss (consult manual for your receiver on how to do it)

## Configuration of iNav

Go to `Failsafe` tab, and enable `RTH` as Stage 2 failsafe.

For fixedwing set `failsafe_throttle_low_delay = 0` or else it will disarm fixedwing in air when Failsafe triggers  and you have had low throttle for the default time period.

The behavior of `RTH` can also be configured.

 - [iNav Flight modes / Navigation Modes](/iNavFlight/inav/wiki/Navigation-modes#rth-altitude-control-modes)

## Verifying that failsafe works as intended

Verify that your failsafe works without props:

1. Remove all props

1. Go outside, arm and apply throttle, run with it 50meter away from home (normally the place where you armed it) and then turn off transmitter. The aircraft should now try to climb (increase throttle). Also verify that you're able to regain control by turning on transmitter again, and move the ROLL/PITCH stick more than `failsafe_stick_threshold`.

Now, verify that failsafe works while in flight:

1. Put the props on again.

1. Take off, fly at least 50 meters from home, and turn off transmitter. Tip: Do this over soft grass. If it's an airplane it's better to have some altitude.

Note: If you are using a fixedwing without a magnetometer enabled you will need to run with the airplane before turning off the transmitter to test failsafe. This is because GPS speed needs to be above a certain threshold to acquire a valid heading. Without a valid heading failsafe will not initiated.

Note: To regain control after a failsafe event, you must move the roll/pitch sticks more than `failsafe_stick_threshold` in order to regain control.

**INAV offers additional failsafe safety features**

**failsafe_min_distance** and the action you wish to invoke (_failsafe_min_distance_procedure_)

****failsafe_throttle_low_delay**** (Time throttle level must have been closed  to Auto disarm)

The first setting could avoid injury as it will prevent the possibility of the craft blasting off to it's RTH height within you chosen safety distance of the set home point.It could also work against you if a failsafe event occurred while flying close in with a setting of (just land) and you were flying from a very small safe landing area. 
All options are available to best suite your needs.

The second setting could just ruin your day with a mid air disarm but conversely save you from personal injury if it is forgotten to disarm the craft
( not using motor stop also goes a long way to making the craft safer as the spinning propellers are a visible sign the craft is armed and dangerous)

Further reading and settable parameters are available here :-
https://github.com/iNavFlight/inav/blob/master/docs/Failsafe.md#failsafe_throttle

And here :-
https://github.com/iNavFlight/inav/blob/master/docs/Cli.md

