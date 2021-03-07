from transformers import MarianTokenizer, MarianMTModel
from django.conf import settings
import os
from typing import List


class Translator():
    def __init__(self):
        self.models = {}
        self.models_dir = settings.MODEL_PATH
        self.load_model('en', 'de')

    def get_supported_langs(self):
        routes = [x.split('-')[-2:] for x in os.listdir(self.models_dir)]
        return routes

    def load_model(self, source, target):
        route = f'{source}-{target}'
        model = f'opus-mt-{route}'
        path = os.path.join(self.models_dir, model)
        try:
            model = MarianMTModel.from_pretrained(path)
            tok = MarianTokenizer.from_pretrained(path)
        except:
            return False, f"Make sure you have downloaded model for {route} translation"
        self.models[route] = (model, tok)
        return True, f"Successfully loaded model for {route} transation"

    def translate(self, source, target, text):

        route = f'{source}-{target}'
        batch = self.models[route][1].prepare_seq2seq_batch(
            src_texts=text, return_tensors="pt", padding=True)
        gen = self.models[route][0].generate(**batch)
        words: List[str] = self.models[route][1].batch_decode(
            gen, skip_special_tokens=True)
        return words
