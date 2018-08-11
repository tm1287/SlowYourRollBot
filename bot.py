import praw
import secret
import urllib

reddit = praw.Reddit(client_id = secret.client_id, client_secret = secret.client_secret, user_agent = secret.user_agent, username = secret.username, password = secret.password)

url = "https://www.reddit.com/r/FortNiteBR/comments/95t737/how_to_counter_spray_meta/".split("/")

print(url[6])

def ScrapeVideo(link_id):
    submission = reddit.submission(id=link_id)
    urllib.request.urlretrieve(str(submission.media['reddit_video']['fallback_url']), link_id + '.mp4')

ScrapeVideo(url[6])

