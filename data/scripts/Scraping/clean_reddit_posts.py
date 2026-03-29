import pandas as pd

df = pd.read_csv('final_reddit_posts.csv', encoding='utf-8-sig')
print(f"Before: {len(df)} rows")

# 1. Remove clearly non-fitness subreddits
REMOVE_SUBREDDITS = [
    'cricket', 'nba', 'nfl', 'nhl', 'soccer', 'football',
    'bollywood', 'movies', 'television', 'gaming', 'games',
    'politics', 'news', 'worldnews', 'indiacricket', 'indiaspeaks',
    'hilariabaldwin', 'roadies_mtv', 'instacelebsgossip',
    'bollyblindsnggossip', 'alienstage', 'superstonk',
    'topcharactertropes', 'nosleep', 'popculturechat',
    'createaroster', 'oklahoma', 'askreddit', 'funny',
    'pics', 'videos', 'worldnews', 'tifu', 'todayilearned',
]
df['sub_lower'] = df['subreddit'].str.lower()
df = df[~df['sub_lower'].isin(REMOVE_SUBREDDITS)].copy()
df.drop(columns=['sub_lower'], inplace=True)

# 2. Fill null text with empty string
df['text'] = df['text'].fillna('')

# 3. Combine title + text for richer sentiment analysis later
df['full_text'] = df['title'] + ' ' + df['text']
df['full_text'] = df['full_text'].str.strip()

# 4. Remove rows where full_text is too short (less than 10 chars)
df = df[df['full_text'].str.len() > 10].copy()

# 5. Reset index
df.reset_index(drop=True, inplace=True)

print(f"After : {len(df)} rows")
print()
print("Top subreddits:")
print(df['subreddit'].value_counts().head(15))

df.to_csv('final_reddit_posts.csv', index=False, encoding='utf-8-sig')
print(f"\n✅ Cleaned and saved to final_reddit_posts.csv!")