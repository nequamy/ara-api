# MultiWii NAV Protocol and Types

This document describes a number of values and enumerations for for **MultiWii** MSP messages. As **iNav** implements a part of this specification it is documented in the iNav wiki.

This information is provided in the hope it might be useful NO WARRANTY.

Note that all binary values are little endian (MSP standard).

# Implementation and versions

This document should match the iNav 1.2 (and later) and Multiwii 2.4 flight controller firmware. The messages described are implemented in mwp (Linux / FreeBSD) and ezgui (Android) ground station applications. mwp and ezgui support both iNav and Multiwii; WinGui is a Windows / Multiwii only mission planner that also supports this message set.

# WayPoint / Action Attributes

Each  waypoint has a type and takes a number of parameters, as below. These are used in the MSP_WP message. The final column indicated if the message is implemented for iNav 1.2.

| Value | Enum | P1 | P2 | P3 | Lat | Lon | Alt | iNav |
| ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- |
| 1 | WAYPOINT      | speed [1] | | | ✔ | ✔ | ✔ | ✔ |
| 2 | POSHOLD_UNLIM |          | | | ✔ | ✔ | ✔ | [5] |
| 3 | POSHOLD TIME  | Seconds | | | ✔ | ✔ | ✔ |    |
| 4 | RTH [4]       | Land | | |    |    | ✔ [2] | ✔ |
| 5 | SET POI       |          | | | ✔ | ✔ | | |
| 6 | JUMP          | WP#      | Repeat (-1 = forever) | | | | |  |
| 7 | SET HEAD [3]  | Heading  | | | | | | |
| 8 | LAND | | | | ✔ | ✔ | ✔ | |

1. Leg speed is an iNav extension
2. Not used by iNav
3. Once SET_HEAD is invoked, it remains active until cleared by a P1 value of -1.
4. If a mission contains multiple RTH stanzas, then for MultiWii, the mission terminates at the first RTH. For iNav, the mission will continue if LAND is not set, and valid waypoints follow.
5. If the final entry in a mission is a WP, the iNav treats it as POSHOLD_UNLIM.

## Uploading

For safety, if no mission is defined, a single RTH action should be sent.

| Enum | P1 | P2 | P3 | Lat | Lon | Alt | Flag |
| ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- |
| RTH | 0 | 0 | 0 | 0 | 0 | 25m [1] | 0xa5 |

1. your choice, really.

In general, flag is 0, unless it's the last point in a mission, in which case it is set to 0xa5. When waypoints are uploaded, the values are also returned by the FC, thus enabling the application to verify that the mission has been uploaded correctly.

## FC Capabilities (MW only)

Note that 32bit flight controllers (baseflight, cleanflight) use capability == 16 for a different purpose
(CAP_CHANNEL_FORWARDING). It is advised to use other messages for checking for capabilities on non-MW platforms.

| Capability | Value |
| ---- | ---- |
| BIND | 1 |
| DYNBAL | 4 |
| FLAP | 8 |
| NAV | 16 |

# Messages (Nav related)

| MNEMONIC | Value | Direction (relative to FC) |
| -------- | ---- | ---- |
| MSP_NAV_STATUS | 121 | Out |
| MSP_NAV_CONFIG | 122 | Out |
| MSP_WP | 118  | Out |
| MSP_RADIO | 199 | Out |
| MSP_SET_NAV_CONFIG | 215 | In |
| MSP_SET_HEAD | 211 | In |
| MSP_SET_WP | 209 | In (& out) |

# MSP_WP / MSP_SET_WP

Special waypoints are 0 and 255. 0 is the RTH (Home) position, 255 is the POSHOLD position (lat, lon, alt).

| Name | Type | Usage |
| ---- | ---- | ----- |
| wp_no | uchar | way point number |
| action | uchar | action (wp type / action) |
| lat | int32 | decimal degrees latitude * 10,000,000 |
| lon | int32 | decimal degrees longitude * 10,000,000 |
| altitude | int32 | altitude (metre) * 100 |
| p1 | int16 | varies according to action |
| p2 | int16 | varies according to action |
| p3 | int16 | varies according to action |
| flag | uchar | 0xa5 = last, otherwise set to 0 |

The values for the various parameters are given in the section “WayPoint / Action Attributes”
Note that altitude is measured from the "home" location, not absolute above mean sea level.

# MSP_NAV_STATUS

The following data are returned by a MSP_NAV_STATUS message. The texts are those defined by Wingui; multiwii and iNav support this message. Almost the same data is returned by the [iNav LTM NFRAME](https://github.com/iNavFlight/inav/wiki/Lightweight-Telemetry-(LTM)#navigation-frame-n)

<table>
<thead>
<tr class="header">
<th>Name</th>
<th>Type</th>
<th>Usage</th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td>gps_mode</td>
<td>uchar</td>
<td>None <br/>
PosHold <br/>
RTH <br/>
Mission</td>
</tr>
<tr class="even">
<td>nav_state</td>
<td>uchar</td>
<td>None <br/>
RTH Start <br/>
RTH Enroute <br/>
PosHold infinite<br/>
PosHold timed<br/>
WP Enroute <br/>
Process next <br/>
Jump <br/>
Start Land <br/>
Land in Progress <br/>
Landed <br/>
Settling before land <br/>
Start descent </td>
</tr>
<tr class="odd">
<td>action</td>
<td>uchar</td>
<td>(last wp, next wp?)</td>
</tr>
<tr class="even">
<td>wp_number</td>
<td>uchar</td>
<td>(last wp, next wp?)</td>
</tr>
<tr class="even">
<td>nav_error</td>
<td>uchar</td>
<td>Navigation system is working <br/>
Next waypoint distance is more than the safety limit, aborting mission <br/>
GPS reception is compromised - pausing mission, COPTER IS ADRIFT! <br/>
Error while reading next waypoint from memory, aborting mission. <br/>
Mission Finished. <br/>
Waiting for timed position hold. <br/>
Invalid Jump target detected, aborting mission. <br/>
Invalid Mission Step Action code detected, aborting mission. <br/>
Waiting to reach return to home altitude. <br/>
GPS fix lost, mission aborted - COPTER IS ADRIFT! <br/>
Copter is disarmed, navigation engine disabled. <br/>
Landing is in progress, check attitude if possible. </td>
</tr>
<tr class="odd">
<td>target_bearing</td>
<td>int16</td>
<td>(presumably to the next WP?)</td>
</tr>
</tbody>
</table>

# MSP_NAV_CONFIG (MW)

The following data are returned from a MSP_NAV_CONFIG message. Values are from multiwii config.h. Values may also be set by MSP_SET_NAV_CONFIG. 

<table>
<thead>
<tr class="header">
<th>Name</th>
<th>Type</th>
<th>Usage</th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td>flags1</td>
<td>uchar</td>
<td>
Bitmap of settings from MW config.h <br/>
b0 : GPS filtering <br/>
b1 : GPS Lead <br/>
b2 : Reset Home <br/>
b3 : Heading control <br/>
b4 : Tail first <br/>
b5 : RTH Head <br/>
b6 : Slow Nav <br/>
b7 : RTH Alt </td>
</tr>
<tr class="even">
<td>flags2</td>
<td>uchar</td>
<td>
Bitmap of settings from MW config.h <br/>
b0 : Disable sticks <br/>
b1 : Baro takeover</td>
</tr>
<tr class="odd">
<td>wp_radius</td>
<td>uint16</td>
<td>radius around which waypoint is reached (cm)</td>
<tr class="even">
<td>safe_wp_distance</td>
<td>uint16</td>
<td>Maximum permitted first leg of mission (m, assumed?)</td>
</tr>
<tr class="odd">
<td>nav_max_altitude</td>
<td>uint16</td>
<td>Maximum altitude for NAV (m)</td>
</tr>
<tr class="even">
<td>nav_speed_max</td>
<td>uint16</td>
<td>maximum speed for NAV (cm/sec)</td>
</tr>
<tr class="odd">
<td>nav_speed_min</td>
<td>uint16</td>
<td>minimum speed for NAV (cm/s)</td>
</tr>
<tr class="even">
<td>crosstrack_gain</td>
<td>uchar</td>
<td>MW config.h value*100</td>
</tr>
<tr class="odd">
<td>nav_bank_max</td>
<td>uint16</td>
<td>maximum bank ??? for NAV, MW config.h value*100</td>
</tr>
<tr class="even">
<td>rth_altitude</td>
<td>uint16</td>
<td>RTH altitude (m)</td>
</tr>
<tr class="odd">
<td>land_speed</td>
<td>uchar</td>
<td>Governs the descent speed during landing. 100 ~= 50 cm/sec unknown units</td>
</tr>
<tr class="even">
<td>fence</td>
<td>uint16</td>
<td>Distance beyond which forces RTH (m)</td>
</tr>
<tr class="odd">
<td>max_wp_number</td>
<td>uchar</td>
<td>maximum number of waypoints possible (read only)</td>
</tr>
</tbody>
</table>

# MSP_RADIO

If you have a 3DR radio with the MW/MSP specific firmware, the follow data are sent from the radio, unsolicited.

| Name | Type | Usage |
| ---- | ---- | ----- |
| rxerrors | uint16 | Number of RX errors |
| fixed_errors | uint16 | Number of fixed errors, if error correction is set |
| localrssi | uchar | Local RSSI |
| remrssi | uchar | Remote RSSI |
| txbuf  | uchar | Size of TX buffer |
| noise | uchar | Local noise |
| remnoise | uchar | Remote noise |

# Implementations

The MSP NAV message set is implemented by mwptools (Linux), ezgui (Android) and WinGUI (MS Windows).

# XML Mission Files

mwptools, ezgui (and WinGUI) share an XML mission file format. A [reverse engineered definition (XSD)](https://github.com/stronnag/mwptools/blob/master/samples/mw-mission.xsd) can be found in the mwp samples  directory.
