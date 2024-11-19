[YouTube Video showing the steps below](https://youtu.be/WN0UEmIJLX4)

1. Download and install [VirtualBox](https://www.virtualbox.org/)
1. Download [Arch-anywhere](https://arch-anywhere.org/download/) ISO.
1. Install Arch-anywhere in a new virtualbox
1. Reboot into your new Virtualbox
1. Install the requirred packages. By running this in terminal: sudo pacman -S git make gcc arm-none-eabi-gcc arm-none-eabi-newlib
1. Download a fresh copy of INAV by running this in terminal. git clone https://github.com/inavflight/inav)
1. Enter INAV folder and type make TARGET=TARGET_YOU_WANT_TO_MAKE

And heres a [link](https://github.com/iNavFlight/inav/blob/master/docs/Features%20safe%20to%20remove%20and%20add.md) that gives some hints how to tailor INAV for your needs.