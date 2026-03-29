import pandas as pd

print("🔄 Combining YouTube data from both laptops...\n")

# Load laptop1 (friend)
laptop1_channels = pd.read_csv('channels_lap1.csv')
laptop1_videos = pd.read_csv('videos_lap1.csv')
laptop1_comments = pd.read_csv('comments_lap1.csv')

print(f"Laptop1 (Friend):")
print(f"  Channels: {len(laptop1_channels)}")
print(f"  Videos: {len(laptop1_videos)}")
print(f"  Comments: {len(laptop1_comments)}\n")

# Load laptop2 (you)
laptop2_channels = pd.read_csv('channels_lap2.csv')
laptop2_videos = pd.read_csv('videos_lap2.csv')
laptop2_comments = pd.read_csv('comments_lap2.csv')

print(f"Laptop2 (You):")
print(f"  Channels: {len(laptop2_channels)}")
print(f"  Videos: {len(laptop2_videos)}")
print(f"  Comments: {len(laptop2_comments)}\n")

# Combine
all_channels = pd.concat([laptop1_channels, laptop2_channels], ignore_index=True)
all_videos = pd.concat([laptop1_videos, laptop2_videos], ignore_index=True)
all_comments = pd.concat([laptop1_comments, laptop2_comments], ignore_index=True)

print(f"Combined (before dedup):")
print(f"  Channels: {len(all_channels)}")
print(f"  Videos: {len(all_videos)}")
print(f"  Comments: {len(all_comments)}\n")

# Remove duplicates (in case any overlap)
final_channels = all_channels.drop_duplicates(subset='channel_id', keep='first')
final_videos = all_videos.drop_duplicates(subset='video_id', keep='first')
final_comments = all_comments.drop_duplicates(subset='comment_id', keep='first')

print(f"Final (after removing duplicates):")
print(f"  Channels: {len(final_channels)}")
print(f"  Videos: {len(final_videos)}")
print(f"  Comments: {len(final_comments)}\n")

# Save final files
final_channels.to_csv('final_youtube_channels.csv', index=False)
final_videos.to_csv('final_youtube_videos.csv', index=False)
final_comments.to_csv('final_youtube_comments.csv', index=False)

print("✅ Combined data saved!")
print("\n📁 Files created:")
print("   - final_youtube_channels.csv")
print("   - final_youtube_videos.csv")
print("   - final_youtube_comments.csv")
print(f"\n🎉 YOUTUBE DATA COLLECTION COMPLETE!")
print(f"   Total: {len(final_channels)} unique channels")
print(f"   Total: {len(final_videos)} videos")
print(f"   Total: {len(final_comments)} comments")