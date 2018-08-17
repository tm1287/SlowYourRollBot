import praw
import secret
import time
import urllib

reddit = praw.Reddit(client_id = secret.client_id, client_secret = secret.client_secret, user_agent = secret.user_agent, username = secret.username, password = secret.password)

def ScrapeVideo(link_id):
    submission = reddit.submission(id=link_id)
    urllib.request.urlretrieve(str(submission.media['reddit_video']['fallback_url']), link_id + '_' + str(time.time()) + '.mp4')



for mention in reddit.inbox.mentions(limit=25):
    if mention.new:
        ScrapeVideo(str(mention.submission))
        mention.mark_read()
