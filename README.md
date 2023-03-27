# PicoFlightData
## Overview
A fairly simple program to use a Pi Pico and a Pimionri Inky display to show details of the nearest overhead plane in near real time.

Insipred by Colin Waddell's more substantial approach at https://blog.colinwaddell.com/flight-tracker/, this one is much smaller, simpler and cheaper (although not as good looking).

## Requirements
- A Raspberry Pi Pico W, with headers
- Pimoroni Inky pack (https://shop.pimoroni.com/products/pico-inky-pack)
- A WiFi connection
- Pimoroni picographics library (https://github.com/pimoroni/pimoroni-pico/blob/main/micropython/modules/picographics)

## Getting it running
I use Thonny, so instructions assume you have that installed
1. Plug the Inky display into the Pi Pico W
2. Install the right python version (Pimoroni • Inky Frame (with Pimoroni libraries)). (Click bottom right of the Thonny window -> Configure Interpreter -> Install or update MicroPython
3. Modify the config.py file and change the SSID and PASSWORD lines with your wifi SSID and password. This step is essential
6. Copy the main.py and config.py files to the root of the Pi in Thonny
7. You can now unplug the PC and connect any USB power source.

## Config
There is a config.py file. It's fairly simple, with the following parameters:
- SSID : The SSID of your wireless network
- PASSWORD : The password of your wireless network
- piLocation : A JSON format of the longitude and latitude to find the flights near. _**This is only used**_ if a longitude/latitude cannot be deduced from the Wifi connection.
- boxWidth : The East/West size of box to look for flights, in Degrees. I live near an airport, so a smaller number works. If you are not, make this bigger (but the whole thing is probably less interesting anyway)
- boxHeight : The North/South size of box to look for flights, in Degrees
- NUM_FLIGHTS : Maximum number of flights to request at a time. Should be more than the maximum number of flights in the box above at any time


## Notes / Comments
- The display shows the last thing it showed after the power is removed (or something else goes wrong). The altitude changing is the easiest way to see it is doing something
- The display does ghost a little. There are options to make that better, but at the expense of slower updates showing more of a flicker
- Sometimes mine has trouble connecting to Wifi, and I have to power cycle it (or press the reset button)
- Some aircraft have less data available (especially helicopters near me)



