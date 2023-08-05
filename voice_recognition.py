import json
import os.path
import subprocess

from vosk import Model, KaldiRecognizer, SetLogLevel
from file_management import FileManager
from punctuation import SetPunctuation
from model.vosk_recasepunc.recasepunc import WordpieceTokenizer


class ConvertToText:
    CHANNELS = 1
    FRAME_RATE = 16000

    def __init__(self, vosk_voice_recognition_path: str, vosk_punctuation_model: str) -> None:
        self.file_management = FileManager()

        model = Model(vosk_voice_recognition_path)
        self.rec = KaldiRecognizer(model, self.FRAME_RATE)
        self.rec.SetWords(True)

        SetLogLevel(0)

    def convert_one_audio_to_text(self, filepath: str) -> str:

        with subprocess.Popen(["ffmpeg", "-loglevel", "quiet", "-i",
                               filepath,
                               "-ar", str(self.FRAME_RATE), "-ac", "1", "-f", "s16le", "-"],
                              stdout=subprocess.PIPE) as process:

            while True:
                data = process.stdout.read(4000)
                if len(data) == 0:
                    break
                if self.rec.AcceptWaveform(data):
                    self.rec.Result()
                else:
                    self.rec.PartialResult()

            text = json.loads(self.rec.FinalResult())["text"]

            return text

    def convert_all_audios(self):
        for i, file_path in enumerate(self.file_management.get_list_of_files()[self.file_management.INPUT_PATHS_KEY]):
            text = self.convert_one_audio_to_text(file_path)
            text_with_punctuation = SetPunctuation(text).insert_punctuation()

            save_path = os.path.join(self.file_management.get_list_of_files()[self.file_management.OUTPUT_PATH_KEY],
                                     self.file_management.get_list_of_files()[self.file_management.OUTPUT_NAMES][i])

            with open(save_path, "w") as f:
                f.write(text_with_punctuation)


if __name__ == "__main__":
    c = ConvertToText(r"model/vosk-model-ru-0.42", r"model/vosk-recasepunc-ru-0.22")
    c.convert_all_audios()
