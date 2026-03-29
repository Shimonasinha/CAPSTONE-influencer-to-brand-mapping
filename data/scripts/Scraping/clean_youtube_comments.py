import pandas as pd

# ── 1. Load both laps ──────────────────────────────────────────
df1 = pd.read_csv('comments_lap1.csv', encoding='utf-8')
df2 = pd.read_csv('comments_lap2.csv', encoding='utf-8')

print(f"Lap1 rows: {len(df1)}")
print(f"Lap2 rows: {len(df2)}")

# ── 2. Combine ─────────────────────────────────────────────────
combined = pd.concat([df1, df2], ignore_index=True)
print(f"Combined rows: {len(combined)}")

# ── 3. Remove duplicates ───────────────────────────────────────
combined.drop_duplicates(subset='comment_id', inplace=True)
print(f"After removing duplicates: {len(combined)}")

# ── 4. Drop rows with empty text ───────────────────────────────
combined.dropna(subset=['text'], inplace=True)

# ── 5. Fix timestamps ──────────────────────────────────────────
combined['published_at'] = pd.to_datetime(combined['published_at'], utc=True)

# Extra columns useful for lag analysis
combined['date']        = combined['published_at'].dt.date
combined['hour']        = combined['published_at'].dt.hour
combined['day_of_week'] = combined['published_at'].dt.day_name()

# ── 6. Sort by time ────────────────────────────────────────────
combined.sort_values('published_at', inplace=True)
combined.reset_index(drop=True, inplace=True)

# ── 7. Save clean CSV (utf-8-sig = no gibberish in Excel) ──────
combined.to_csv('final_youtube_comments_clean.csv', index=False, encoding='utf-8-sig')

print(f"\n✅ Done! Saved as final_youtube_comments_clean.csv")
print(f"Total clean rows: {len(combined)}")
print(f"Date range: {combined['published_at'].min()} → {combined['published_at'].max()}")