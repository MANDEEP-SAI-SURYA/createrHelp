import os
import assemblyai as aai
from dotenv import load_dotenv

load_dotenv()

aai.settings.api_key = os.getenv("ASSEMBLYAI_API_KEY")

def transcribe_audio(audio_path):

    config = aai.TranscriptionConfig(
        speech_models=[
            "universal-2"
        ]
    )

    transcript = aai.Transcriber().transcribe(
        audio_path,
        config=config
    )

    print("STATUS:", transcript.status)
    print("ERROR:", transcript.error)

    if transcript.error:
        raise Exception(transcript.error)

    return transcript.text