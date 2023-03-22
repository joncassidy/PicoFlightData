import os
if not(hasattr(os,'name')): # Pico
    import connection
    ip = connection.connect()
    
import urequests as requests
import time
import math
import machine
from picographics import PicoGraphics, DISPLAY_INKY_PACK
# To Do
# Allow for long and lat being different kms
# Show message when connecting to network
# Maybe status dot on display when waiting for HTTP response
# Full text of aircraft type / origin / destination?
# Multiple locations. Click buttin to scrill through (and show name for a second on each scroll)

class Flight:
    def __init__(self, flight_id, info):
        self.id = flight_id
        self.id = flight_id
        self.icao_24bit = info[0]
        self.latitude = info[1]
        self.longitude = info[2]
        self.heading = info[3]
        self.altitude = info[4]
        self.ground_speed = info[5]
        self.squawk = info[6]
        self.aircraft_code = info[8]
        self.registration = info[9]
        self.time = info[10]
        self.origin_airport_iata = info[11]
        self.destination_airport_iata = info[12]
        self.number = info[13]
        self.airline_iata = info[13][:2]
        self.on_ground = info[14]
        self.vertical_speed = info[15]
        self.callsign = info[16]
        self.airline_icao = info[18]
        # using lat=log for the moment
        self.distanceSq = (((self.latitude - piLocation['lat'])**2) + (self.longitude - piLocation['long'])**2)
        
def setup():
    global button_a, button_b, button_c, piLocation, graphics

    button_a = machine.Pin(12, machine.Pin.IN, pull=machine.Pin.PULL_UP)
    button_b = machine.Pin(13, machine.Pin.IN, pull=machine.Pin.PULL_UP)
    button_c = machine.Pin(14, machine.Pin.IN, pull=machine.Pin.PULL_UP)

    button_a.irq(trigger=machine.Pin.IRQ_FALLING, handler=buttonPressed)
    button_b.irq(trigger=machine.Pin.IRQ_FALLING, handler=buttonPressed)
    button_c.irq(trigger=machine.Pin.IRQ_FALLING, handler=buttonPressed)

    piLocation = {"lat":51.46549,"long":-0.2986}
    graphics = PicoGraphics(DISPLAY_INKY_PACK)
    graphics.set_update_speed(3)
    graphics.set_font("bitmap8")

def buttonPressed(pin):
    global button_a, button_b, button_c
    if pin == button_a:
        print("a")
        graphics.set_pen(15) # black
        graphics.pixel(295,127)    
    if pin == button_b:
        graphics.set_pen(0) # white
        graphics.pixel(295,127)    
    if pin == button_c:
        graphics.clear()
    graphics.update()
    
def getNearestFlight():
    width = 0.1 # 0.1
    height = 0.1 #0.1
    url = "https://data-cloud.flightradar24.com/zones/fcgi/feed.js?"
    params = {"maxage":144000,"limit":50}
    params['bounds'] = "{}%2C{}%2C{}%2C{}".format(piLocation['lat']+height, piLocation['lat']-height , piLocation['long']-width,piLocation['long']+width)
    url += "&".join(["{}={}".format(k, v) for k, v in params.items()])
    headers = {'accept-encoding': '',
               'user-agent': 'Dummy',
               'accept': 'application/json'}
    response  = requests.get(url, headers=headers)
    flightsData = response.json()
    response.close()
    flights = [Flight(flight_id, info) for flight_id, info in flightsData.items()  if flight_id[0] in '01234567890']
    flights.sort(key=lambda x: x.distanceSq)
    return flights[0]

    
def writeFlight(flight):
    white = 15
    black=0
    if f1 == None:
        print ("No nearby flights")
        graphics.text("No nearby Flights", 0, 0, scale=2)
        return
    print(f1.origin_airport_iata, f1.destination_airport_iata, f1.altitude,"m", f1.number, f1.aircraft_code )
    graphics.set_pen(white)
    graphics.clear()
    graphics.clear()
    graphics.set_pen(black)
    graphics.text(flight.number,                   5, 5, scale=4)
    graphics.text(flight.origin_airport_iata+"-"+flight.destination_airport_iata,      160, 5, scale=4)
    graphics.text(str(flight.altitude)+"m",        5, 55, scale=3)
    #graphics.text("ETA"+str(flight.time),                 100, 100, scale=3)
    graphics.text(str(flight.ground_speed)+" kts", 200, 55, scale=3)
    graphics.text(str(flight.aircraft_code),       5, 95, scale=3)
    graphics.text(str(flight.registration),        98, 95, scale=3)
    
    graphics.rectangle(0, 40, 296, 5)
    graphics.rectangle(140, 0, 5, 40)
    graphics.line(0, 85, 296, 85)
    graphics.line(90, 45, 90, 128)
    graphics.line(190, 45, 190, 128)

    graphics.update()
    
setup()
while True:
    f1 = getNearestFlight()
    writeFlight(f1)
    time.sleep(1)
