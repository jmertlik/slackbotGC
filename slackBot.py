

import os
import datetime
from slackclient import SlackClient
from dotenv import load_dotenv
from classes import Timer

load_dotenv('python.env')

slack_token = os.environ["SLACK_API_TOKEN"]
sc = SlackClient(slack_token)
batch_presence_aware = True
presence_sub = True

rpgUser = {
    "user": None,
    "start": None,
    "total": None}
#dictionary name, start time, total time
events = {
    "ts": None}

ud = open("userdata.txt", "w+")
ud.write("{}".format(rpgUser))

def get_ts():
    print("%s is now active" % rpgUser["user"])
    rpgUser["start"] = Timer.start

def end_ts():
    print("%s is now inactive" % rpgUser["user"])
    rpgUser["total"] = (datetime.datetime.now - rpgUser["start"] + rpgUser["total"])

if sc.rtm_connect():
    while True:
        events = sc.rtm_read()
        for event in events:
            if event["type"] == "message":
                if event["text"] == "list users":
                    sc.api_call(
                        "chat.postMessage",
                        channel=event["channel"], 
                        text="hello")
            elif event["type"] == "presence_change":
                if event["presence"] == "active":
                    get_ts()
                elif event["presence"] == "away":
                    end_ts()
    else:
         print("Connection Failed")