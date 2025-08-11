import praw
import os
import feedparser
import requests
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone
load_dotenv()

# Use your own credentials or load from .env
CLIENT_ID = os.getenv("REDDIT_CLIENT_ID") or "YOUR_CLIENT_ID"
CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET") or "YOUR_CLIENT_SECRET"
USER_AGENT = os.getenv("REDDIT_USER_AGENT") or "EventGPTApp/0.1 by YourUsername"


# Initialize Reddit API client
reddit = praw.Reddit(client_id=CLIENT_ID,
                     client_secret=CLIENT_SECRET,
                     user_agent=USER_AGENT)

def fetch_subreddit_rss(url):
    headers = {'User-Agent': 'EventGPT/1.0'}
    feed = feedparser.parse(url, request_headers=headers)
    return feed

def fetch_post_html(url):
    headers = {'User-Agent': 'EventGPT/1.0'}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.text

def fetch_subreddit_posts(subreddit_name, limit=10):
    subreddit = reddit.subreddit(subreddit_name)
    posts = []
    now = datetime.now(timezone.utc)
    time_limit = now - timedelta(days=1) 

    for post in subreddit.new(limit=limit):

        post_time = datetime.fromtimestamp(post.created_utc, tz=timezone.utc)
        if post_time < time_limit:
            # Skip posts older than 24 hours
            continue
        posts.append({
            "id": post.id,
            "title": post.title,
            "selftext": post.selftext,
            "url": post.url,
            "created_utc": post.created_utc,
            "created_datetime": post_time,
            "author": str(post.author),
            "num_comments": post.num_comments,
            "score": post.score,
            "permalink": post.permalink,
        })
    
    posts.sort(key=lambda x: (x["num_comments"], x["score"]), reverse=True)
    return posts

def search_subreddits(keyword, limit=10):
    results = reddit.subreddits.search(keyword, limit=limit)
    for subreddit in results:
        print(f"{subreddit.display_name}: {subreddit.title}")

if __name__ == "__main__":

    # keywords = ["events", "meetup", "social", "tech", "hackathon"]
    # for kw in keywords:
    #     print(f"Subreddits related to '{kw}':")
    #     search_subreddits(kw)
    #     print("\n")

    subreddits = ["erlangen","munich", "munichsocialclub","berlinsocialclub","Regensburg","Nuremberg", "Augsburg", "Stuttgart", "Berlin", "Hamburg", "Cologne", "freiburg", "Frankfurt", "Leipzig", "Dresden",  "Dortmund"]
    for sub in subreddits:
        print(f"Fetching posts from r/{sub} (last 24 hours, sorted by comments & score)...")
        posts = fetch_subreddit_posts(sub, limit=10)
        for p in posts:
            created_str = p["created_datetime"].strftime("%Y-%m-%d %H:%M:%S %Z")
            print(f"- {p['title']} - {p['num_comments']} comments, \n {p['created_datetime']} created_datetime, {p['score']} points\n")
        print("\n")




