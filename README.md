# TripTracker

This application can track/log your business and non-business car trips, to ease for example administering your travel expenses if you are a consultant.
It runs on a Raspberry Pi and to add some coolness to it, it has a nice dashboard-like UI which especially works nice together with the official Raspberry Pi 7" touchscreen (like i used when developing this thing)
So if you are really handy you can put this thing in your car.

The current version works only with this UI, but there are plans to add some kind of 'headless' mode, so that it can be remotely operated (for example off a phone). 

## Prequisites

### Hardware
- Raspberry Pi 3 (would probably also work on other Pis or other platforms with run Python, but i haven't tested them)
- A GPS receiver (optional, you can also for example use your phone GPS)
- (Car)power cable
- [7" touchscreen](https://www.raspberrypi.org/blog/the-eagerly-awaited-raspberry-pi-display/)
- A case for the whole shebang (i used [this](https://thepihut.com/products/raspberry-pi-official-7-touchscreen-case) one, but feel free to use/make something else.


### Software
- Latest version of Raspbian installed and it should be configured to use the touchscreen
- Python 3.x (already installed in Raspbian)
- PIP
- [Kivy](https://kivy.org/docs/installation/installation-rpi.html) (i used the 0.92-dev version which is at the time of writing the latest version, but any version greater or equal then 0.91 should do)
- [GPSD](http://www.catb.org/gpsd/)


## Installation
- Clone this repository to some directory on your rpi (called `$INSTALLDIR` from here on)
- `cd` into `$INSTALLDIR`
- Execute `sudo pip install -r requirements.txt` to install the remaining required libraries (Kivy should already be installed)
- Done!

## Running the application
- Connect your GPS receiver to the Rpi or enable your phone GPS (make sure GPSD is configured correctly)
- `cd` into `$INSTALLDIR`
- Run `python3 triptracker.py` and the main screen should appear after a while.
