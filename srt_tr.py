"""
A script to translate subtitle files (.srt) from one language to another.
"""

import argparse
import os
import re
import sys
from dataclasses import dataclass
import chardet
from deep_translator import GoogleTranslator
from deep_translator.exceptions import TranslationNotFound
from tqdm import tqdm

@dataclass
class Subtitle:
    """Represents a single subtitle block."""
    index: int
    start: str
    end: str
    text: str

    def __str__(self):
        return f"{self.index}\n{self.start} --> {self.end}\n{self.text}\n"

def detect_encoding(file_path):
    """Detects the encoding of a file."""
    with open(file_path, 'rb') as f:
        result = chardet.detect(f.read())
    return result['encoding']

def parse_srt(file_path):
    """
    Parses an SRT file and returns a list of Subtitle objects.
    This parser is designed to be robust against common formatting errors.
    """
    try:
        encoding = detect_encoding(file_path)
        if not encoding:
            encoding = 'utf-8'  # Default to utf-8 if detection fails
        with open(file_path, 'r', encoding=encoding, errors='replace') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Error: Input file not found at {file_path}", file=sys.stderr)
        return None
    except IOError as e:
        print(f"Error reading file: {e}", file=sys.stderr)
        return None

    # Regex to capture index, start time, end time, and text of a subtitle block.
    # It handles optional index and variations in newlines.
    subtitle_pattern = re.compile(
        r'(\d+)?\s*'
        r'(\d{2}:\d{2}:\d{2},\d{3})\s*-->\s*(\d{2}:\d{2}:\d{2},\d{3})\s*'
        r'([\s\S]*?)(?=\n\n|\Z)',
        re.MULTILINE
    )

    subtitles = []
    for match in subtitle_pattern.finditer(content):
        index = int(match.group(1)) if match.group(1) else len(subtitles) + 1
        start = match.group(2)
        end = match.group(3)
        text = match.group(4).strip()
        if text:
            subtitles.append(Subtitle(index, start, end, text))

    if not subtitles:
        print("Warning: No subtitles found in the file.", file=sys.stderr)

    return subtitles

def translate_subtitle_block(text, source_language, target_language):
    """
    Translates a single block of subtitle text, preserving HTML tags.
    Detects language automatically for each block if source_language is 'auto'.
    """
    if not text.strip():
        return text

    # Preserve HTML tags by replacing them with placeholders
    tags = re.findall(r'<[^>]+>', text)
    text_without_tags = re.sub(r'<[^>]+>', ' ', text)

    try:
        translator = GoogleTranslator(source=source_language, target=target_language)
        translated_text = translator.translate(text_without_tags)
        if translated_text:
            # Restore HTML tags
            for tag in tags:
                translated_text = f"{tag}{translated_text}{tag}"
            return translated_text
        return text  # Return original text if translation is empty
    except TranslationNotFound as e:
        print(f"Error: Invalid language code. {e}", file=sys.stderr)
        # Return original text if language is not supported
        return text
    except Exception as e: # pylint: disable=broad-except
        # Catching broad exception to handle various translator API errors
        # and prevent the script from crashing.
        print(f"Warning: Could not translate block: '{text[:30]}...'. Error: {e}", file=sys.stderr)
        return text # Return original text on any translation error

def translate_srt_file(input_file, target_language, source_language='auto', output_file=None):
    """Translates the subtitles in the input .srt file."""
    subtitles = parse_srt(input_file)
    if not subtitles:
        return

    translated_subtitles = []
    failed_translations = 0

    for sub in tqdm(subtitles, desc="Translating", unit="subtitle"):
        translated_text = translate_subtitle_block(sub.text, source_language, target_language)
        if translated_text == sub.text and sub.text.strip():
            failed_translations += 1

        translated_subtitles.append(Subtitle(sub.index, sub.start, sub.end, translated_text))

    if failed_translations > 0:
        print(f"Warning: {failed_translations}/{len(subtitles)} blocks failed.", file=sys.stderr)

    if not output_file:
        base, _ = os.path.splitext(input_file)
        output_file = f"{base}_trs_{target_language}.srt"

    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            for sub in translated_subtitles:
                f.write(str(sub) + '\n')
        print(f"Translation completed! Output saved to {output_file}")
    except IOError as e:
        print(f"Error writing to output file: {e}", file=sys.stderr)

def main():
    """Main function to parse arguments and run the translation."""
    parser = argparse.ArgumentParser(
        description='Translate subtitles from one language to another.',
        formatter_class=argparse.RawTextHelpFormatter,
        epilog='''
Language codes examples:
  en - English
  bn - Bangla
  es - Spanish
  fr - French
  de - German
  zh - Chinese
  ja - Japanese
  ko - Korean
  ru - Russian
  hi - Hindi
'''
    )
    parser.add_argument('input_file', help='Input .srt file path')
    parser.add_argument('target_language', help='Language code to output (e.g., bn for Bangla)')
    parser.add_argument('-s', '--source_language', default='auto',
                        help='Language code for input (default: auto)')
    parser.add_argument('-o', '--output_file', help='Output .srt file path')
    args = parser.parse_args()

    translate_srt_file(args.input_file, args.target_language,
                       args.source_language, args.output_file)

if __name__ == "__main__":
    main()
