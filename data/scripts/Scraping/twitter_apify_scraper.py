from apify_client import ApifyClient
import pandas as pd
import time

# PASTE YOUR TOKEN HERE (from Step 1)
APIFY_TOKEN = YOUR_API_TWITTER

# Load YouTube channels
print(" Loading YouTube channels...")
df_yt = pd.read_csv('final_youtube_channels_clean.csv', encoding='utf-8-sig')
names = df_yt['name'].dropna().unique().tolist()

print(f" Found {len(names)} influencers")
print(f"Sample: {names[:5]}\n")

# Initialize Apify
client = ApifyClient(APIFY_TOKEN)

all_tweets = []
total_scraped = 0

# Start with first 50 influencers (to stay within free tier)
for i, name in enumerate(names[:50]):
    print(f"\n[{i+1}/50] Searching: {name}")
    
    # Apify Twitter Scraper input
    run_input = {
        "searchTerms": [f'"{name}"'],
        "maxTweets": 20,
        "start": "2025-09-01",
        "end": "2026-03-26",
        "onlyVerifiedUsers": False
    }
    
    try:
        # Run the Twitter scraper actor
        run = client.actor("quacker/twitter-scraper").call(run_input=run_input)
        
        # Get results
        count = 0
        for item in client.dataset(run["defaultDatasetId"]).iterate_items():
            all_tweets.append({
                "tweet_id": item.get("id", ""),
                "influencer_name": name,
                "author": item.get("author", {}).get("userName", "unknown"),
                "text": item.get("text", ""),
                "likes": item.get("likeCount", 0),
                "retweets": item.get("retweetCount", 0),
                "replies": item.get("replyCount", 0),
                "views": item.get("viewCount", 0),
                "published_at": item.get("createdAt", "")
            })
            count += 1
        
        total_scraped += count
        print(f"   Got {count} tweets (Total: {total_scraped})")
        
        # Check free tier limit (5,000 results)
        if total_scraped >= 4800:
            print("\n Approaching free tier limit (5,000 tweets)")
            print("Stopping to stay within free tier")
            break
        
    except Exception as e:
        print(f"   Error: {e}")
        continue
    
    time.sleep(2)  # Rate limiting

# Save results
if all_tweets:
    df = pd.DataFrame(all_tweets)
    df.drop_duplicates(subset='tweet_id', inplace=True)
    
    # Add temporal columns
    df['published_at'] = pd.to_datetime(df['published_at'], utc=True, errors='coerce')
    df['date'] = df['published_at'].dt.date
    df['hour'] = df['published_at'].dt.hour
    df['day_of_week'] = df['published_at'].dt.day_name()
    
    df.to_csv('final_twitter_matched.csv', index=False, encoding='utf-8-sig')
    
    print(f"\n COMPLETE!")
    print(f"   Total tweets: {len(df)}")
    print(f"   Influencers matched: {df['influencer_name'].nunique()}")
    print(f"   Saved to: final_twitter_matched.csv")
else:
    print("\n No tweets collected!")