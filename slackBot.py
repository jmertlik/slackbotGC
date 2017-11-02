import os
import time
from slackclient import SlackClient
from dotenv import load_dotenv

load_dotenv('.env')

slack_token = os.environ["SLACK_API_TOKEN"]
sc = SlackClient(slack_token)

rpgUser = {
    "user": None,
    "start": None,
    "total": 0
} #dictionary name, start time, end time, total time

def handle_channel_join(event):
    print("Status change for ", event['user'])
    print("They are now ", event['presence'])
    print("Time is: ", time.time())
    if event['presence'] == 'active':
        rpgUser ["user"] = event["user"]
        #i = len(user_list)
        #user_list[i] = rpgUser ["user"]
        rpgUser ["start"] = time.time()
        for person in users:
            print(person["name"])
    else:
        rpgUser ["total"] = float(rpgUser ["total"]) + (float(time.time()) - float(rpgUser ["start"]))
        print("They are gone ", rpgUser ["total"])


if sc.rtm_connect():
    while True:
        events = sc.rtm_read()
        
        users = sc.api_call("users.list")

        for event in events:
            if event ["type"] == "message":
                if event ["text"] == "waddayaat":
                    sc.api_call(
                        "chat.postMessage",
                        channel=event ["channel"], 
                        #text= user_list
                    )
            elif event ["type"] == "presence_change":
                handle_channel_join(event)        
