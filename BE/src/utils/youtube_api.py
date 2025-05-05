from googleapiclient.discovery import build  # type: ignore
from dotenv import load_dotenv  # type: ignore
import os

load_dotenv()

# API_KEY = os.getenv("YOUTUBE_API_KEY")
# print(f'youtube_api_key: f{API_KEY}')

class Youtube:
    def __init__(self, api_key: str):
        self.youtube = build("youtube", "v3", developerKey=api_key) # type: ignore

    def get_top_vids(self, keyword: str):
        request = self.youtube.search().list(
            q=keyword,
            part="snippet",
            type="video",
            videoCategoryId="10",
            order="relevance",
            maxResults=10,
            topicId="/m/04rlf",
            videoDuration="medium",
            relevanceLanguage="en"
        )

        response = request.execute()
        music_links = []

        for item in response['items']:
            title = item['snippet']['title']
            channel = item['snippet']['channelTitle']
            video_id = item['id']['videoId']
            link = f"https://www.youtube.com/watch?v={video_id}"

            if "official" in title.lower() or "vevo" in channel.lower():
                music_links.append(f"{title}\n{link}")
            else:
                music_links.append(f"{title}\n{link}")


        return music_links
    

# # For checking
# keyword = "piya ore piya"
# youtube = Youtube(API_KEY)
# links = youtube.get_top_vids(keyword)

# for link in links:
#     print(f"{link}")
