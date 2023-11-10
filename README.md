# MusicStream Server

This project is a server application written in MicroPython for the RPi Pico W. It creates an access point and handles multiple incoming connections using multithreading.

## Features

- Creates an access point with the SSID 'MusicStream' and password 'I<3Music'.
- Prints the IP address of the access point.
- Handles multiple incoming connections using multithreading.

## Usage

1. Flash the MicroPython firmware onto your RPi Pico W.
2. Upload the server script to your RPi Pico W.
3. Reset the RPi Pico W to start the server.
4. Connect to the 'MusicStream' access point from your client device.
5. Determine what the default gateway is and connect to it on port 80 for audio controls.

## Notes

- The server receives audio data in chunks of 1024 bytes. Adjust the buffer size as needed for your specific use case.
- Consider looking at [this](https://www.hackster.io/sandeep-mistry/create-a-usb-microphone-with-the-raspberry-pi-pico-cc9bd5) tutorial for the basics on using a microphone with a RPi Pico.
- Here is an alternative microphone which is assumed in the code based on [this](https://www.adafruit.com/product/1713) StackOverflow post.