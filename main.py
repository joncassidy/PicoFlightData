import urequests as requests
import time
import math
import network
from config import *
from picographics import PicoGraphics, DISPLAY_INKY_PACK

def connect():
    wlan = network.WLAN(network.STA_IF)
    connectingMessage = "Connecting "
    if wlan.isconnected() == False:
        wlan.active(True)
        wlan.connect(SSID, PASSWORD)
        while wlan.isconnected() == False:
            graphics.set_pen(white)
            graphics.clear()
            graphics.set_pen(black)
            graphics.text(connectingMessage, 5,5, wordwrap=290, scale=4)
            graphics.update()
            connectingMessage += ". "
            time.sleep(1)

class Flight:
    def __init__(self, flight_id, info):
        self.id = flight_id
        self.icao_24bit = info[0]
        self.latitude = info[1]
        self.longitude = info[2]
        self.heading = info[3]
        self.altitude = str(info[4])+" m"
        self.ground_speed = str(info[5])+" kts"
        self.squawk = info[6]
        self.aircraft_code = info[8]
        self.registration = info[9]
        self.time = info[10]
        self.origin_airport_iata = info[11]
        self.destination_airport_iata = info[12]
        self.routeText = self.origin_airport_iata+"-"+self.destination_airport_iata
        self.number = info[13]
        self.airline_iata = info[13][:2]
        self.on_ground = info[14]
        self.vertical_speed = info[15]
        self.callsign = info[16]
        self.airline_icao = info[18]
        # Only use distance to find nearest, so squared is enough. Need to correct for longitude degrees being different distances
        self.distanceSq = (((self.latitude - piLocation['lat'])**2) + ((self.longitude - piLocation['long'])*longLatRatio)**2)
        
def setup():
    global graphics, longLatRatio, black, white, piLocation
    graphics = PicoGraphics(DISPLAY_INKY_PACK)
    graphics.set_update_speed(3)
    graphics.set_font("bitmap8")
    white = 15
    black=0
    connect()
    try:
        locationURL = 'http://ip-api.com/json/'
        myLocationResponse = requests.get(locationURL)
        myLocation = myLocationResponse.json()
        piLocation = {'lat':myLocation['lat'], 'long':myLocation['lon']}
    except:
        # Will fallback to config file
        pass
    longLatRatio = math.cos(math.radians(piLocation['lat']))
    
  
def getNearestFlight():
    # Returns a single Flight object which is closest to the current location
    url = "https://data-cloud.flightradar24.com/zones/fcgi/feed.js?"
    params = {"maxage":144000,"limit":NUM_FLIGHTS}
    params['bounds'] = "{}%2C{}%2C{}%2C{}".format(piLocation['lat']+boxHeight, piLocation['lat']-boxHeight , piLocation['long']-boxWidth,piLocation['long']+boxWidth)
    url += "&".join(["{}={}".format(k, v) for k, v in params.items()])
    headers = {'accept-encoding': '',
               'user-agent': 'Dummy',
               'accept': 'application/json'}
    response  = requests.get(url, headers=headers)
    flightsData = response.json()
    response.close()
    flights = [Flight(flight_id, info) for flight_id, info in flightsData.items()  if flight_id[0] in '01234567890']
    flights.sort(key=lambda x: x.distanceSq)
    if len(flights)>0:
        return flights[0]
    
def writeFlight(flight):
    row1, row2, row3 = 5,55,95
    col1,col2 = 5,150
    graphics.set_pen(white)
    graphics.clear()
    
    graphics.set_pen(black)
    if flight == None:
        graphics.text("No nearby Flights", 0, 0, scale=2)
        return
    
    graphics.text(flight.number,       col1, row1, scale=4)
    graphics.text(flight.routeText,    col2, row1, scale=4)
    graphics.text(flight.registration, col1, row2, scale=3)
    graphics.text(flight.altitude,     col2, row2, scale=3)
    graphics.text(flight.aircraft_code,col1, row3, scale=3)
    graphics.text(flight.ground_speed, col2, row3, scale=3)

    # Draw boxes
    graphics.rectangle(0, 40, 296, 5)
    graphics.rectangle(140, 0, 5, 40)
    graphics.line(0, 85, 296, 85)
    graphics.line(142, 45, 142, 128)

    graphics.update()
    
setup()
while True:
    try:
        f1 = getNearestFlight()
        writeFlight(f1)
        time.sleep(1)
    except Exception as e:
        print(e)