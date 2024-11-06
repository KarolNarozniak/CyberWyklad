import os
import uuid
import requests  # Import requests for direct API calls

# Define constants
XI_API_KEY = os.getenv("XI_API_KEY")
VOICE_ID = "pNInz6obpgDQGcFmaJgB"  # Pre-made voice ID
TEXT_TO_SPEAK = "Quantum cryptography is about using the principles of quantum mechanics to secure communication, ensuring data confidentiality by making eavesdropping detectable. It primarily leverages quantum key distribution (QKD), where quantum particles like photons create encryption keys that are virtually impossible to intercept without being noticed."

# Set up the Eleven Labs API URL and headers
tts_url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}/stream"
headers = {
    "xi-api-key": XI_API_KEY,
    "Accept": "application/json"
}

# Set up data payload
data = {
    "text": TEXT_TO_SPEAK,
    "model_id": "eleven_turbo_v2_5",
    "voice_settings": {
        "stability": 0.5,
        "similarity_boost": 0.5,
        "style": 0.5,
        "use_speaker_boost": True
    }
}

def text_to_speech_file(text: str) -> str:
    # Make POST request with streaming to save audio in chunks
    response = requests.post(tts_url, headers=headers, json=data, stream=True)

    # Generate a unique filename
    save_file_path = f"{uuid.uuid4()}.mp3"

    # Check for successful request
    if response.ok:
        # Write audio to file
        with open(save_file_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=1024):
                f.write(chunk)
        print(f"{save_file_path}: A new audio file was saved successfully!")
    else:
        print("Error:", response.text)

    return save_file_path

# Call the function
text_to_speech_file(TEXT_TO_SPEAK)
