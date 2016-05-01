# -*- coding: utf-8 -*-
from slackclient import SlackClient
import os
import requests
import time
import math


BOT_TOKEN = os.environ.get('API_TOKEN')
CHANNEL_NAME = "test_bot" #change to #general-discussions

SLACK_GUIDELINE = 'https://raw.githubusercontent.com/grokking-vietnam/docs/master/slack_guideline.md?ts={}'
SLACK_WELCOME = 'https://raw.githubusercontent.com/grokking-vietnam/docs/master/welcome_message.md?ts={}'

INTRODUCE_TIME_INTERVAL = 20 #seconds
INTRODUCE_MAX_MEMBER = 2

def main():
    # Create the slackclient instance
    sc = SlackClient(BOT_TOKEN)

    startTimer = 0
    newMembers = []

    # Connect to slack
    if sc.rtm_connect():
        channe_id = sc.server.channels.find(CHANNEL_NAME).id
        while True:
            # Read latest messages
            for slack_message in sc.rtm_read():
                #print slack_message
                if slack_message.get('type') == 'message':
                    if slack_message.get('subtype') == 'channel_join' and slack_message.get('channel') == channe_id:
                        user = slack_message.get('user')
                        
                        #add new members to list for self-introduce in channel
                        if len(newMembers) == 0:
                            startTimer = time.time()
                        newMembers.append(user)

                        #send IM guidelines message
                        timestamp = math.floor(time.time())
                        gk_guideline = requests.get(SLACK_GUIDELINE.format(timestamp))
                        guideline_im = gk_guideline.text.format(user=user)
                        print sc.api_call("chat.postMessage", channel=user, as_user="true", text=guideline_im)
                    else:
                        message = slack_message.get("text")
                        user = slack_message.get("user")
                        if not message or not user:
                            continue
                        sc.rtm_send_message(CHANNEL_NAME, "<@{}> wrote something...".format(user))

            #Send introduce message on channel every INTRODUCE_TIME_INTERVAL OR members joint > INTRODUCE_MAX_MEMBER
            if (len(newMembers) > 0) and ((time.time() - startTimer > INTRODUCE_TIME_INTERVAL) or (len(newMembers) >= INTRODUCE_MAX_MEMBER)):
                timestamp = math.floor(time.time())
                gk_welcome = requests.get(SLACK_WELCOME.format(timestamp))

                userIds = ''
                for user in newMembers:
                    userIds += '<@' + user + '> '
                userIds = userIds.rstrip(' ')

                sc.rtm_send_message(CHANNEL_NAME, gk_welcome.text.format(userIds=userIds, channel=CHANNEL_NAME))
                newMembers = []

            time.sleep(0.5)
    else:
        print 'Cannot connect'

if __name__ == '__main__':
    main()