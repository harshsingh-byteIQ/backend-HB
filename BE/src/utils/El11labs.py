import os
from elevenlabs.client import ElevenLabs  # type: ignore
from elevenlabs import play, save, stream, Voice, VoiceSettings  # type: ignore
from dotenv import load_dotenv  # type: ignore

load_dotenv()

# Elevenlabs_api_key = os.getenv('ELEVENLABS_API_KEY')
# print(f'Elevenlabs_api_key: f{Elevenlabs_api_key}')

class Eleve11labs:
    def __init__(self, api_key: str):
        self.client = ElevenLabs(api_key=api_key)

    def generate(self, text: str, filename: str = "audio1.mp3"):
        audio_generator = self.client.generate(
            text=text,
            stream=False,
            voice=Voice(
                voice_id='nPczCjzI2devNBz1zQrb',
                settings=VoiceSettings(
                    stability=0.8, similarity_boost=0.6, style=0.9, use_speaker_boost=True)
            )
        )
        audio_bytes = b"".join(audio_generator)
        return audio_bytes

# # For checking
# elaoven = Eleve11labs(api_key = Elevenlabs_api_key)
# test_text = "hello praveen"
# audio = elaoven.generate(test_text)
# play(audio)
# save(audio, 'audio1.mp3')
