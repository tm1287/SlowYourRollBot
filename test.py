import praw
import secret


reddit = praw.Reddit(client_id = secret.client_id, client_secret = secret.client_secret, user_agent = secret.user_agent, username = secret.username, password = secret.password)


for mention in reddit.inbox.mentions(limit=25):
    print('{}\n{}\n'.format(mention.author, mention.body))
    print(mention.submission)
    #submission = reddit.submission(str(mention.submission))
    #print(submission.permalink.split('/')[6])
