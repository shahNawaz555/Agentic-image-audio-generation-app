from pydub import AudioSegment
import requests
import json
import os
import base64
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# Constants
XI_API_KEY = "sk_718b690509ab6bf0c6d7e524101008866e0fa14a926554a5"

VOICE_IDS = [
    "9BWtsMINqrJLrRacOk9x", "CwhRBWXzGAHq8TQ4Fs17", "EXAVITQu4vr4xnSDxMaL",
    "FGY2WhTYpPnrIDTdsKH5", "IKne3meq5aSn9XLyUdCD", "JBFqnCBsd6RMkjVDRZzb",
    "N2lVS1w4EtoT3dr4eOWO", "SAz9YHcvj6GT2YYXdXww", "TX3LPaxmHKxFdv7VOQHJ",
    "XB0fDUnXU5powFXDhCwa", "Xb7hH8MSUJpSbSDYk0k2", "XrExE9yKIg1WjnnlVkGX",
    "bIHbv24MWmeRgasZH58o", "cgSgspJ2msm6clMCkdW9", "cjVigY5qzO86Huf0OWal",
    "iP95p4xoKVk53GoZ742B", "nPczCjzI2devNBz1zQrb", "onwK4e9ZLuTAKqWW03F9",
    "pFZP5JQG7iQjIQuC4Bku", "pqHfZKP75CvOlQylNhV4"
]

class AudioGenerationAgent:
    def __init__(self):
        self.session = requests.Session()
        retries = Retry(total=5, backoff_factor=1, status_forcelist=[502, 503, 504])
        self.session.mount('https://', HTTPAdapter(max_retries=retries))
        self.voice_ids = {}

    def generate_audio(self, character, text, voice_id, output_dir):
        os.makedirs(output_dir, exist_ok=True)
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}/with-timestamps"
        data = {"text": text, "model_id": "eleven_multilingual_v2"}
        headers = {
            "xi-api-key": XI_API_KEY,
            "Content-Type": "application/json"
        }

        response = self.session.post(url, json=data, headers=headers)

        if response.status_code == 200:
            response_json = response.json()
            if "audio_base64" in response_json:
                # Decode base64-encoded audio and save as MP3
                audio_content = base64.b64decode(response_json["audio_base64"])
                audio_file_path = os.path.join(output_dir, f"{character}_{len(text)}.mp3")
                with open(audio_file_path, "wb") as audio_file:
                    audio_file.write(audio_content)
                return audio_file_path  # Return the path of the generated audio file
            else:
                print(f"Warning: No audio data received for {character}.")
        else:
            print(f"Failed to generate audio for {character}. Status: {response.status_code}")
            print(f"Response Content: {response.text}")
        return None

    def read_dialogues(self, json_file):
        with open(json_file, 'r') as file:
            data = json.load(file)
            return data.get("dialogues", {})

    def process_dialogues(self, json_file, output_dir):
        dialogues = self.read_dialogues(json_file)
        self.voice_ids = self.assign_voice_ids(dialogues)
        audio_files = []  # List to keep track of audio file paths in dialogue order

        for character, lines in dialogues.items():
            for line in lines:
                voice_id = self.get_voice_id(character)
                audio_file_path = self.generate_audio(character, line, voice_id, output_dir)
                if audio_file_path:
                    audio_files.append(audio_file_path)  # Append audio path in order

        self.concatenate_audio_files(audio_files, output_dir)

    def get_voice_id(self, character):
        return self.voice_ids.get(character)

    def assign_voice_ids(self, dialogues):
        voice_ids = {}
        for i, character in enumerate(dialogues.keys()):
            voice_ids[character] = VOICE_IDS[i % len(VOICE_IDS)]
        return voice_ids

    def concatenate_audio_files(self, audio_files, output_dir):
        combined_audio = AudioSegment.empty()
        for file_path in audio_files:
            segment = AudioSegment.from_file(file_path)
            combined_audio += segment

        # Save the combined audio file
        combined_audio_file_path = os.path.join(output_dir, "complete_audio_story.mp3")
        combined_audio.export(combined_audio_file_path, format="mp3")
        print(f"Concatenated audio saved as {combined_audio_file_path}")

# Example usage
if __name__ == "__main__":
    agent = AudioGenerationAgent()
    output_directory = r"E:\agent_storage\audio"
    json_file = "audio_agent_data.json"  # JSON file containing dialogues
    agent.process_dialogues(json_file, output_directory)