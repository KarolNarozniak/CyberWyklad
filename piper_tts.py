import requests


class PiperTTS:
    def __init__(self, url: str) -> None:
        self.url = url

    def get_audio(self, text: str) -> bytes:
        data={"text": text}
        response = requests.post(self.url, json=data)
        return response.content

    def save_to_file(self, text: str, file_path: str) -> None:
        audio = self.get_audio(text)
        with open(file_path, 'wb') as file:
            file.write(audio)

