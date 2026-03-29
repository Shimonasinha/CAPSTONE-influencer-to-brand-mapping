import asyncio
import ssl
import os
import pandas as pd

ssl._create_default_https_context = ssl._create_unverified_context

from twikit import Client

# ── FILL IN YOUR DETAILS ──────────────────────────────────────
USERNAME = "SSinha56281"
EMAIL    = "shimonasinha222@gmail.com"
PASSWORD = "shimona123"        # ← only change this!

YOUTUBE_CHANNELS_FILE  = "final_youtube_channels_clean.csv"
TWEETS_PER_INFLUENCER  = 20


async def main():
    # ── 1. Login (saves cookies so you only login once) ───────
    client = Client('en-US')

    if os.path.exists('cookies.json'):
        print(" Loading saved cookies...")
        client.load_cookies('cookies.json')
    else:
        print(" Logging in for first time...")
        await client.login(
            auth_info_1=USERNAME,
            auth_info_2=EMAIL,
            password=PASSWORD,
            cookies_file='cookies.json'
        )
        print(" Logged in and cookies saved!")

    # ── 2. Load YouTube influencer names ──────────────────────
    print("\n Loading YouTube channels...")
    df_yt = pd.read_csv(YOUTUBE_CHANNELS_FILE, encoding='utf-8-sig')
    names = df_yt['name'].dropna().unique().tolist()
    names = [n for n in names if len(str(n)) > 3]
    print(f" Found {len(names)} influencers")
    print(f"Sample: {names[:5]}")

    # ── 3. Search tweets for each influencer ──────────────────
    all_tweets = []

    for i, name in enumerate(names):
        clean_name = str(name).strip()
        print(f"\n[{i+1}/{len(names)}]  {clean_name}")

        try:
            tweets = await client.search_tweet(
                f'"{clean_name}"', 'Latest'
            )

            count = 0
            for tweet in tweets:
                if count >= TWEETS_PER_INFLUENCER:
                    break
                all_tweets.append({
                    "tweet_id"        : tweet.id,
                    "influencer_name" : clean_name,
                    "author"          : tweet.user.screen_name if tweet.user else "unknown",
                    "text"            : tweet.text,
                    "likes"           : tweet.favorite_count,
                    "retweets"        : tweet.retweet_count,
                    "replies"         : tweet.reply_count,
                    "views"           : tweet.view_count,
                    "published_at"    : tweet.created_at,
                })
                count += 1

            print(f"   Got {count} tweets")

        except Exception as e:
            print(f"   Skipped '{clean_name}': {e}")
            continue

        await asyncio.sleep(2)

    # ── 4. Save clean CSV ─────────────────────────────────────
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

    print(f"\n Done! Saved as final_twitter_matched.csv")
    print(f"Total tweets       : {len(df)}")
    print(f"Influencers matched: {df['influencer_name'].nunique()}")


if __name__ == "__main__":
    asyncio.run(main())