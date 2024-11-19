### Description of PIFF controller:

Link to [inavflight article](http://inavflight.com/news/pages/2017/02/14/PIFF-controller.html)

The FF-gain should do most of the work steering the airplane, leaving only P and I controller to fight turbulence and drift.  

**1: Figure out the maximum rates your airplane can do, both for rolling, loops and yaw turn**

* Fly in `MANUAL` mode (called `PASSTHROUGH` mode up to version 1.8.1) with the `manual_roll_rate`, `manual_pitch_rate` and `manual_yaw_rate` settings set to 100%, have some way of recording the flight, blackbox, video camera or both. Do hard roll, hard loops and one 360deg yaw turn. ( Use full stick on all )

* Note down the maximum rates, typical 360deg/s on roll, 100deg/s on pitch and 60deg/s yaw.  
Enter these values as your rates in configurator.  

**2: Zero out P and I gain on Roll, Pitch and YAW controller. Increase FF-gain (D column in the PID tuning tab) until you get 90% of full servo throw when having sticks at full throw when in `ACRO` mode (no flight mode enabled).**

* This is so the FF-gain does most of the work turning the airplane, but leaving some for the P and I gain to work with.
* For this step it is convenient to have the two modes `MANUAL` (called `PASSTHROUGH` mode up to version 1.8.1) and `ACRO` available on a switch to be able to switch easily between the two to compare the throws.

Now set a little P and I gain as a starting point for example 10 P-gain and 15 I-gain to Roll, Pitch and Yaw axis.

**3: Go out and fly in acro mode.**

* If airplane drifts to one side or up and down add I-gain to the axis it drifts in.
* If you want more stabilization against wind try and add more P-gain.

**4: Want to calm your airplane down? Now is the time to reduce rates to fit your needs.**

* Note: Yes it`s normal to get reduced servo throw when reducing rates at this point, if you got full servo throw at this stages you would overshoot the target deg/s you wanted.

**5: Tune Angle / Horizon mode**

* Enter `Angle` mode, if aircraft doesn't fly straight and level, you need to trim you board alignment.
* If you are unhappy with the value of maximum bank angle / pitch angle, adjust them in CLI, max_angle_inclination_rll and max_angle_inclination_pit. (Be aware of you want the same amount of maximum angle for poshold / althold you will also need to increase their values in [CLI](https://github.com/iNavFlight/inav/blob/master/docs/Cli.md))
* If you are unhappy with the strength of the Angle mode, example it yerks itself to quick up to level, adjust P-gain of the level controller.

### Other tuning tips:

* Setup your TPA correctly. [PID Attenuation and scaling](https://github.com/iNavFlight/inav/wiki/PID-Attenuation-and-scaling)

* If your plane over corrects when RTH is engaged, try increasing ``nav_fw_pos_xy_p`` and/or increasing ``nav_fw_pos_xy_i``. Good values to start: "set nav_fw_pos_xy_p = 50"; "set nav_fw_pos_xy_i = 5". Also you can lower "nav_fw_pos_xy_d". The behaviour of the plane is very different with or w/o wind, so it is necessary to test and tweak parameters in both scenarios.