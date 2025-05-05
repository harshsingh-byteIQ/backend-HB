from ytmusicapi import YTMusic # type: ignore
from dotenv import load_dotenv
import os

# load_dotenv()

# api_key = os.getenv("YTMUSIC_API_KEY") 

class YTMusicAPI():
    def __init__(self, headers_path):
        self.ytmusic = YTMusic(headers_path)

    def get_official_music_videos(self, keyword: str):
        search_results = self.ytmusic.search(keyword, filter="songs")

        video_links = []
        for result in search_results:
            video_id = result['videoId']
            video_links.append(f"https://www.youtube.com/watch?v={video_id}")

        return video_links

#example run
keyword = input("Enter song name: ").strip()
YTM = YTMusicAPI(r"C:\Users\BYTEIQ\Desktop\ss\Helping-Buddy\helping-buddy\src\helping_buddy\App\headers_auth.json")
links = YTM.get_official_music_videos(keyword)

for link in links:
    print(f"{link}\n")