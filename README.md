# attentionButtonPublic
Raspberry Pi powered attention button connected via Twitter API + MongoDB. Uses Neopixel library, so will only work with neoPixel compatible LEDs. Built in Python. The first raspberry Pi needs to have a keyboard/keypad attached that can input 1,2,3. When the user presses 1, it will turn the attached LED light on and off. When the user presses 2, it will toggle between preset RGB colors stored in MongoDB. When the user presses 3, it will send the current color to the second Raspberry Pi, which will also light up with the same color. Users can control the preset colors, as well as the brightness by sending tweets. Example: https://imgur.com/WIjm0gY

# preRequesites: 
- Two Raspberry Pis with RPIO, and one has to have I/O to input 1/2/3 keys. 
- Two NeoPixel Compatible LEDs (these are the ones I used: https://www.amazon.com/gp/product/B08PCP6RY7/ref=ppx_yo_dt_b_asin_title_o04_s00?ie=UTF8&psc=1).
- Breadboard Jumper wires to connect LEDs to RPIO.
- Twitter Developer account with elevated access. 

# example tweets: 

These tweets must be sent in JSON format in order for the python listening side to work correctly.

**Listing colors:**

{"action":"colors", 
“mention”: “yourTwitterHandleHere”}

**Adding a color:**

{"action" : "add", 
"color" : "black",
"hexcode" : "#000000",
“mention”: “yourTwitterHandleHere”
}

**Removing a color:** 

- Remove via name:
{"action": "remove", "color":"pale green",“mention”: “yourTwitterHandleHere”}

- Remove via hexcode:
{"action": "remove", "hexcode":"#c7fdb5",“mention”: “yourTwitterHandleHere”}

**Changing Brightness:**

{"action":"brightness", "brightness": "2",“mention”: “yourTwitterHandleHere”}

**Turning the light off for the second RPi:**

{"action": "stop", "mention": "@yourTwitterHandleHere"}

# Files: 
There are two files in this repository: 

1. attentionButton.py - This python file parses the mongoDB for colors and sends the messages that the other RPi listens to in order to function. 
2. listener.py - This python file has all the server side code to listen for tweets and perform the operations: adding/removing colors, setting brightness, turning itself on, etc. 

# Database:
You can configure this how'd you like but you will need to modify the code to fit your own personal formatting. This is just how my databases are configured for this specific setup:

**colorDb.colors:**
color : "testGreen"
hexcode : "#0C8E18"

**colorDb.brightness:**
brightness: 2

# Usage: 
Put the python code onto your RPis and set the code to run on startup. I modified the .bashrc file personally. Make sure that for your MongoDB atlas you have the ports opened up for whatever IPv4 you're accessing the MongoDBs from. Adding/Removing Colors/Changing Brightness from the DB will require a reboot to take effect.