import argparse
import os
from .srt_parser import SrtParser
from .translators import GoogleTranslate, DeepLTranslate
from tqdm import tqdm

def translate_single_srt(input_file, output_lang, source_lang, translator_service, output_dir=None):
    try:
        # Parse SRT
        srt_parser = SrtParser(input_file)
        original_subtitle_blocks = srt_parser.get_subtitles_text()

        # Initialize translator
        if translator_service == 'google':
            translator = GoogleTranslate()
        elif translator_service == 'deepl':
            translator = DeepLTranslate()
        else:
            raise ValueError(f"Unknown translator: {translator_service}")

        translated_subtitle_blocks = []

        for original_text in original_subtitle_blocks:
            # Clean text and extract tags
            cleaned_text, tags = SrtParser.clean_text(original_text)
            sentences = SrtParser.split_into_sentences(cleaned_text)

            translated_sentences = []
            for sentence in sentences:
                detected_lang = SrtParser.detect_language(sentence)

                # Determine source language for this sentence
                current_source_lang = source_lang
                if source_lang == 'auto' and detected_lang != 'unknown':
                    current_source_lang = detected_lang
                elif source_lang != 'auto' and detected_lang != 'unknown' and detected_lang != source_lang:
                    # If user specified source_lang, but a different language is detected,
                    # we still try to translate from the detected language for better results.
                    # This is a heuristic and can be refined.
                    current_source_lang = detected_lang

                # Translate sentence
                translated_sentence = translator.translate(sentence, output_lang, current_source_lang)
                translated_sentences.append(translated_sentence)

            # Reassemble translated sentences
            translated_cleaned_text = " ".join(translated_sentences)

            # Reinsert tags into the fully translated text
            final_translated_text = SrtParser.reinsert_tags(translated_cleaned_text, tags)
            translated_subtitle_blocks.append(final_translated_text)

        # Update and save SRT
        srt_parser.update_subtitles_text(translated_subtitle_blocks)

        # Determine output file path
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
            base_name = os.path.basename(input_file)
            base, ext = os.path.splitext(base_name)
            output_file = os.path.join(output_dir, f'{base}_{output_lang}{ext}')
        else:
            base, ext = os.path.splitext(input_file)
            output_file = f'{base}_{output_lang}{ext}'

        srt_parser.write_srt(output_file)
        return f'Translated {input_file} to {output_file}'

    except FileNotFoundError:
        return f'Error: Input file not found at {input_file}'
    except ValueError as ve:
        return f'Configuration Error for {input_file}: {ve}'
    except Exception as e:
        return f'An error occurred for {input_file}: {e}'

def main():
    parser = argparse.ArgumentParser(description='Translate SRT subtitle files.')
    parser.add_argument('input_paths', type=str, nargs='+',
                        help='Path(s) to input SRT files or directories containing SRT files.')
    parser.add_argument('output_lang', type=str, help='Target language for translation (e.g., en, es, fr).')
    parser.add_argument('--source_lang', type=str, default='auto',
                        help='Source language for translation (e.g., en, es, fr). Defaults to auto-detect.')
    parser.add_argument('--translator', type=str, default='google', choices=['google', 'deepl'],
                        help='Translation service to use (google or deepl). Defaults to google.')
    parser.add_argument('--output_dir', type=str,
                        help='Directory to save translated files. If not provided, files are saved next to originals.')

    args = parser.parse_args()

    srt_files_to_translate = []
    for path in args.input_paths:
        if os.path.isfile(path) and path.lower().endswith('.srt'):
            srt_files_to_translate.append(path)
        elif os.path.isdir(path):
            for root, _, files in os.walk(path):
                for file in files:
                    if file.lower().endswith('.srt'):
                        srt_files_to_translate.append(os.path.join(root, file))

    if not srt_files_to_translate:
        print("No SRT files found to translate.")
        return

    print(f'Translating {len(srt_files_to_translate)} SRT file(s) to {args.output_lang} using {args.translator}...')

    results = []
    for srt_file in tqdm(srt_files_to_translate, desc="Translating SRT files"):
        result = translate_single_srt(srt_file, args.output_lang, args.source_lang, args.translator, args.output_dir)
        results.append(result)

    print("\n--- Translation Summary ---")
    for res in results:
        print(res)

if __name__ == '__main__':
    main()
