""" Script with TextToSpeechModule and usage example """

import os
import shutil
from datetime import datetime
from typing import List

import pyttsx3


class TextToSpeechModule:
    """ Class responsible for converting text to speech. It takes text file with lecture content and converts it to
    audio files with a speech"""

    def __init__(self, input_data_dir: str, input_text_file: str, audio_dir: str, backup_audio_dir: str) -> None:
        # setup TTS engine
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150)
        self.engine.setProperty('volume', 0.9)
        self.engine.setProperty('voice', self.engine.getProperty('voices')[0].id)

        # setup folders paths and file names
        self.input_data_dir = input_data_dir
        self.input_text_file = input_text_file
        self.audio_dir = audio_dir
        self.backup_audio_dir = backup_audio_dir

        # TODO: use implemented filter
        self.filter = lambda text: text.split('\n')

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
        input_file = os.path.join(self.input_data_dir, self.input_text_file)
        print("Getting text from file ", input_file)
        with open(input_file, encoding='utf-8') as f:
            return f.read()

    def filter_text(self, text: str) -> List[str]:
        """ Filter text """
        filtered_texts = self.filter(text)
        print("Filtered text: ", filtered_texts)
        return filtered_texts

    def save_recording(self, text: str, out_file: str) -> None:
        """ Generate Lecturer Recording based on the text """
        print("Saving text:")
        print(text)
        self.engine.save_to_file(text, os.path.join(self.audio_dir, out_file))
        self.engine.runAndWait()

    def generate_tts_audio(self) -> None:
        """ Get the text for Lecturer and generate his speak recording """
        self.backup_audio_folder()
        presentation_text = self.get_text()
        filtered_presentation_texts = self.filter_text(presentation_text)

        for i, presentation_text in enumerate(filtered_presentation_texts):
            self.save_recording(presentation_text, f'presentation_number_{i + 1}.mp3')


if __name__ == '__main__':
    INPUT_DATA_DIR = 'input_data'
    INPUT_TEXT_FILE = 'sample_presentation_text_no_separators.txt'
    PRESENTATION_AUDIO_DIR = 'presentation_audio_parts'
    BACKUP_AUDIO_DIR = 'backup_audio_parts'

    text_to_speech_module = TextToSpeechModule(
        INPUT_DATA_DIR, INPUT_TEXT_FILE, PRESENTATION_AUDIO_DIR, BACKUP_AUDIO_DIR)

    text_to_speech_module.generate_tts_audio()
