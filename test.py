import praw
import secret
import pprint

reddit = praw.Reddit(client_id = secret.client_id, client_secret = secret.client_secret, user_agent = secret.user_agent, username = secret.username, password = secret.password)

submission = reddit.submission(id='996hiv')
#submission = reddit.submission(id='995eot')
print(submission.title) # to make it non-lazy
pprint.pprint(vars(submission))