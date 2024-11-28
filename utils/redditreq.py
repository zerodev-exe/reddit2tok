import praw
import random

# Set up your Reddit API credentials
client_id = "mqUapE34mxg-Fo_KRSa9rQ"
client_secret = "d3zMEmGJxK6Ov5FYv4_qFSHDpFpMOQ"
user_agent = "random_post_fetcher:v1.0 (by u/PwaDiePie)"

subreddits = ["nosleep"]

# Create a Reddit instance
reddit = praw.Reddit(
    client_id=client_id,
    client_secret=client_secret,
    user_agent=user_agent
    )

def return_random_subreddit():
    random_sub = random.choice(subreddits)
    return random_sub

def get_random_post_text():
    # Get the subreddit
    subreddit = reddit.subreddit(return_random_subreddit())

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
