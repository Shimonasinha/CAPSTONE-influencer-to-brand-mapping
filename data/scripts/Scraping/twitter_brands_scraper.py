import requests
import pandas as pd
import time
import re

# ── API KEY ───────────────────────────────────────────────────
RAPIDAPI_KEY  = "489c3b82c4mshf8834aabeed8423p1389c1jsn9b1f895c9a87"
RAPIDAPI_HOST = "twitter241.p.rapidapi.com"

HEADERS = {
    "x-rapidapi-key":  RAPIDAPI_KEY,
    "x-rapidapi-host": RAPIDAPI_HOST,
    "Content-Type":    "application/json"
}

# ── FITNESS BRANDS TO SCRAPE ──────────────────────────────────
BRANDS = [
    # Global
    "Nike",
    "Adidas",
    "Gymshark",
    "Lululemon",
    "Puma",
    "Reebok",
    "UnderArmour",
    # Indian
    "MuscleBlaze",
    "HealthifyMe",
    "Decathlon",
    "HKVitals",
    "WellbeingNutrition",
]

TWEETS_PER_BRAND = 50  # get 50 tweets per brand


def get_user_id(username):
    url = "https://twitter241.p.rapidapi.com/user"
    params = {"username": username}
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
    """Extract @mentions from tweet text"""
    return re.findall(r'@(\w+)', text)


def main():
    all_tweets     = []
    brand_profiles = []

    for i, brand in enumerate(BRANDS):
        username = brand.lower().replace(" ", "")
        print(f"\n[{i+1}/{len(BRANDS)}] 🏷️  {brand} → @{username}")

        # Get user ID
        user_id, screen_name, followers, name = get_user_id(username)

        if not user_id:
            print(f"  ⚠️ Not found on Twitter")
            time.sleep(1)
            continue

        print(f"  ✅ Found @{screen_name} ({followers:,} followers)")
        brand_profiles.append({
            "brand_name"    : brand,
            "twitter_handle": screen_name,
            "followers"     : followers,
            "user_id"       : user_id
        })

        # Get tweets
        tweets = get_user_tweets(user_id, TWEETS_PER_BRAND)
        influencer_tweets = 0

        for t in tweets:
            mentions = extract_mentions(t["text"])
            has_influencer = len(mentions) > 0

            all_tweets.append({
                "tweet_id"          : t["tweet_id"],
                "brand"             : brand,
                "twitter_handle"    : screen_name,
                "text"              : t["text"],
                "likes"             : t["likes"],
                "retweets"          : t["retweets"],
                "replies"           : t["replies"],
                "published_at"      : t["published_at"],
                "lang"              : t["lang"],
                "mentions"          : ", ".join(mentions),
                "has_influencer_mention": has_influencer,
            })

            if has_influencer:
                influencer_tweets += 1

        print(f"  📝 Got {len(tweets)} tweets | {influencer_tweets} mention influencers")
        time.sleep(1.5)

    # ── Save brand profiles ───────────────────────────────────
    if brand_profiles:
        df_brands = pd.DataFrame(brand_profiles)
        df_brands.to_csv('twitter_brand_profiles.csv', index=False, encoding='utf-8-sig')
        print(f"\n✅ Saved {len(df_brands)} brands → twitter_brand_profiles.csv")

    # ── Save all brand tweets ─────────────────────────────────
    if not all_tweets:
        print("\n❌ No tweets collected!")
        return

    df = pd.DataFrame(all_tweets)
    df.drop_duplicates(subset='tweet_id', inplace=True)
    df['published_at'] = pd.to_datetime(df['published_at'], utc=True, errors='coerce')
    df['date']         = df['published_at'].dt.date
    df['hour']         = df['published_at'].dt.hour
    df['day_of_week']  = df['published_at'].dt.day_name()
    df.sort_values('published_at', inplace=True)
    df.reset_index(drop=True, inplace=True)
    df.to_csv('final_twitter_brands.csv', index=False, encoding='utf-8-sig')

    # ── Save ONLY tweets that mention someone (sponsorship events!) ──
    df_sponsors = df[df['has_influencer_mention'] == True].copy()
    df_sponsors.to_csv('twitter_sponsorship_events.csv', index=False, encoding='utf-8-sig')

    print(f"\n🎉 Done!")
    print(f"Total brand tweets      : {len(df)}")
    print(f"Sponsorship event tweets: {len(df_sponsors)}")
    print(f"Brands scraped          : {df['brand'].nunique()}")
    print(f"Date range              : {df['published_at'].min()} → {df['published_at'].max()}")
    print(f"\nFiles saved:")
    print(f"  → twitter_brand_profiles.csv")
    print(f"  → final_twitter_brands.csv")
    print(f"  → twitter_sponsorship_events.csv ⭐ (most important for GAIL!)")


if __name__ == "__main__":
    main()