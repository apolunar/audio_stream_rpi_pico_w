"""
Micropython server for the RPi Pico W
Creates an access point and prints the IP address of the access point
"""

import network
import socket
import _thread
import base64

# Set up the access point (you have to connect to this network to access the webserver)
ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid='MusicStream', password='I<3Music')

ip_address= ap.ifconfig()[0]

# Print the IP address of the access point
print('Access point IP address:', ip_address)

# Set up the server socket (this is where we recieve audio data from the RPi Picos)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((ip_address, 5000))
server_socket.listen(1)

# Set up the web server socket (this is where we send HTML to display data from the RPi Picos)
webserver_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
webserver_socket.bind((ip_address, 80))
webserver_socket.listen(1)

# Set up the streaming server socket (this is where we stream audio data recieved on the server socket)
straming_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
straming_socket.bind((ip_address, 8080))
straming_socket.listen(1)

streaming_client = None

# This streams the audio to the ONE HTML consumer
def handle_streaming():
  global streaming_client

  while True:
    # Wait to accept new client connections; should only get connected to from the below HTML subscriber
    streaming_client, streaming_address = server_socket.accept()
    
    print('Streaming client connected:', streaming_address)

# Handle connections from clients to the WEB SERVER
def handle_webserver_client(webserver_client):
    # Tell the client we are working in HTTP
    webserver_client.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')

    # Give the client some basic HTML with an audio stream reciever (audio controls means volume control is included)
    webserver_client.send("<html><body><audio controls><source src='http://{}:8080' type='audio/wav'></audio></body></html>".format(ip_address))

# Only handles ONE connection
def handle_webserver():
  while True:
    # Accept new client connections
    webserver_client, webserver_address = webserver_socket.accept()
    
    print('Webserver client connected:', webserver_address)
    
    handle_webserver_client(webserver_client)

    # We don't have anymore HTML to send, instead the HTML will subscribe to the audio stream
    webserver_client.close()

# Receive audio data from the client
def handle_server_client(server_client):
  while True:
    if streaming_client is None: continue
    data = server_client.recv(1024)  # Adjust buffer size as needed
    
    # Send the audio data to the streaming client
    streaming_client.send(data)

# This recieves the audio on ip_address:5000 from other RPi Picos
def handle_server():
  while True:
    # Wait to accept new client connections
    server_client, server_address = server_socket.accept()
    
    print('Server client connected:', server_address)
    
    # Make a thread so we can recieve from multiple RPi Pico clients
    _thread.start_new_thread(handle_server_client, (server_client))

# This has to be multithreaded so we can handle connections on multiple sockets at the same time
_thread.start_new_thread(handle_webserver, ())
_thread.start_new_thread(handle_server, ())
_thread.start_new_thread(handle_streaming, ())
