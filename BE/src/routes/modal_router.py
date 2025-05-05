from fastapi import APIRouter  
from fastapi.responses import StreamingResponse
import io
from pydantic import BaseModel, Field  # type: ignore
from typing import Annotated , List
from src.utils.prompt import Genprompt
from src.utils.logger import Logger
from src.utils.youtube_api import Youtube
from src.utils.spotify import spotifyapi
from src.utils.El11labs import ElevenLabs  
from dotenv import load_dotenv  
import os

class Request(BaseModel):
    keyword: Annotated[str, Field(min_length=2)] 

class ytMusicRequest(BaseModel):
    song: str = Field(description="The name of the song")

class MusicRequest(BaseModel):
    song: str|None = Field(default=None, description="The name of the song")
    artist: str|None = Field(default=None, description="The name of the Artist")
    
class ytMusicRequest(BaseModel):
    song: str

class Song(BaseModel):
    title: str
    url: str

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

model_router = APIRouter()
gemini = Genprompt(api_key=GOOGLE_API_KEY)  
logger = Logger()
spotify = spotifyapi()
elevenlabs = ElevenLabs(api_key=ELEVENLABS_API_KEY)
Youtube = Youtube(api_key=YOUTUBE_API_KEY)

@model_router.get("/")
def read_root():
    return {"message": "Welcome to the Question Generator API!", "success": "API endpoint is running."}

@model_router.post("/question")
def get_questions(request : Request):
    try:
        keyword = request.keyword
        logger.log_info(f"Received input: {keyword}")  
        questions = gemini.generate_questions(keyword) 
        return {"data": questions , "status_code" : 200}
    except Exception as e:
        logger.log_error(f"Error generating questions: {str(e)}")
        return {"error": "Something went wrong!"}
    
@model_router.post("/ytMusic")
def get_music(request: ytMusicRequest):
    try:
        song_name = request.song
        # logger.info(f"Received keyword: {song_name}")
        
        if song_name:
            ytmusic_links = Youtube.get_top_vids(song_name)
            songs: List[Song] = []

            for entry in ytmusic_links:
                parts = entry.strip().split('\n')
                if len(parts) == 2:
                    title, url = parts
                    songs.append(Song(title=title.strip(), url=url.strip()))

            return {"data": [song.dict() for song in songs] , "status_code" : 200}
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return {"error": "Something went wrong while fetching music links."}

    except Exception as e:
        logger.log_error(f"Error fetching music: {str(e)}")
        return {"error": "Something went wrong!"}

@model_router.post("/Text-to-speech")
def get_speech(request: Request):
    try:
        keyword = request.keyword
        logger.log_info(f"Received text: {keyword}")
        
        audio = elevenlabs.generate(text=keyword)  # this returns filename
        return StreamingResponse(io.BytesIO(audio), media_type="audio/mpeg")
    
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print("Full Error Traceback:\n", error_details) 
        logger.log_error(f"Error generating audio: {str(e)}")
        return {"error": str(e)}  

