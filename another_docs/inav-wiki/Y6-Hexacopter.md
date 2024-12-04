Name of frame: Y6 Hexacopter (own design, see here) http://www.hobbyking.com/hobbyking/forum/forum_posts.asp?TID=69766

Size of Frame: 573.9 mm in diameter

Total weight including battery, sonar, video-TX, GPS and 3-axis gimbal :  1583g

Total Thrust: 786g*6, Turnigy Mutistar 2216 800kv, carbon fiber props 10*4,5

Battery: Turnigy Multistar 3S 5200mAh

Mixer : mixer CUSTOM

mmix reset

mmix 0 1.0 0.0 1.333333 1.0     # REAR

mmix 1 1.0 -1.0 -0.666667 -1.0  # RIGHT

mmix 2 1.0 1.0 -0.666667 -1.0   # LEFT

mmix 3 1.0 0.0 1.333333 -1.0    # UNDER_REAR

mmix 4 1.0 -1.0 -0.666667 1.0   # UNDER_RIGHT

mmix 5 1.0 1.0 -0.666667 1.0   # UNDER_LEFT

iNav Version: 1.01 (e78054b)

set pid_controller = MWREWRITE

set p_pitch = 40

set i_pitch = 30

set d_pitch = 23

set p_roll = 40

set i_roll = 30

set d_roll = 23

set p_yaw = 85

set i_yaw = 45

set d_yaw = 0

set p_pitchf =  1.400

set i_pitchf =  0.300

set d_pitchf =  0.020

set p_rollf =  1.400

set i_rollf =  0.300

set d_rollf =  0.020

set p_yawf =  3.500

set i_yawf =  0.400

set d_yawf =  0.010

set level_horizon =  4.000

set level_angle =  4.000

set sensitivity_horizon = 75

set p_level = 20

set i_level = 20

set d_level = 100

