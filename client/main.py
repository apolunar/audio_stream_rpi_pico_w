"""
Micropython client for the RPi Pico W
"""

import websocket
from machine import ADC
import network
import socket

SSID = "MusicStream"
PASSWORD = "I<3Music"

def connect_to_ap() -> str:
  """
  Sets up the access point and returns the IP address of the access point
  """
  # Connect to WiFi network
  sta_if = network.WLAN(network.STA_IF)
  sta_if.active(True)
  sta_if.connect(SSID, PASSWORD)

  # Wait for connection to be established
  while not sta_if.isconnected():
    print("Waiting for connection to be established...", end="\r")
  print("Connection established!")

  # Get default gateway IP address
  gateway_ip = socket.getaddrinfo('0.0.0.0', 0)[0][-1][0]

  print("Connected to network with IP address:", sta_if.ifconfig()[0])
  print("Default gateway IP address:", gateway_ip)

  return gateway_ip

gateway_ip = connect_to_ap()

# Set up ADC on pin 26
adc = ADC(26)

# Connect to websockets server
ws = websocket.WebSocket()
ws.connect("ws://" + gateway_ip + ":5000")

conversion_factor = 3.3/(4096)

# Continuously read audio from ADC and send to server
# Thanks to https://stackoverflow.com/questions/72018811/use-microphone-in-raspberry-pi-pico-micropython
# Try microphone https://www.adafruit.com/product/1713
while True:
  audio = adc.read_u16() * conversion_factor
  ws.send(audio)
