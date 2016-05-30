from slackclient import SlackClient
import os
import requests
import time
import math
import argparse

BOT_TOKEN = os.environ.get('API_TOKEN')
CLIENT_ID = "2d7d4b83a596ae06623c"
CLIENT_SECRET = "9167a622887a9f5a468d49ee39142140750141f9"

API_URL = "https://api.github.com/repos/awesome-jobs/jobs/issues" \
			+ "?client_id=" + CLIENT_ID \
			+ "&client_secret=" + CLIENT_SECRET

def generate_jobs_post(order, title, kw, link):
    jobs_post_file = open("jobs_post.md", "r").read()
    return jobs_post_file.format(order=order, title=title, kw=kw, link=link)

def main(args):
    sc = SlackClient(BOT_TOKEN)

    channel_name = args.channel
    timer = args.timer
    extend_timer = args.extend
    group_newmember = args.group

    CLIENT_ID = "2d7d4b83a596ae06623c"
    CLIENT_SECRET = "9167a622887a9f5a468d49ee39142140750141f9"

    API_URL = "https://api.github.com/repos/awesome-jobs/jobs/issues" \
            + "?client_id=" + CLIENT_ID \
            + "&client_secret=" + CLIENT_SECRET

    r = requests.get(API_URL)
    jsonData = r.json()

    jobs = []

    for job in jsonData:
        item = {}
        item['title'] = job['title']
        item['html_url'] = job['html_url']
        item['labels'] = []
        for label in job['labels']:
            item['labels'].append(label['name'])

        jobs.append(item.copy())

    if not sc.rtm_connect():
        print 'Cannot connect'
        return

    job_post = generate_jobs_post(1, jobs[0]['title'], ", ".join(jobs[0]['labels']), jobs[0]['html_url'])

    print job_post
    print sc.api_call("chat.postMessage", as_user="true", channel=channel_name, text=job_post, mrkdwn="true")   

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