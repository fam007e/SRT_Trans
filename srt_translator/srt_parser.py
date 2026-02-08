"""
SRT Parser - Handles reading, parsing, and writing SRT subtitle files.
Also provides utility methods for text cleaning and language detection.
"""
import re
import pysrt
from nltk.tokenize import sent_tokenize
from langdetect import detect, DetectorFactory
from langdetect.lang_detect_exception import LangDetectException

# Alias Subtitle to pysrt.SubRipItem for test compatibility
Subtitle = pysrt.SubRipItem

# Ensure reproducibility for langdetect
DetectorFactory.seed = 0

class SrtParser:
    """
    Parser for SRT files using pysrt.
    """
    def __init__(self, input_file):
        """Initialize parser with an input SRT file."""
        self.subs = pysrt.open(input_file, encoding='utf-8')

    def get_subtitles_text(self):
        """Return a list of text content from all subtitles."""
        return [sub.text for sub in self.subs]

    def get_subtitles_text_blocks(self):
        """Return the list of SubRipItem objects."""
        return self.subs

    @staticmethod
    def detect_encoding(file_path):
        """Detect file encoding using chardet."""
        import chardet  # pylint: disable=import-outside-toplevel
        with open(file_path, 'rb') as f:
            result = chardet.detect(f.read())
        return result['encoding']

    def update_subtitles_text(self, translated_texts):
        """Update subtitle objects with new translated text."""
        for i, sub in enumerate(self.subs):
            sub.text = translated_texts[i]

    def write_srt(self, output_file):
        """Save the subtitles to a file in UTF-8 encoding."""
        self.subs.save(output_file, encoding='utf-8')

    @staticmethod
    def clean_text(text):
        """
        Extract HTML tags and return cleaned text with placeholders.

        Args:
            text: Original subtitle text with HTML tags.

        Returns:
            Tuple of (cleaned_text, tags_list).
        """
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
        """Reinsert HTML tags into translated text using placeholders."""
        # Reinsert HTML tags from placeholders
        for placeholder, tag in tags:
            text = text.replace(placeholder, tag)
        return text

    @staticmethod
    def split_into_sentences(text):
        """Split text into sentences using NLTK."""
        return sent_tokenize(text)

    @staticmethod
    def detect_language(text):
        """Detect language code of the given text."""
        try:
            return detect(text)
        except LangDetectException:
            return 'unknown'
