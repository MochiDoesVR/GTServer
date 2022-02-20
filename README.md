
![amongus](https://raw.githubusercontent.com/MochiDoesVR/GTServer/15b3acd4749f3791b73be55ded98aa3307d5826e/GTServer_Banner.png)

## About
This is a simple Python script, which uses Bleak to communicate with a smartwatch via Bluetooth LE, and sends the heartrate monitor readings to VRChat over OSC. This script is very unfinished, and will likely require take some trial and error to get working!

## Tested Models:
Although this script has only been tested with one model, other similar smartwatches which rely on the Wearfit app (Eg. GT105, DT78) may work.
 - GT101 ([Amazon](https://www.amazon.com/dp/B09MY428RV/))

## Usage
**This script requires the latest VRChat Open Beta (As of 2/20/22), otherwise it won't work, as it relies on OSC support!**

To add heart rate monitoring support to your avatar using GTServer, add a new `float` parameter to your avatar, named `Heartrate`. This value is uncapped, so it'd be best to make any animator systems that make use of this range from 0-128 at least. At the time of writing this, the VRCSDK Build & Test function is broken, so you'll have to upload your avatar to test it. 

### Demo
[![Video](https://i.imgur.com/aP3oAs6.png)](https://streamable.com/yilo9h)

## Setup/Install
### Prerequisites
- A Bluetooth adapter that can do Bluetooth 4.0+ and BLE
- [Python 3.9+](https://www.python.org/downloads/release/python-390/) (Windows Store Version may work too!)
- [Bleak](https://pypi.org/project/bleak/)
- [Python-OSC](https://pypi.org/project/python-osc/)

### Setup
Grab a copy of the latest commit [here](https://github.com/MochiDoesVR/GTServer/archive/refs/heads/main.zip), and extract it somewhere. Open `main.py` in your text editor of choice, and change the zeros on the line `address = "00:00:00:00:00:00"` to match the Bluetooth MAC address of your watch, which can be found in one of it's menus, and optionally set your OSC IP Address & Port, if you changed them in your VRChat launch options. 

### Running
Open VRChat, run `start.bat`, and make sure your watch is powered on, not currently paired to any devices, and in range of your computer, otherwise the script will exit!

## Extras
- [Writeup](https://github.com/MochiDoesVR/GTServer/blob/main/WRITEUP.md)
- [My Website & Socials (I Guess?)](https://mochivr.me/)
