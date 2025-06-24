import os
import argparse
import time
import pandas as pd
import tweepy
from dotenv import load_dotenv
from tweepy.errors import TooManyRequests

# Load bearer token from .env
def load_config():
    load_dotenv()
    return os.getenv("BEARER_TOKEN")

# Get Twitter user ID from username
def get_user_id(client, username):
    try:
        user = client.get_user(username=username)
        return user.data.id
    except Exception as e:
        print(f"❌ Failed to get user ID for '{username}': {e}")
        return None

# Check if tweet contains media or links
def detect_media(tweet):
    if hasattr(tweet, 'attachments') and tweet.attachments:
        return "media"
    elif tweet.entities and ("urls" in tweet.entities):
        return "link"
    return "none"

# Fetch all tweets using pagination
def fetch_all_tweets(client, user_id, max_total=2000):
    data = []
    try:
        paginator = tweepy.Paginator(
            client.get_users_tweets,
            id=user_id,
            tweet_fields=["id", "created_at", "public_metrics", "entities", "attachments"],
            expansions=["attachments.media_keys"],
            media_fields=["type"],
            max_results=100
        )

        for response in paginator:
            if response.data is None:
                break

            for tweet in response.data:
                metrics = tweet.public_metrics
                data.append([
                    tweet.id,
                    tweet.created_at,
                    metrics.get("like_count", 0),
                    metrics.get("retweet_count", 0),
                    metrics.get("reply_count", 0),
                    metrics.get("quote_count", 0),
                    detect_media(tweet),
                    tweet.text
                ])

                # Optional limit (~2k tweets)
                if len(data) >= max_total:
                    return data

    except TooManyRequests:
        print("⚠️ Rate limit hit. Sleeping for 60 seconds...")
        time.sleep(60)
        return fetch_all_tweets(client, user_id, max_total)
    except Exception as e:
        print(f"❌ Error fetching tweets: {e}")
    return data

# Save to CSV
def save_to_csv(data, output_file):
    columns = ["Tweet ID", "Created At", "Likes", "Retweets", "Replies", "Quotes", "Media", "Tweet"]
    df = pd.DataFrame(data, columns=columns)
    df.to_csv(output_file, index=False)
    print(f"✅ Saved {len(df)} tweets to {output_file}")

# Main CLI interface
def main():
    parser = argparse.ArgumentParser(description="Fetch all tweets from a public Twitter user timeline.")
    parser.add_argument("--username", required=True, help="Twitter username (without @)")
    parser.add_argument("--output", default="tweets_sample.csv", help="Output CSV filename")
    parser.add_argument("--max", type=int, default=2000, help="Max number of tweets to fetch (default 2000)")

    args = parser.parse_args()

    bearer_token = load_config()
    if not bearer_token:
        print("❌ Bearer token not found in .env file.")
        return

    client = tweepy.Client(bearer_token=bearer_token, wait_on_rate_limit=True)

    user_id = get_user_id(client, args.username)
    if not user_id:
        return

    print(f"🔍 Fetching tweets for @{args.username}...")
    tweets_data = fetch_all_tweets(client, user_id, max_total=args.max)

    if tweets_data:
        save_to_csv(tweets_data, args.output)
    else:
        print("⚠️ No tweets found.")

if __name__ == "__main__":
    main()
