import requests
import pandas as pd
import time

# ── API KEY ───────────────────────────────────────────────────
RAPIDAPI_KEY  = YOUR_API_TWITTER
RAPIDAPI_HOST = "twitter241.p.rapidapi.com"

HEADERS = {
    "x-rapidapi-key":  RAPIDAPI_KEY,
    "x-rapidapi-host": RAPIDAPI_HOST,
    "Content-Type":    "application/json"
}

# ── YOUR YOUTUBE CHANNELS FILE ────────────────────────────────
YOUTUBE_CHANNELS_FILE = "final_youtube_channels_clean.csv"
TWEETS_PER_USER       = 20


def get_user_id(username):
    """Find Twitter user ID from username"""
    url = "https://twitter241.p.rapidapi.com/user"
    params = {"username": username}
    try:
        r = requests.get(url, headers=HEADERS, params=params, timeout=10)
        data = r.json()
        user = data.get("result", {}).get("data", {}).get("user", {}).get("result", {})
        user_id = user.get("rest_id")
        screen_name = user.get("legacy", {}).get("screen_name")
        followers = user.get("legacy", {}).get("followers_count", 0)
        return user_id, screen_name, followers
    except:
        return None, None, 0


def get_user_tweets(user_id, count=20):
    """Get tweets for a user ID"""
    url = "https://twitter241.p.rapidapi.com/user-tweets"
    params = {"user": user_id, "count": str(count)}
    try:
        r = requests.get(url, headers=HEADERS, params=params, timeout=10)
        data = r.json()
        instructions = (data.get("result", {})
                           .get("timeline", {})
                           .get("instructions", []))
        tweets = []
        for inst in instructions:
            for entry in inst.get("entries", []):
                tweet_data = (entry.get("content", {})
                                   .get("itemContent", {})
                                   .get("tweet_results", {})
                                   .get("result", {})
                                   .get("legacy", {}))
                if tweet_data:
                    tweets.append({
                        "tweet_id"    : tweet_data.get("id_str"),
                        "text"        : tweet_data.get("full_text"),
                        "likes"       : tweet_data.get("favorite_count", 0),
                        "retweets"    : tweet_data.get("retweet_count", 0),
                        "replies"     : tweet_data.get("reply_count", 0),
                        "views"       : tweet_data.get("views", {}).get("count", 0),
                        "published_at": tweet_data.get("created_at"),
                        "lang"        : tweet_data.get("lang"),
                    })
        return tweets
    except:
        return []


def main():
    # ── 1. Load YouTube influencer names ──────────────────────
    print(" Loading YouTube channels...")
    df_yt = pd.read_csv(YOUTUBE_CHANNELS_FILE, encoding='utf-8-sig')
    names = df_yt['name'].dropna().unique().tolist()
    names = [n for n in names if len(str(n)) > 3]
    print(f" Found {len(names)} influencers")

    # ── 2. Find Twitter handles + scrape tweets ───────────────
    all_tweets    = []
    matched_users = []

    for i, name in enumerate(names):
        clean_name = str(name).strip()
        # Convert name to possible username (remove spaces)
        username = clean_name.replace(" ", "").lower()

        print(f"\n[{i+1}/{len(names)}]  {clean_name} → @{username}")

        # Find user
        user_id, screen_name, followers = get_user_id(username)

        if not user_id:
            print(f"   Not found on Twitter")
            time.sleep(1)
            continue

        print(f"   Found @{screen_name} ({followers:,} followers)")
        matched_users.append({
            "youtube_name" : clean_name,
            "twitter_handle": screen_name,
            "followers"    : followers,
            "user_id"      : user_id
        })

        # Get their tweets
        tweets = get_user_tweets(user_id, TWEETS_PER_USER)
        for t in tweets:
            t["influencer_name"]   = clean_name
            t["twitter_handle"]    = screen_name
            all_tweets.append(t)

        print(f"   Got {len(tweets)} tweets")
        time.sleep(1.5)  # be nice to the API

    # ── 3. Save matched users ─────────────────────────────────
    if matched_users:
        df_users = pd.DataFrame(matched_users)
        df_users.to_csv('twitter_matched_users.csv', index=False, encoding='utf-8-sig')
        print(f"\n Saved {len(df_users)} matched users → twitter_matched_users.csv")

    # ── 4. Save tweets ────────────────────────────────────────
    if not all_tweets:
        print("\n No tweets collected!")
        return

    df = pd.DataFrame(all_tweets)
    df.drop_duplicates(subset='tweet_id', inplace=True)
    df['published_at'] = pd.to_datetime(df['published_at'], utc=True)
    df['date']         = df['published_at'].dt.date
    df['hour']         = df['published_at'].dt.hour
    df['day_of_week']  = df['published_at'].dt.day_name()
    df.sort_values('published_at', inplace=True)
    df.reset_index(drop=True, inplace=True)
    df.to_csv('final_twitter_matched.csv', index=False, encoding='utf-8-sig')

    print(f"\n🎉 Done! Saved as final_twitter_matched.csv")
    print(f"Total tweets       : {len(df)}")
    print(f"Influencers matched: {df['influencer_name'].nunique()}")
    print(f"Date range         : {df['published_at'].min()} → {df['published_at'].max()}")


if __name__ == "__main__":
    main()