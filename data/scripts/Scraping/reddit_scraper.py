import requests
import pandas as pd
import time

HEADERS = {"User-Agent": "fitness_research/1.0"}
YOUTUBE_CHANNELS_FILE = "final_youtube_channels_clean.csv"
POSTS_PER_INFLUENCER  = 10

def search_reddit(query, limit=10):
    url = "https://www.reddit.com/search.json"
    params = {"q": query, "limit": limit, "sort": "relevance", "type": "link"}
    try:
        r = requests.get(url, headers=HEADERS, params=params, timeout=10)
        data = r.json()
        posts = data.get("data", {}).get("children", [])
        return [p["data"] for p in posts]
    except Exception as e:
        print(f"    Error: {e}")
        return []

def main():
    print("📂 Loading YouTube channels...")

    # Try multiple encodings
    df_yt = None
    for enc in ['utf-8-sig', 'utf-8', 'latin-1', 'cp1252']:
        try:
            df_yt = pd.read_csv(YOUTUBE_CHANNELS_FILE, encoding=enc, on_bad_lines='skip')
            print(f"✅ Loaded with encoding: {enc}")
            print(f"Columns: {list(df_yt.columns)}")
            break
        except Exception as e:
            print(f" {enc} failed: {e}")
            continue

    if df_yt is None:
        print(" Could not load file!")
        return

    # Get name column
    name_col = 'name' if 'name' in df_yt.columns else df_yt.columns[1]
    print(f"Using column: '{name_col}'")

    names = df_yt[name_col].dropna().unique().tolist()
    names = [n for n in names if len(str(n)) > 3]
    print(f"✅ Found {len(names)} influencers")
    print(f"Sample: {names[:5]}")

    all_posts = []

    for i, name in enumerate(names):
        clean_name = str(name).strip()
        print(f"\n[{i+1}/{len(names)}] 🔍 {clean_name}")

        posts = search_reddit(clean_name, limit=POSTS_PER_INFLUENCER)
        count = 0

        for post in posts:
            all_posts.append({
                "influencer_name": clean_name,
                "title"          : post.get("title", ""),
                "text"           : post.get("selftext", ""),
                "subreddit"      : post.get("subreddit", ""),
                "author"         : post.get("author", ""),
                "score"          : post.get("score", 0),
                "upvote_ratio"   : post.get("upvote_ratio", 0),
                "num_comments"   : post.get("num_comments", 0),
                "published_at"   : pd.to_datetime(post.get("created_utc", 0), unit='s', utc=True),
                "url"            : post.get("url", ""),
            })
            count += 1

        print(f"   Got {count} posts")
        time.sleep(1)

    if not all_posts:
        print("\n No posts collected!")
        return

    df = pd.DataFrame(all_posts)
    df.drop_duplicates(subset=['influencer_name', 'title'], inplace=True)
    df['date']        = df['published_at'].dt.date
    df['hour']        = df['published_at'].dt.hour
    df['day_of_week'] = df['published_at'].dt.day_name()
    df.sort_values('published_at', inplace=True)
    df.reset_index(drop=True, inplace=True)
    df.to_csv('final_reddit_posts.csv', index=False, encoding='utf-8-sig')

    print(f"\n🎉 Done! Saved as final_reddit_posts.csv")
    print(f"Total posts        : {len(df)}")
    print(f"Influencers found  : {df['influencer_name'].nunique()}")
    print(f"Subreddits covered : {df['subreddit'].nunique()}")
    print(f"Date range         : {df['published_at'].min()} → {df['published_at'].max()}")

if __name__ == "__main__":
    main()