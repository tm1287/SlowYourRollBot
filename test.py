import urllib
import re

import praw
import secret
import pprint

from bs4 import BeautifulSoup

reddit = praw.Reddit(client_id = secret.client_id, client_secret = secret.client_secret, user_agent = secret.user_agent, username = secret.username, password = secret.password)

'''
submission = reddit.submission(id='99dckg')
#submission = reddit.submission(id='995eot')
print(submission.title) # to make it non-lazy
pprint.pprint(vars(submission))
print(submission.is_reddit_media_domain)
'''

imgurUrl = "https://imgur.com/a/1Bpniri"
imgurPage = urllib.request.urlopen(imgurUrl)
imgurSoup = BeautifulSoup(imgurPage, 'html.parser')

videoContainer = imgurSoup.find('meta', attrs={'property': 'og:video'})
videoLink = re.findall('"([^"]*)"', str(videoContainer))[0]

urllib.request.urlretrieve(videoLink, 'a' + '_' + 'b' + '.mp4')

