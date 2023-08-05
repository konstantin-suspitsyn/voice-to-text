from transformers import logging
from model.vosk_recasepunc.recasepunc import CasePuncPredictor
from model.vosk_recasepunc.recasepunc import WordpieceTokenizer
from model.vosk_recasepunc.recasepunc import Config


class SetPunctuation:
    def __init__(self, text: str):
        # self.text = text
        logging.set_verbosity_error()
        self.predictor = CasePuncPredictor(r"model/vosk_recasepunc/checkpoint", lang="ru")
        self.tokens = list(enumerate(self.predictor.tokenize(text)))

    def insert_punctuation(self):
        results = ""
        for token, case_label, punc_label in self.predictor.predict(self.tokens, lambda x: x[1]):
            prediction = self.predictor.map_punc_label(self.predictor.map_case_label(token[1], case_label), punc_label)
            if token[1][0] != '#':
                results = results + ' ' + prediction
            else:
                results = results + prediction

        results = results.strip()

        return results


