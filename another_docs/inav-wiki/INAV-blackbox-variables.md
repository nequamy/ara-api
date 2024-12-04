# Overview

Blackbox is a valuable tool for analyzing the flight dynamics of our airborne vehicles and as such it can be useful for troubleshooting and debugging purposes.

In INAV we use a set of specific variables, each variable may contain multiple arrays, for example - navPos[0-2]. 

**navPos**, **navVel**, **navTgtPos** and **navTgtVel** each hold arrays [0-2], which represent distances due North [0], due East [1] and straight Up [2], all relative to the "point of origin".
North and East are fused from accelerometer and GPS data, while Up is fused from accelerometer + barometer for multicopters and accelerometer + gps for airplanes if no barometer is available. Read the [[Inertial position estimator|Inertial-position-estimator-(INAV)]] page for detailed explanation.

"Point of origin" might be different from "Home". "Home" is defined as position at the time of arming. While "Point of origin" is recorded after a valid GPS fix is aquired.

For further information about the coordinate system used please read the [[Coordinate systems|Coordinate-systems]] page.

#iNav Variables 

Variables listed below with a short description of each:

*  **navMode** (**navState** in newer code):
current mode of operation from iNav's point of view. Might be different from flight mode. Meaning vary by version, but navMode=0 and navState=1 means idle.

* **navFlags**: 
binary flags of iNav internal state: new data availability for altitude, position and heading, validity of altitude, surface distance and position, flags to indicate if pilot is adjusting altitude and position via rc input.

* **navTgtPos**:
represents the desired position velocity as used/calculated by iNav. When you are in PH, navTgtPos will be set to hold position coordinates. 

* **navPos**:
array of latest NEU coordinates as provided by inertial estimator. Will be slightly different from GPS/baro readings for 99% of time. Units - cm. 

* **navVel**:
same as navPos, but for estimated velocity. Units - cm/s

* **navTgtVel**:
represents the desired velocity as used/calculated by iNav. When you are in PH, navTgtVel will be set to calculated desired velocity to reach the target position.

* **navDebug**: 
as the name suggests it is used for debugging. Meaning of these values differ all the time depending on what part of the code is currently being debugged.

Blackbox can log data either via serial port or into internal dataflash. In order to log the data into the internal flash at the moment is possible via CLI:  
set blackbox_device = SPIFLASH # instead of SERIAL  
set blackbox_rate_num = 1  
set blackbox_rate_denom = 2  
This will make it work and store every second value.

# iNav Logging Intervals

Blackbox logs several types of frames - flight behaviour is written using I- and P-frames. I-frames are fairly big and contain absolute values, P-frames are delta-encoded to save space. Blackbox denominator only reduces P-frame rate, the I-frame rate is constant.

Originally I-frames were logged every 32 iterations, P-frame is logged every blackbox_rate_denom after I-frame. This doesn't give you exactly 1 / blackbox_rate_denom rate, i.e. for 1/16 - 1/31 rates it's going to be c. 16 iterations between frames on average.

For iNav 1.6 and later, the I-frame interval is set dynamically at 1/32, 1/64, 1/128 and 1/256 based on the blackbox_rate_denom chosen.

For example, if a blackbox_rate_denom of 50 is used, INav will select 64 as the I-frame interval, meaning c. 1/32 actual logging rate.


