# Forewords

There are two outputs that can be used, in this guide we will name them `SERVO 0` and `SERVO 1`

`SERVO 0` is intended to be used on PITCH-axis when used in combination with `CAMSTAB`  
`SERVO 1` is intended to be used on ROLL-axis when used in combination with `CAMSTAB`  
`SERVO 1` can also be used to command YAW-axis, but use without `CAMSTAB` enabled.  

`CAMSTAB` Mode is a mode that will use accelerometer data from flight controller and stabilize these outputs so movement of the aircraft itself get canceled out.


There are mainly two scenarios for using `SERVO GIMBAL` feature.


1: Using an actuall gimbal like  [this](http://www.banggood.com/Upgrade-Debugging-Edition-JIYI-FPV-G3-3D-3-Axis-Gimbal-For-Gopro-Hero3-3-Hero4-Aerial-Photography-p-1031482.html?rmmds=search), with the purpose of just having manual controll over the gimbal movement.

2: Controlling an gimbal like device like [this](https://www.youtube.com/watch?v=Py_RLdZwAlc&t=81s), which don't have any external gimbal control board. This will enable PITCH and ROLL controll and you can optinally enable `CAMSTAB` mode so the flight controller acts as an gimbal controller and stabilize the camera. If you want to sacrifise the ROLL-axis to control an servo controlling YAW-axis you need to disable `CAMSTAB`.

## Warning

On some boards (SP Racing F3 for example) servo connectors might not be 5V tolerant, while gimbal controller might be using INPUT_PULLUP 5V in Roll/Pitch inputs. This might damage flight controller.  
  
  

##  Difference between flight controller boards and mixer used.

Because boards are different, the pinout may be different. It also depends on what Mixer is being used.  
Also be aware that on some boards when using `SERVO GIMBAL` feature motor outputs can get moved to new outputs.  
See map below:  

| Board              | Mixer       | SERVO 0 Output pin | SERVO 1 Output pin | Motor / Servo Output |
|--------------------|:-----------:|:------------------:|:------------------:|:--------------------:|
| NAZE               | QuadX       | Output Pin 1       | Output Pin 2       | Output 3-6           |
| SP RACING F3       | QuadX       | Output Pin 7       | Output Pin 8       | Output 1-4           |
| SP RACING F3       | QuadX       | Output Pin 7       | Output Pin 8       | Output 1-4           |
| SP RACING F3       | Flying wing | Output Pin 5       | Output Pin 6       | Output 1-4           |
| SP RACING F3       | Airplane    | Output Pin 7       | Output Pin 8       | Output 1-6           |


### Servo Tilt usage

1. Connect wires up according to your flightcontroller.  
1. Enable `SERVO GIMBAL` feature.  
1. Enable `CAMSTAB` mode if you want to stabilize it. ( Don't use this if you have an actuall gimbal controller )  
1. Tune Servo MID, MIN and MAX to match your servo / gimbal so it centered and does not exceed mechanical limits.  
1. If the servo / gimbal moves incorrectly change direction on the `SERVO` tab to negativ number instead of positive.  
1. To control the servo / gimbal using a free AUX channel enter `SERVO` tab and assign an free AUX to servo 0 (Pitch) and servo 1 (Roll).  

  
Example of AUX 4 controlling Servo 0 ( Pitch ), and AUX 5 controlling Servo 1 ( Roll )
![Example of AUX 4 controlling Servo 0 ( Pitch ), and AUX 5 controlling Servo 1 ( Roll )](https://quadmeup.com/wp-content/uploads/2017/01/2017_01_12-10_46AM.png)

To verify your configuration is working you can enter the `Motors` tab of the configurator, here you should see Servo 1 and Servo 2 output changing. Both as `CAMSTAB` doing its stabilitation and controlling it with an AUX channel. ( Yes its confusing, In motor tab the servo are listed Servo 1-8, while in Servo tab its listed 0-7. )
