import os
from abc import ABC, abstractmethod
from googletrans import Translator as GoogleTranslator
from deep_translator import DeeplTranslator

class BaseTranslator(ABC):
    @abstractmethod
    def translate(self, text, dest_lang, src_lang=None):
        pass

class GoogleTranslate(BaseTranslator):
    def __init__(self):
        self.translator = GoogleTranslator()

    def translate(self, text, dest_lang, src_lang=None):
        if isinstance(text, list):
            return [self.translator.translate(t, dest=dest_lang, src=src_lang).text for t in text]
        else:
            return self.translator.translate(text, dest=dest_lang, src=src_lang).text

class DeepLTranslate(BaseTranslator):
    def __init__(self):
        api_key = os.getenv("DEEPL_API_KEY")
        if not api_key:
            raise ValueError("DeepL API key not found. Please set the DEEPL_API_KEY environment variable.")
        self.translator = DeeplTranslator(api_key=api_key)

    def translate(self, text, dest_lang, src_lang=None):
        if isinstance(text, list):
            return self.translator.translate(text, target=dest_lang, source=src_lang)
        else:
            return self.translator.translate(text, target=dest_lang, source=src_lang)
