import uuid
import os
from dotenv import load_dotenv

from deepgram import (
    DeepgramClient,
    SpeakOptions,
)

load_dotenv()


def text2speech(text: str) -> str:
    filename = str(uuid.uuid4()) + '.wav'
    try:
        speak_options = {"text": text}

        # STEP 1: Create a Deepgram client using the API key from environment variables
        deepgram = DeepgramClient(api_key=os.getenv("DG_API_KEY"))

        # STEP 2: Configure the options (such as model choice, audio configuration, etc.)
        options = SpeakOptions(
            model="aura-orion-en",
            encoding="linear16",
            container="wav"
        )

        # STEP 3: Call the save method on the speak property
        deepgram.speak.v("1").save(filename, speak_options, options)
        return filename

    except Exception as e:
        return 'can_you_repeat_please.wav'


if __name__ == "__main__":
    print(text2speech('This is a test text to be converted to speech'))
