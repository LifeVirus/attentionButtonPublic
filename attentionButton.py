#This python file is run on the rasp pi that will select and send the colors. 

import board
import neopixel
import keyboard
import pymongo
import tweepy
import json
from datetime import datetime
from pymongo import MongoClient

while True:
    try:
        #the api is used to send tweets
        api = tweepy.Client(consumer_key="INSERT CONSUMER KEY HERE", 
                            consumer_secret="INSERT CONSUMER SECRET HERE",
                            access_token="INSERT ACCESS TOKEN HERE",
                            access_token_secret="INSERT TOKEN SECRET HERE",
                            bearer_token="INSERT BEARER TOKEN HERE",
                            wait_on_rate_limit=True)

        #setting up your collection details
        CONNECTION_STRING = "INSERT MONGO CONNECTION STRING HERE"
        client = MongoClient(CONNECTION_STRING)
        db = client["DATABASE NAME"]
        colorCollection = db["COLOR COLLECTION NAME"]
        brightnessCollection = db["BRIGHTNESS COLLECTION NAME"]
        #brightness is set from 0.1-1.0 so in DB it should be 0-10
        brightness = brightnessCollection.find()[0]["BRIGHTNESS COLLECTION NAME"]/10.0
        pixels = neopixel.NeoPixel(board.D21, 16, brightness= brightness)
        onOff = "off"
        colorIndex = 0
        red = 255
        green = 255
        blue = 255

        #turns the RPi on and off
        def onOffSetter():
            try:
                global onOff
                if (onOff == "off"):
                    pixels.fill((red,green,blue))
                    pixels.show()
                    onOff = "on"
                else:
                    pixels.fill((0,0,0))
                    pixels.show()
                    onOff = "off"
            except Exception as e:
                print ("Exception in onOffSetter")
                print (e)

        #sets the color that the RPi will be using, by iterating through the mongoDB one color at a time       
        def colorSetter():
            try:
                global colorIndex
                global red
                global green
                global blue
                colors = colorCollection.find()
                colorsList = list(colors)
                
                #if the color is on, it will go to the next color
                if(onOff == "on"):
                    if (colorIndex < len(colorsList)):
                        if (colorIndex == 0):
                            colorIndex = 1
                        hexValue = colorsList[colorIndex]["hexcode"].lstrip("#")
                        #turns hexcode into rgb values
                        colorTuple = tuple(int(hexValue[i:i+2], 16) for i in (0, 2, 4))
                        red = colorTuple[0]
                        green = colorTuple[1]
                        blue = colorTuple[2]
                        colorIndex += 1
                        print("red: " + str(red) + " green: " + str(green) + " blue: " + str(blue))
                    
                    #once we reach the end, we loop back to the beginning
                    else:
                        colorIndex = 0
                        hexValue = colorsList[colorIndex]["hexcode"].lstrip("#")
                        ##turns hexcode into rgb values
                        colorTuple = tuple(int(hexValue[i:i+2], 16) for i in (0, 2, 4))
                        red = colorTuple[0]
                        green = colorTuple[1]
                        blue = colorTuple[2]
                        print("red: " + str(red) + " green: " + str(green) + " blue: " + str(blue))
                        
                    pixels.fill((red,green,blue))
                    pixels.show()
            except Exception as e:
                print("exception occurred in colorSetter")
                print(e)

        #sends a tweet that the other RPi listens to so that it can match color
        def colorSender():
            try:
                now = datetime.now()
                current_time = now.strftime("%H:%M:%S")
                tweet = {"action" : "read",
                    "red": red,
                    "green": green,
                    "blue": blue,
                    "timeStamp": current_time}
                tweetText = json.dumps(tweet)
                api.create_tweet(text = tweetText)
                print("tweet Sent")
                print(tweetText)
            except Exception as e:
                print("exception occurred in colorSender")
                print(e)

        #keyboard module makes it so when you hit 1,2,3 the respective function will run
        keyboard.add_hotkey("1", onOffSetter)
        keyboard.add_hotkey("2", colorSetter)
        keyboard.add_hotkey("3", colorSender)
        try:
            keyboard.wait()
        except Exception as e:
            print("Exception in keyboard wait")
            print(e)
    
    except Exception as e:
        print("Exception Occurred in main")
        print(e)