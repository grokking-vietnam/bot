from slackclient import SlackClient
import os
import os.path
import requests
import time
import math
import argparse

BOT_TOKEN = os.environ.get('API_TOKEN')
CLIENT_ID = os.environ.get('CLIENT_ID')
CLIENT_SECRET = os.environ.get('CLIENT_SECRET')

API_URL = "https://api.github.com/repos/awesome-jobs/jobs/issues" \
			+ "?client_id=" + CLIENT_ID \
			+ "&client_secret=" + CLIENT_SECRET

def generate_jobs_post(order, title, kw, link):
    jobs_post_file = open("jobs_post.md", "r").read()
    return jobs_post_file.format(order=order, title=title, kw=kw, link=link)

def getJobs(url):
    r = requests.get(url)
    jsonData = r.json()

    jobs = []

    for job in jsonData:
        item = {}
        item['title'] = job['title']
        item['id'] = job['id']
        item['html_url'] = job['html_url']
        item['labels'] = []
        for label in job['labels']:
            item['labels'].append(label['name'])

        jobs.append(item.copy())
    return jobs

def main(args):
    sc = SlackClient(BOT_TOKEN)

    channel_name = args.channel
    timer = args.timer
    extend_timer = args.extend
    group_newmember = args.group

    if not sc.rtm_connect():
        print 'Cannot connect'
        return

    # Initialize job post message
    job_post = "New jobs:\n"
    jobs = getJobs(API_URL)

    # Open file to read id
    if os.path.isfile("id.txt"):
        file = open("id.txt", "r")
        file_read = file.read()
        id_from_file = int(file_read)

        if id_from_file == jobs[0]['id']: 
            job_post = ""
    else:
        id_from_file = None

    # Post jobs from beginning to the previously saved id
    for index, job in enumerate(jobs):
        if job['id'] == id_from_file:
            # If id == previously saved id, then break the loop and save the new id to file
            os.remove("id.txt")
            break

        job_post += generate_jobs_post(index + 1, jobs[index]['title'].encode('utf-8'), ", ".join(jobs[index]['labels']), jobs[index]['html_url'])

    # Overwrite the new id to file
    file2 = open("id.txt", "w")
    file2.write(str(jobs[0]['id']))
    file2.close()

    sc.api_call("chat.postMessage", as_user="true", channel=channel_name, text=job_post, mrkdwn="true")   

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
