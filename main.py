import requests
import pypdf
import os
from dotenv import load_dotenv

load_dotenv()

CHUNK_SIZE = 1024
PDF_PATH = "test.pdf"

VOICE_ID = os.getenv("VOICE_ID")
API_KEY = os.getenv("API_KEY")


class Converter:

    def __init__(self, voice_id: str, api_key: str, filename: str):
        self.url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
        self.filename = filename
        self.data = None

        self.header = {"Accept": "audio/mpeg",
                       "Content-Type": "application/json",
                       "xi-api-key": api_key
                       }

    def convert_to_mp3(self, text: str):
        self.data = {
            "text": text,
            "model_id": "eleven_monolingual_v1",
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.5
            }
        }
        response = requests.post(self.url, json=self.data, headers=self.header)
        with open(f'{self.filename}.mp3', 'wb') as f:
            for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
                if chunk:
                    f.write(chunk)


def main():
    converter = Converter(voice_id=VOICE_ID,
                          api_key=API_KEY,
                          filename="output"
                          )

    reader = pypdf.PdfReader("test.pdf")

    text = ""
    for page in reader.pages:
        text += page.extract_text()

    converter.convert_to_mp3(text=text)


if __name__ == "__main__":
    main()
