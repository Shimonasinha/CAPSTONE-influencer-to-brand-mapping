import requests
import pandas as pd
import time
import re
import os

# ── API KEY ───────────────────────────────────────────────────
RAPIDAPI_KEY  = "489c3b82c4mshf8834aabeed8423p1389c1jsn9b1f895c9a87"
RAPIDAPI_HOST = "twitter241.p.rapidapi.com"

HEADERS = {
    "x-rapidapi-key":  RAPIDAPI_KEY,
    "x-rapidapi-host": RAPIDAPI_HOST,
    "Content-Type":    "application/json"
}

# ── ONLY NEW INDIAN BRANDS ────────────────────────────────────
NEW_BRANDS = [
    {"name": "GNC India",         "handle": "gnclivewellind"},
    {"name": "MyProtein",         "handle": "myprotein"},
    {"name": "Optimum Nutrition", "handle": "optimumnutrition"},
    {"name": "Bewakoof",          "handle": "bewakoof"},
    {"name": "Cult Fit",          "handle": "cultfit"},
    {"name": "Fitpass",           "handle": "fitpass"},
    {"name": "Kapiva",            "handle": "kapivaayurveda"},
]

TWEETS_PER_BRAND = 50


def get_user_id(handle):
    url = "https://twitter241.p.rapidapi.com/user"
    params = {"username": handle}
    try:
        r = requests.get(url, headers=HEADERS, params=params, timeout=10)
        data = r.json()
        user = (data.get("result", {})
                    .get("data", {})
                    .get("user", {})
                    .get("result", {}))
        legacy      = user.get("legacy", {})
        user_id     = user.get("rest_id")
        screen_name = legacy.get("screen_name")
        followers   = legacy.get("followers_count", 0)
        name        = legacy.get("name", "")
        return user_id, screen_name, followers, name
    except:
        return None, None, 0, ""


def get_user_tweets(user_id, count=50):
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
                if tweet_data and tweet_data.get("full_text"):
                    tweets.append({
                        "tweet_id"    : tweet_data.get("id_str"),
                        "text"        : tweet_data.get("full_text"),
                        "likes"       : tweet_data.get("favorite_count", 0),
                        "retweets"    : tweet_data.get("retweet_count", 0),
                        "replies"     : tweet_data.get("reply_count", 0),
                        "published_at": tweet_data.get("created_at"),
                        "lang"        : tweet_data.get("lang"),
                    })
        return tweets
    except:
        return []


def extract_mentions(text):
    return re.findall(r'@(\w+)', text)


def main():
    # ── Load existing files ───────────────────────────────────
    print(" Loading existing data...")
    df_existing = pd.read_csv('final_twitter_brands.csv', encoding='utf-8-sig') if os.path.exists('final_twitter_brands.csv') else pd.DataFrame()
    df_existing_sponsors = pd.read_csv('twitter_sponsorship_events.csv', encoding='utf-8-sig') if os.path.exists('twitter_sponsorship_events.csv') else pd.DataFrame()
    print(f"  Existing brand tweets     : {len(df_existing)}")
    print(f"  Existing sponsorship events: {len(df_existing_sponsors)}")

    new_tweets = []

    for i, brand in enumerate(NEW_BRANDS):
        print(f"\n[{i+1}/{len(NEW_BRANDS)}]   {brand['name']} → @{brand['handle']}")

        user_id, screen_name, followers, name = get_user_id(brand['handle'])

        if not user_id:
            print(f"   Not found on Twitter")
            time.sleep(1)
            continue

        print(f"  Found @{screen_name} ({followers:,} followers)")

        tweets = get_user_tweets(user_id, TWEETS_PER_BRAND)
        influencer_tweets = 0

        for t in tweets:
            mentions = extract_mentions(t["text"])
            has_influencer = len(mentions) > 0
            new_tweets.append({
                "tweet_id"              : t["tweet_id"],
                "brand"                 : brand['name'],
                "twitter_handle"        : screen_name or brand['handle'],
                "text"                  : t["text"],
                "likes"                 : t["likes"],
                "retweets"              : t["retweets"],
                "replies"               : t["replies"],
                "published_at"          : t["published_at"],
                "lang"                  : t["lang"],
                "mentions"              : ", ".join(mentions),
                "has_influencer_mention": has_influencer,
            })
            if has_influencer:
                influencer_tweets += 1

        print(f"   Got {len(tweets)} tweets | {influencer_tweets} mention influencers")
        time.sleep(1.5)

    # ── Combine old + new ─────────────────────────────────────
    df_new = pd.DataFrame(new_tweets)
    df_combined = pd.concat([df_existing, df_new], ignore_index=True)
    df_combined.drop_duplicates(subset='tweet_id', inplace=True)
    df_combined['published_at'] = pd.to_datetime(df_combined['published_at'], utc=True, errors='coerce', format='mixed')
    df_combined['date']         = df_combined['published_at'].dt.date
    df_combined['hour']         = df_combined['published_at'].dt.hour
    df_combined['day_of_week']  = df_combined['published_at'].dt.day_name()
    df_combined.sort_values('published_at', inplace=True)
    df_combined.reset_index(drop=True, inplace=True)

    # ── Save back to SAME files ───────────────────────────────
    df_combined.to_csv('final_twitter_brands.csv', index=False, encoding='utf-8-sig')

    df_sponsors = df_combined[df_combined['has_influencer_mention'] == True].copy()
    df_sponsors.to_csv('twitter_sponsorship_events.csv', index=False, encoding='utf-8-sig')

    print(f"\n Done! Updated existing files!")
    print(f"Total brand tweets      : {len(df_combined)} (was {len(df_existing)})")
    print(f"Sponsorship events      : {len(df_sponsors)} (was {len(df_existing_sponsors)})")
    print(f"New tweets added        : {len(df_new)}")

if __name__ == "__main__":
    main()