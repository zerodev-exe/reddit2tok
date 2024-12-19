import praw
import os
import random

# Set up your Reddit API credentials
client_id = os.getenv("REDDIT_CLIENT_ID")
client_secret = os.getenv("REDDIT_CLIENT_SECRET")
user_agent = "random_post_fetcher:v1.0 (by u/PwaDiePie)"

subreddits = ["nosleep", "confession"]

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
    sub = return_random_subreddit()
    subreddit = reddit.subreddit(sub)

    # # Fetch a list of top posts from today
    posts = list(subreddit.top(limit=100, time_filter='day'))  # Getting top 100 posts from 'top' of today

    # # Select a random post
    random_post = random.choice(posts)

    # random_post = reddit.submission(id="1hh4phc")

    reddit_url = "https://www.reddit.com/r/"+sub+"/comments/"+random_post.id

    # Return the title and body text
    return {
        "title": random_post.title,
        "body": random_post.selftext,
        "id": random_post.id,
        "sub": subreddit,
        "url": reddit_url
    }
