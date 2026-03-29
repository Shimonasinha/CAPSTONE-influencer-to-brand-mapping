import pandas as pd

# ── 1. Load both laps ──────────────────────────────────────────
df1 = pd.read_csv('channels_lap1.csv', encoding='utf-8')
df2 = pd.read_csv('channels_lap2.csv', encoding='utf-8')

print(f"Lap1 rows: {len(df1)}")
print(f"Lap2 rows: {len(df2)}")

# ── 2. Combine ─────────────────────────────────────────────────
combined = pd.concat([df1, df2], ignore_index=True)
print(f"Combined rows: {len(combined)}")

# ── 3. Remove duplicates ───────────────────────────────────────
combined.drop_duplicates(subset='channel_id', inplace=True)
print(f"After removing duplicates: {len(combined)}")

# ── 4. Fill missing values ─────────────────────────────────────
combined['description'] = combined['description'].fillna('')
combined['country']     = combined['country'].fillna('Unknown')
combined['scraped_at']  = combined['scraped_at'].fillna('Unknown')

# ── 5. Fix scraped_at timestamp where available ────────────────
combined['scraped_at'] = pd.to_datetime(combined['scraped_at'], errors='coerce', utc=True)

# ── 6. Sort by subscribers (biggest first) ─────────────────────
combined.sort_values('subscribers', ascending=False, inplace=True)
combined.reset_index(drop=True, inplace=True)

# ── 7. Save clean CSV ──────────────────────────────────────────
combined.to_csv('final_youtube_channels_clean.csv', index=False, encoding='utf-8-sig')

print(f"\n✅ Done! Saved as final_youtube_channels_clean.csv")
print(f"Total clean channels: {len(combined)}")
print(f"Countries found: {combined['country'].value_counts().to_dict()}")