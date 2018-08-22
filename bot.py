import praw
import secret
import os
import urllib
import requests
from moviepy.editor import *

reddit = praw.Reddit(client_id = secret.client_id, client_secret = secret.client_secret, user_agent = secret.user_agent, username = secret.username, password = secret.password)

def ScrapeVideo(link_id, mention_id):
    submission = reddit.submission(id=link_id)
    if submission.is_reddit_media_domain == "True":
        urllib.request.urlretrieve(str(submission.media['reddit_video']['fallback_url']), link_id + '_' + mention_id + '.mp4')
    else:
        urllib.request.urlretrieve('https://imgur.com/download/' + str(str(submission.url).split('/')[3].split('.')[0]), link_id + '_' + mention_id + '.mp4')

def ProcessVideo(link, mention, start_time, end_time, slow_factor):
    fullclip = VideoFileClip(link + "_" + mention + ".mp4")
    clip1 = VideoFileClip(link + "_" + mention + ".mp4").subclip(0, get_sec(start_time))
    clip2 = VideoFileClip(link + "_" + mention + ".mp4").subclip(get_sec(start_time), get_sec(end_time)).fx( vfx.speedx, float(slow_factor))
    clip3 = VideoFileClip(link + "_" + mention + ".mp4").subclip(get_sec(end_time), int(fullclip.duration))
    result = concatenate_videoclips([clip1, clip2, clip3])
    result.write_videofile(link + "_" + mention + "_processed" + ".mp4")
    fullclip.reader.close()
    clip1.reader.close()
    clip2.reader.close()
    clip3.reader.close()
    os.remove(link + "_" + mention + ".mp4")

#def UploadVideo(videoName):

def get_sec(time_str):
    m, s = time_str.split(':')
    return int(m) * 60 + int(s)

#while True:
#    for mention in reddit.inbox.mentions(limit=25):
#        if mention.new:
#            ScrapeVideo(str(mention.submission), str(mention))
#            print(mention.body.split(" ")[1], mention.body.split(" ")[2], mention.body.split(" ")[3])
#            ProcessVideo(str(mention.submission), str(mention), mention.body.split(" ")[1], mention.body.split(" ")[2], mention.body.split(" ")[3])
#            mention.mark_read()

ScrapeVideo("996hiv", "837hia")