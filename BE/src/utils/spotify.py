import os
import base64
import json
from requests import get, post  # type: ignore
from dotenv import load_dotenv  # type: ignore

load_dotenv()

# SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
# SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

class spotifyapi:
    def __init__(self):
        load_dotenv()
        self.client_id = os.getenv('SPOTIFY_CLIENT_ID')
        self.client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
        self.token = None
        self.token_expires_in = 0  
        self.token_timestamp = 0  

    def get_token(self):
        import time
        current_time = time.time()

        # Refresh token only if expired
        if self.token and (current_time - self.token_timestamp) < self.token_expires_in:
            return self.token

        auth_string = f"{self.client_id}:{self.client_secret}"
        auth_bytes = auth_string.encode('utf-8')
        auth_base64 = base64.b64encode(auth_bytes).decode('utf-8')

        url = "https://accounts.spotify.com/api/token"
        headers = {
            "Authorization": f"Basic {auth_base64}",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        data = {"grant_type": "client_credentials"}

        response = post(url, headers=headers, data=data)
        result = response.json()

        self.token = result.get('access_token')
        self.token_expires_in = result.get('expires_in', 3600) 
        self.token_timestamp = current_time
        return self.token


    def get_auth_header(self):
        token = self.get_token()
        return {"Authorization": f"Bearer {token}"}

    def search_spotify(self, song_title=None, artist_name=None):
        url = "https://api.spotify.com/v1/search"
        headers = self.get_auth_header()

        if song_title and artist_name:
            query = f"?q=track:{song_title} artist:{artist_name}&type=track&limit=1"
        elif song_title:
            query = f"?q={song_title}&type=track&limit=1"
        elif artist_name:
            query = f"?q={artist_name}&type=artist&limit=1"
        else:
            return "no input given, try again!"

        response = get(url + query, headers=headers)
        json_result = response.json()

        if song_title:
            items = json_result.get("tracks", {}).get("items", [])
            return items[0]["external_urls"]["spotify"] if items else "no song found"

        if artist_name:
            items = json_result.get("artists", {}).get("items", [])
            return items[0]["external_urls"]["spotify"] if items else "no artist found"

        return items

# example usage
# spotify = spotifyapi()
# song_name = "tum hi ho"
# artist_name  = ""
# song_link = spotify.search_spotify(song_name)
# profile_link = spotify.search_spotify(artist_name)
# print(f"{song_name} song link: {song_link}")
# print(f"{artist_name} profile link: {profile_link}")