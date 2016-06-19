# -*- coding: utf-8 -*-
from slackclient import SlackClient
import os
import requests
import time
import math
import argparse

BOT_TOKEN = os.environ.get('API_TOKEN')

SLACK_CHANNEL_DESC = 'https://raw.githubusercontent.com/grokking-vietnam/docs/master/channels_description.md?ts={}'
SLACK_WELCOME = 'https://raw.githubusercontent.com/grokking-vietnam/docs/master/welcome_message.md?ts={}'

def generate_channel_desc_message(user):
    timestamp = math.floor(time.time())
    gk_guideline = requests.get(SLACK_CHANNEL_DESC.format(timestamp))
    return gk_guideline.text.format(user=user)


def generate_welcome_message(user_ids, channel_name):
    timestamp = math.floor(time.time())
    gk_welcome = requests.get(SLACK_WELCOME.format(timestamp))
    return gk_welcome.text.format(userIds=user_ids, channel=channel_name)

def main(args):
    channel_name = args.channel
    timer = args.timer
    extend_timer = args.extend
    group_newmember = args.group

    # Create the slackclient instance
    sc = SlackClient(BOT_TOKEN)

    start_timer = 0
    new_members = []

    # Connect to slack
    if not sc.rtm_connect():
        print 'Cannot connect'
        return

    channel_id = sc.server.channels.find(channel_name).id
    while True:
        # Read latest messages
        for slack_message in sc.rtm_read():
            if (slack_message.get('type') == 'message'
                and slack_message.get('subtype') == 'channel_join'
                and slack_message.get('channel') == channel_id):
                user = slack_message.get('user')

                new_members.append(user)
                # add new members to list for self-introduce in channel
                if len(new_members) <= extend_timer:
                    start_timer = time.time()

                # send IM guidelines message
                guideline_im = generate_channel_desc_message(user)
                sc.api_call("chat.postMessage", channel=user, as_user="true", text=guideline_im)

        # Send introduce message on channel every timer
        # OR members joint > group_newmember
        if (len(new_members) > 0
            and (
                (time.time() - start_timer > timer) or
                (len(new_members) >= group_newmember)
            )):
            user_ids = ' '.join(['<@' + user + '>' for user in new_members])
            #sc.rtm_send_message(channel_name, generate_welcome_message(user_ids, channel_name))
            new_members = []

        time.sleep(0.5)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='This is Grokking bot')
    parser.add_argument('-c', '--channel', help='Channel name bot running e.g. test_bot', required=True)
    parser.add_argument('-t', '--timer',
                        help='[Seconds] Time wait before sending welcoming message on channel to new user. Default: 600s',
                        type=int,
                        default=600)
    parser.add_argument('-e', '--extend',
                        help='Maximum times to reset timer when a new user join. Default: 3',
                        type=int,
                        default=3)
    parser.add_argument('-g', '--group',
                        help='Group maximum n users and send 1 welcoming message. Default: 5',
                        type=int,
                        default=5)

    args = parser.parse_args()
    main(args)