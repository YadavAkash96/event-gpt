import os
import praw
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
USER_AGENT = os.getenv("REDDIT_USER_AGENT") or "EventGPTApp/0.1 by YourUsername"

reddit = praw.Reddit(client_id=CLIENT_ID,
                     client_secret=CLIENT_SECRET,
                     user_agent=USER_AGENT)

def fetch_posts_with_images(subreddit_name, limit=20):
    subreddit = reddit.subreddit(subreddit_name)
    posts_with_images = []

    for post in subreddit.new(limit=limit):
        image_url = None
        
        # Check if post has preview images (most common case)
        if hasattr(post, 'preview'):
            images = post.preview.get('images', [])
            if images:
                image_url = images[0]['source']['url']

        # Sometimes post.url itself is a direct image link (jpg, png, gif)
        if not image_url:
            if post.url.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
                image_url = post.url

        if image_url:
            posts_with_images.append({
                "id": post.id,
                "title": post.title,
                "image_url": image_url,
                "created_utc": post.created_utc,
                "author": str(post.author),
                "num_comments": post.num_comments,
                "score": post.score,
                "permalink": post.permalink,
            })

    return posts_with_images


if __name__ == "__main__":
    subreddit_name = ["Art"] #,"erlangen","munich", "munichsocialclub","berlinsocialclub","Regensburg","Nuremberg", "Augsburg", "Stuttgart", "Berlin", "Hamburg", "Cologne", "freiburg", "Frankfurt", "Leipzig", "Dresden",  "Dortmund"]
    for sub in subreddit_name:
        print(f"Fetching posts with images from r/{sub} ...")
        posts = fetch_posts_with_images(sub, limit=5)
        for p in posts:
            print(f"Title: {p['title']}")
            print(f"Image URL: {p['image_url']}")
            print(f"Link: https://reddit.com{p['permalink']}")
            print()
