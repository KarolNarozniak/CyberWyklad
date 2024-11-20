""" Script with TextToSpeechModule and usage example """

import os
import shutil
from datetime import datetime
from typing import List

import FilterModule
from piper_tts import PiperTTS


class TextToSpeechModule:
    """ Class responsible for converting text to speech. It takes text file with lecture content and converts it to
    audio files with a speech"""

    def __init__(self, input_text: str, audio_dir: str, backup_audio_dir: str,
                 audio_file_prefix: str, llm_model_name: str, llm_base_url: str) -> None:
        # setup TTS engine
        self.engine = PiperTTS('https://piper-tts.rosowski.me/speech/')
        # self.engine = pyttsx3.init()
        # self.engine.setProperty('rate', 150)
        # self.engine.setProperty('volume', 0.9)
        # self.engine.setProperty('voice', self.engine.getProperty('voices')[0].id)
        self.input_text = input_text
        self.audio_file_prefix = audio_file_prefix
        self.audio_dir = audio_dir
        self.backup_audio_dir = backup_audio_dir
        self.llm_model_name = llm_model_name
        self.llm_base_url = llm_base_url

    def backup_audio_folder(self) -> None:
        """ Backup audio folder to clear it for new audio """
        # make sure folders exists
        os.makedirs(self.audio_dir, exist_ok=True)
        os.makedirs(self.backup_audio_dir, exist_ok=True)

        # Back up all audio files from audio_folder if exists
        if any(os.scandir(self.audio_dir)):
            current_backup_folder_name = f'audio_backup_{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}'
            current_backup_folder_path = os.path.join(self.backup_audio_dir, current_backup_folder_name)
            os.makedirs(current_backup_folder_path)
            for file_name in os.listdir(self.audio_dir):
                shutil.copy(os.path.join(self.audio_dir, file_name), current_backup_folder_path)

        # Remove all files from the audio folder
        for file_name in os.listdir(self.audio_dir):
            os.remove(os.path.join(self.audio_dir, file_name))

        print('Audio folder cleared')

    def get_text(self) -> str:
        """ Get text that will be said """
        return self.input_text

    def filter_text(self, text: str) -> List[str]:
        """ Filter text """
        filter_fs = FilterModule.Filter(text, self.llm_model_name, base_url=self.llm_base_url)
        return filter_fs.get_presentations_splited()

    def save_recording(self, text: str, out_file: str) -> None:
        """ Generate Lecturer Recording based on the text """
        print("Saving text:")
        print(text)
        self.engine.save_to_file(text, os.path.join(self.audio_dir, out_file))
        # self.engine.runAndWait()

    def generate_tts_audio(self) -> None:
        """ Get the text for Lecturer and generate his speak recording """
        self.backup_audio_folder()
        presentation_text = self.get_text()
        filtered_presentation_texts = self.filter_text(self.input_text)

        for i, self.input_text in enumerate(filtered_presentation_texts):
            self.save_recording(self.input_text, f'{self.audio_file_prefix}_{i + 1}.wav')


if __name__ == '__main__':
    INPUT_TEXT = '''------>[cos]<------
        Wstęp: Czym jest informatyka kwantowa?
        Dzień dobry Państwu, cieszę się, że mogę dziś opowiedzieć o jednym z najbardziej ekscytujących obszarów współczesnej
        nauki – informatyce kwantowej. Może na początek przypomnę, czym w ogóle jest ta „kwantowość”, o której tak często ostatnio słyszymy.
        ------>[cos]<------
        Klasyczne komputery – te, które wszyscy znamy – opierają się na bitach, które mogą przyjmować wartość 0 albo 1.
        Natomiast w komputerze kwantowym pracujemy na kubitach. Kubit to coś, co może być jednocześnie 0 i 1 – i to właśnie
        dzięki tej właściwości komputery kwantowe mają potencjał do wykonywania pewnych zadań znacznie szybciej niż tradycyjne.
        ------>[cos]<------
        Superpozycja: Klucz do kwantowej mocy obliczeniowej
        Superpozycja to zjawisko, które brzmi niemal jak science fiction, ale jest bardzo realne. Wyobraźmy sobie, że klasyczny
        bit jest jak żarówka – może być włączona (1) albo wyłączona (0).
        '''
    PRESENTATION_AUDIO_DIR = 'presentation_audio_parts'
    BACKUP_AUDIO_DIR = 'backup_audio_parts'

    text_to_speech_module = TextToSpeechModule(
        INPUT_TEXT, PRESENTATION_AUDIO_DIR, BACKUP_AUDIO_DIR)

    text_to_speech_module.generate_tts_audio()
