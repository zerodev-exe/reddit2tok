import praw
import random

# Set up your Reddit API credentials
client_id = "mqUapE34mxg-Fo_KRSa9rQ"
client_secret = "d3zMEmGJxK6Ov5FYv4_qFSHDpFpMOQ"
user_agent = "random_post_fetcher:v1.0 (by u/PwaDiePie)"

# Create a Reddit instance
reddit = praw.Reddit(client_id=client_id,
                    client_secret=client_secret,
                    user_agent=user_agent)


def get_random_post_text(subreddit_name="nosleep"):
    # Get the subreddit
    subreddit = reddit.subreddit(subreddit_name)

    # Fetch a list of hot posts (or another list)
    posts = list(subreddit.hot(limit=200))  # Getting top 200 posts from 'hot'

    # Select a random post
    random_post = random.choice(posts)

    # Return the title and body text
    return {
        "title": random_post.title,
        "body": random_post.selftext,
        "id": random_post.id
    }
