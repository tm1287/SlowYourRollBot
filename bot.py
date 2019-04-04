import praw
import secret
import urllib
import re
import psutil

from bs4 import BeautifulSoup
from pystreamable import StreamableApi
from moviepy.editor import *

api = StreamableApi(secret.email, secret.streamable_pass)

reddit = praw.Reddit(client_id = secret.client_id, client_secret = secret.client_secret, user_agent = secret.user_agent, username = secret.username, password = secret.password)

#print(reddit.read_only)

def ScrapeImgurVideo(link_id, mention_id):
    submission = reddit.submission(id=link_id)
    print(submission.media['oembed']['url'])
    imgurUrl = str(submission.media['oembed']['url'])
    imgurPage = urllib.request.urlopen(imgurUrl)
    imgurSoup = BeautifulSoup(imgurPage, 'html.parser')

    videoContainer = imgurSoup.find('meta', attrs={'property': 'og:video'})
    videoLink = re.findall('"([^"]*)"', str(videoContainer))[0]

    urllib.request.urlretrieve(videoLink, str(link_id) + '_' + str(mention_id) + '.mp4')

def ScrapeRedditVideo(link_id, mention_id):
    submission = reddit.submission(id=link_id)
    urllib.request.urlretrieve(str(submission.media['reddit_video']['fallback_url']),link_id + '_' + str(mention_id) + '.mp4')


def ScrapeYoutubeVideo(link_id, mention_id):
    PostReply(mention_id, "Sorry, SlowYourRollBot doesn't work on Youtube videos. This will change in the future.")
    print("DOes it get here????")

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

    PROCNAME = 'ffmpeg-win64-v4.1.exe'
    for proc in psutil.process_iter():
        # check whether the process name matches
        if proc.name() == PROCNAME:
            proc.kill()

def UploadVideo(videoName):
    api.upload_video(videoName, str(videoName))
    return api.upload_video(videoName, str(videoName)).get('shortcode')

def PostReply(MentionId, text):
    MentionId.reply(text)

def get_sec(time_str):
    m, s = time_str.split(':')
    return int(m) * 60 + int(s)

while True:
    for mention in reddit.inbox.mentions(limit=25):
        if mention.new:
            if (mention.submission.is_reddit_media_domain) != False:
                ScrapeRedditVideo(str(mention.submission), mention)
            elif (mention.submission.domain.lower() == "youtu.be" or mention.submission.domain.lower() == "youtube.com"):
                ScrapeYoutubeVideo(str(mention.submission), mention)
            else:
                ScrapeImgurVideo(str(mention.submission), mention)

            print(mention.body.split(" ")[1], mention.body.split(" ")[2], mention.body.split(" ")[3])
            try:
                ProcessVideo(str(mention.submission), str(mention), mention.body.split(" ")[1], mention.body.split(" ")[2], mention.body.split(" ")[3])
            except (OSError):
                print("Path to downloaded video was not found. MoviePy Error")
            try:
                PostReply(mention, "[Here is your processed video]" + '(https://streamable.com/' + UploadVideo(str(mention.submission) + "_" + str(mention) + "_processed.mp4") + ')')
                print("Reply Posted")
            except (FileNotFoundError):
                print("File could not be found for the Post Reply func.")
            mention.mark_read()
            try:
                os.remove(str(str(mention.submission) + "_" + str(mention) + "_processed.mp4"))
                os.remove(str(mention.submission) + "_" + str(mention) + ".mp4")
                print("Files Deleted")
            except(FileNotFoundError):
                print("File could not be found for the os remove function.")
