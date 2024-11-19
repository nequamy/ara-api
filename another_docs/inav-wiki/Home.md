![](http://static.rcgroups.net/forums/attachments/6/1/0/3/7/6/a9088858-102-inav.png)

INAV is a fork of cleanflight with a heavy focus upon GPS features for both airplanes & multirotor models.

iNav is **being actively developed** and currently supports RTH (_Return To Home_) with a predefined climb height, position hold, [[waypoints|iNavFlight Missions]], "follow-me" and many more features. 

A wide variety of inexpensive flight controller boards are supported. While Naze32 & CC3D flight control boards are still work (*) with limited features, F3 & F4 flight control boards are **strongly suggested** to gain access to the full features of iNav & extended flight time abilities.

*F1 Flight controllers like Naze32 and CC3D is not supported anymore, previously released firmwares do still work of course. Latest release for F1 boards is INAV 1.7.3

iNav has many settings that are different than cleanflight, so while the configurator may look familiar to you, simply restoring settings from an older version of cleanflight won't work & the calibration process is very, very different.

**As such it is ABSOLUTELY mandatory to read these pages:**

- [Getting started with iNav](https://github.com/iNavFlight/inav/wiki/Getting-started-with-iNav)

- [Sensor calibration](https://github.com/iNavFlight/inav/wiki/Sensor-calibration)

- [Multirotor guide](https://github.com/iNavFlight/inav/wiki/Multirotor-guide) if you're going to use it in a multirotor.

- [Fixed wing guide](https://github.com/iNavFlight/inav/wiki/Fixed-wing-guide) if you're going to use it in a fixed wing model.

- [YouTube videos](https://github.com/iNavFlight/inav/wiki/YouTube-video-guides)

- Many flight controller boards are supported. See the [Supported boards](Supported-boards) page.

All configurator is done through [INAV Configurator](https://github.com/iNavFlight/inav-configurator/releases).

This Wiki is available in other languages: [Русский](https://github.com/iNavFlight/ru_wiki/wiki)

## Searching the wiki

The wiki can be search via Google (as least) as follows:

* In the search bar enter `site:github.com/iNavFlight/inav/wiki TOPIC` (where TOPIC is your search item), e.g.
* `site:github.com/iNavFlight/inav/wiki 3DR` for information on using 3DR radios with iNav
* `site:github.com/iNavFlight/inav/wiki mission planner` for information about iNav capable mission planners

The wider project (issues, pull requests) can be searched by omitting the `wiki` term, e.g.:

* `site:github.com/iNavFlight/inav softserial` 
