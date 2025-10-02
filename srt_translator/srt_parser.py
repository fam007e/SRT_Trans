import re
import pysrt
from nltk.tokenize import sent_tokenize
from langdetect import detect, DetectorFactory
from langdetect.lang_detect_exception import LangDetectException

# Ensure reproducibility for langdetect
DetectorFactory.seed = 0

class SrtParser:
    def __init__(self, input_file):
        self.subs = pysrt.open(input_file, encoding='utf-8')

    def get_subtitles_text(self):
        return [sub.text for sub in self.subs]

    def update_subtitles_text(self, translated_texts):
        for i, sub in enumerate(self.subs):
            sub.text = translated_texts[i]

    def write_srt(self, output_file):
        self.subs.save(output_file, encoding='utf-8')

    @staticmethod
    def clean_text(text):
        tags = []
        # Find all HTML tags and replace them with placeholders
        def replace_tag(match):
            tag = match.group(0)
            placeholder = f'__TAG_{len(tags)}__'
            tags.append((placeholder, tag))
            return placeholder

        cleaned_text = re.sub(r'<[^>]*>', replace_tag, text)
        # Remove multiple spaces
        cleaned_text = re.sub(r'\s+', ' ', cleaned_text)
        return cleaned_text.strip(), tags

    @staticmethod
    def reinsert_tags(text, tags):
        # Reinsert HTML tags from placeholders
        for placeholder, tag in tags:
            text = text.replace(placeholder, tag)
        return text

    @staticmethod
    def split_into_sentences(text):
        return sent_tokenize(text)

    @staticmethod
    def detect_language(text):
        try:
            return detect(text)
        except LangDetectException:
            return 'unknown'
