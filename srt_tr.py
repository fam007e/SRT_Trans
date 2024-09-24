"""A script to translate subtitle files (.srt) from one language to another."""

import argparse
import os
import re
from deep_translator import GoogleTranslator
from tqdm import tqdm

def translate_srt(input_file, source_language, target_language):
    """Translate the subtitles in the input .srt file."""

    translator = GoogleTranslator(source=source_language, target=target_language)

    try:
        with open(input_file, 'r', encoding='utf-8') as infile:
            lines = infile.readlines()
    except UnicodeDecodeError:
        with open(input_file, 'r', encoding='iso-8859-1') as infile:
            lines = infile.readlines()

    translated_lines = []
    for line in tqdm(lines, desc="Translating", unit=" line"):
        stripped_line = line.strip()
        if (re.match(r'^\d+$', stripped_line) or
                re.match(r'^\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}$', stripped_line) or
                stripped_line == ""):
            translated_lines.append(line)
        else:
            translated_text = translator.translate(stripped_line)
            translated_lines.append(translated_text + "\n")

    output_file = os.path.splitext(input_file)[0] + f"_trs_{target_language}.srt"
    with open(output_file, 'w', encoding='utf-8') as outfile:
        outfile.writelines(translated_lines)

    print(f"Translation completed! Output saved to {output_file}")

if __name__ == "__main__":
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
    parser.add_argument('source_language', help='Language code for input (e.g., en for English)')
    parser.add_argument('target_language', help='Language code to output (e.g., bn for Bangla)')
    args = parser.parse_args()

    translate_srt(args.input_file, args.source_language, args.target_language)
