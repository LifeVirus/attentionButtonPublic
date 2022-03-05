import tweepy
import json
import re
import board
import neopixel
import pymongo
from datetime import datetime
from pymongo import MongoClient

while True:
    try:
        CONNECTION_STRING = "YOUR MONGODB CONNECTION STRING"
        client = MongoClient(CONNECTION_STRING)
        db = client["YOUR DB NAME"]
        colorCollection = db["YOUR COLLECTION NAME"]
        brightnessCollection = db["YOUR BRIGHTNESS COLLECTION NAME"]
        brightness = brightnessCollection.find()[0]["brightness"]/10.0
        pixels = neopixel.NeoPixel(board.D21, 16, brightness= brightness)
        colorIndex = 0
        red = 255
        green = 255
        blue = 255
        pixels.fill((0,0,0))
        pixels.show()

        #The RGBReader class builds off the tweepy API Stream object which will listen for tweets from the specified account
        #or mentions that mention the specified account.
        class RGBReader(tweepy.Stream):
            def on_status(self, status):
                api = tweepy.Client(consumer_key="INSERT CONSUMER KEY HERE", 
                            consumer_secret="INSERT CONSUMER SECRET HERE",
                            access_token="INSERT ACCESS TOKEN HERE",
                            access_token_secret="INSERT TOKEN SECRET HERE",
                            bearer_token="INSERT BEARER TOKEN HERE",
                            wait_on_rate_limit=True)

                print(status.text)
                #when we recieve a tweet, check the action
                action = ""
                try:
                    tweetDict = json.loads(status.text)
                    action = tweetDict["action"]
                    print(tweetDict["action"])
                except Exception as e:
                    print(e)

                #depending on the action, do different things
                if action == "stop":
                    print("stop")
                    pixels.fill(0,0,0)
                
                if action == "read":
                    print(tweetDict["red"])
                    print(tweetDict["green"])
                    print(tweetDict["blue"])
                    pixels.fill((int(tweetDict["red"]),int(tweetDict["green"]),int(tweetDict["blue"])))
                    pixels.show()
                
                #list the colors in the db as separate tweets
                if action == "colors":
                    try: 
                        colors = colorCollection.find()
                        colorsList = list(colors)
                        charCounter = 0
                        charString = ''
                        for color in colorsList:
                            if charCounter < 200:
                                charString += color["color"]
                                charString += ":"
                                charString += color["hexcode"]
                                charString += ","
                                charString += " "
                                charCounter = charCounter + len(color["color"]) + 3 + len(color["hexcode"])
                            else:
                                now = datetime.now()
                                current_time = now.strftime("%H:%M:%S")
                                charString += current_time
                                api.create_tweet(text = charString)
                                charString = ''
                                charCounter = 0
                                charString += color["color"]
                                charString += ":"
                                charString += color["hexcode"]
                                charString += ","
                                charString += " "
                                charCounter = charCounter + len(color["color"]) + 3 + len(color["hexcode"])
                        now = datetime.now()
                        current_time = now.strftime("%H:%M:%S")
                        charString += current_time
                        if len(charString) > 280:
                            charString = charString[:250]
                        api.create_tweet(text = charString)
                    
                    except Exception as e:
                        print(e)

                #regex to check if the add is a valid color
                if(action == "add"):
                    try:
                        if re.match("^#[A-Fa-f0-9]{6}$", tweetDict["hexcode"]):
                            colorCollection.insert_one({"color": tweetDict["color"], "hexcode": tweetDict["hexcode"]})
                    except Exception as e:
                        print(e)

                #remove via color name or hexcode
                if(action == "remove"):
                    try:
                        if "color" in tweetDict.keys():
                            colorCollection.delete_one({"color": tweetDict["color"]})
                        
                        elif "hexcode" in tweetDict.keys():
                            colorCollection.delete_one({"hexcode": tweetDict["hexcode"]})
                        
                        
                    except Exception as e:
                        print(e)
                
                if(action == "brightness"):
                    try:
                        brightnessCollection.update_one({"brightness" : brightnessCollection.find()[0]["brightness"]}, {"$set": {"brightness" : int(tweetDict["brightness"])}})
                    except Exception as e:
                        print(e)


        reader = RGBReader(consumer_key="YOUR CONSUMER KEY HERE",
                            consumer_secret="YOUR CONSUMER SECRET HERE",
                            access_token="YOUR ACCESS_TOKEN HERE",
                            access_token_secret="YOUR ACCESS TOKEN SECRET HERE")

        reader.filter(follow = ["THE ACCOUNT THE OTHER PYTHON FILE USES TO TWEET"],track = ['ACCOUNT HANDLE FOR MENTIONS'])
    except Exception as e:
        print("exception occurred, restart!")
        print(e)