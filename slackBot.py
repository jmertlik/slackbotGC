

import os
#import time
from slackclient import SlackClient
from dotenv import load_dotenv

load_dotenv('.env')

slack_token = os.environ["SLACK_API_TOKEN"]
sc = SlackClient(slack_token)
batch_presence_aware = True
presence_sub = True


rpgUser = {
    "user": None,
    "start": None,
    "total": None}
#dictionary name, start time, total time

# HowTo: write mode
with open("mylist.txt", "w") as f:
    f.write("{}".format(rpgUser))

# HowTo: read mode
with open("mylist.txt", "r") as f:
    rd = f.readline()
print(rd)


def handle_channel_join(event):
    print("Status change for ", event['user'])
    rpgUser["user"] = event["user"]
    rpgUser["start"] = event["ts"]
    if rpgUser["start"] != None:
        rpgUser["total"] = (event["ts"] - rpgUser["start"]) + rpgUser["total"]
        rpgUser["start"] = None

## This stuff will replace the above handle function
## Breaking it up should allow us to handle it differently based on if
## the user is coming or going, also there is only Active or Away
## I can't find any documentation for offline
def get_ts():
    print("%s is now active" % rpgUser["user"])
    rpgUser["start"] = event ["ts"]

def end_ts():
    print("%s is now inactive" % rpgUser["user"])
    rpgUser["total"] = event["ts"] - rpgUser["start"] + rpgUser["total"]
    rpgUser["start"] = None

if sc.rtm_connect():
    while True:
        events = sc.rtm_read()
        for event in events:
            if event ["type"] == "message":
                if event ["text"] == "list users":
                    sc.api_call(
                        "chat.postMessage",
                        channel=event ["channel"], 
                        text="hello")
            elif event ["type"] == "presence_change":
                if event ["presence"] == "active":
                    get_ts()
                elif event ["presence"] == "away":
                    end_ts()
    else:
         print("Connection Failed")