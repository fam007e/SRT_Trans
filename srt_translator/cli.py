"""
SRT Translator CLI - Command-line interface for translating SRT subtitle files.
Supports multiple translation services, concurrent processing, and batch operations.
"""
import argparse
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
from .srt_parser import SrtParser
from .translators import get_translator, get_supported_languages, validate_language_code


def translate_block(block_data):
    """
    Translate a single subtitle block.

    Args:
        block_data: Tuple of (index, text, translator, output_lang, source_lang)

    Returns:
        Tuple of (index, translated_text)
    """
    idx, original_text, translator, output_lang, source_lang = block_data

    try:
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
                current_source_lang = detected_lang

            # Translate sentence
            translated_sentence = translator.translate(sentence, output_lang, current_source_lang)
            translated_sentences.append(translated_sentence)

        # Reassemble translated sentences
        translated_cleaned_text = " ".join(translated_sentences)

        # Reinsert tags into the fully translated text
        final_translated_text = SrtParser.reinsert_tags(translated_cleaned_text, tags)
        return (idx, final_translated_text)
    except Exception:
        # On error, return original text
        return (idx, original_text)


def translate_single_srt(input_file, output_lang, source_lang, translator_service, *,
                         output_dir=None, workers=1, _batch_size=10):
    """
    Translate a single SRT file.

    Args:
        input_file: Path to input SRT file
        output_lang: Target language code
        source_lang: Source language code ('auto' for detection)
        translator_service: 'google', 'deepl', or 'mymemory'
        output_dir: Optional output directory
        workers: Number of concurrent workers (1 = sequential)
        batch_size: Sentences per batch (for future batch API support)

    Returns:
        Status message string
    """
    try:
        # Validate target language code
        if not validate_language_code(output_lang):
            raise ValueError(f"'{output_lang}' may not be a valid language code. Use --list-languages to see supported codes.")

        # Parse SRT
        srt_parser = SrtParser(input_file)
        original_subtitle_blocks = srt_parser.get_subtitles_text()
        total_blocks = len(original_subtitle_blocks)

        if total_blocks == 0:
            return f'Warning: No subtitles found in {input_file}'

        # Initialize translator using factory function
        translator = get_translator(translator_service)

        # Prepare work items
        work_items = [
            (i, text, translator, output_lang, source_lang)
            for i, text in enumerate(original_subtitle_blocks)
        ]

        # Translate with concurrency if workers > 1
        if workers > 1 and total_blocks > 10:
            translated_subtitle_blocks = [None] * total_blocks
            with ThreadPoolExecutor(max_workers=workers) as executor:
                futures = {executor.submit(translate_block, item): item[0] for item in work_items}
                for future in tqdm(as_completed(futures), total=total_blocks,
                                   desc=f"  {os.path.basename(input_file)}", leave=False):
                    idx, translated_text = future.result()
                    translated_subtitle_blocks[idx] = translated_text
        else:
            # Sequential translation with progress
            translated_subtitle_blocks = []
            for item in tqdm(work_items, desc=f"  {os.path.basename(input_file)}", leave=False):
                _, translated_text = translate_block(item)
                translated_subtitle_blocks.append(translated_text)

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
        return f'✓ Translated {input_file} → {output_file} ({total_blocks} subtitles)'

    except FileNotFoundError:
        return f'✗ Error: Input file not found at {input_file}'
    except ValueError as ve:
        return f'✗ Configuration Error for {input_file}: {ve}'
    except Exception as e:
        return f'✗ Error for {input_file}: {e}'


# Alias for test compatibility and backward compatibility
def translate_srt_file(input_file, target_language, source_language='auto', output_file=None):
    """Legacy function for backward compatibility."""
    output_dir = os.path.dirname(output_file) if output_file else None
    return translate_single_srt(input_file, target_language, source_language, 'google', output_dir=output_dir)


def collect_srt_files(input_paths):
    """Collect all SRT files from paths and directories."""
    srt_files = []
    for path in input_paths:
        if os.path.isfile(path) and path.lower().endswith('.srt'):
            srt_files.append(path)
        elif os.path.isdir(path):
            for root, _, files in os.walk(path):
                for file in files:
                    if file.lower().endswith('.srt'):
                        srt_files.append(os.path.join(root, file))
    return srt_files


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description='Translate SRT subtitle files to any language.',
        epilog='Examples:\n'
               '  translate-srt movie.srt -t es                      # Translate to Spanish\n'
               '  translate-srt ./subs/ -t fr --translator mymemory  # Directory to French\n'
               '  translate-srt movie.srt -t de --workers 4          # Parallel translation\n'
               '  translate-srt --list-languages                     # Show supported languages',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('--list-languages', action='store_true',
                        help='Display supported language codes and exit.')
    parser.add_argument('input_paths', type=str, nargs='*',
                        help='Path(s) to input SRT files or directories containing SRT files.')
    parser.add_argument('-t', '--target', dest='output_lang', type=str,
                        help='Target language code for translation (e.g., en, es, fr, bn, zh-CN).')
    parser.add_argument('-s', '--source_lang', type=str, default='auto',
                        help='Source language code (e.g., en, es, fr). Defaults to auto-detect.')
    parser.add_argument('--translator', type=str, default='google',
                        choices=['google', 'deepl', 'mymemory'],
                        help='Translation service: google (default), deepl (requires API key), mymemory (free).')
    parser.add_argument('--output_dir', type=str,
                        help='Directory to save translated files. If not provided, files are saved next to originals.')
    parser.add_argument('--workers', '-w', type=int, default=1,
                        help='Number of parallel workers for translation (default: 1, max: 8).')
    parser.add_argument('--batch-size', type=int, default=10,
                        help='Sentences per translation batch (default: 10). Reserved for future use.')

    args = parser.parse_args()

    # Handle --list-languages first
    if args.list_languages:
        print(get_supported_languages())
        return

    # Validate required arguments when not listing languages
    if not args.input_paths:
        parser.error("input_paths is required. Provide path(s) to SRT files or directories.")
    if not args.output_lang:
        parser.error("--target/-t is required. Specify the target language code (e.g., -t es).")

    # Validate and clamp workers
    workers = max(1, min(args.workers, 8))
    if args.workers > 8:
        print(f"Warning: workers capped at 8 (requested {args.workers})")

    # Validate language codes
    if not validate_language_code(args.output_lang):
        print(f"Warning: '{args.output_lang}' may not be a recognized language code.")
        print("Use --list-languages to see common language codes.")

    if args.source_lang != 'auto' and not validate_language_code(args.source_lang):
        print(f"Warning: '{args.source_lang}' may not be a recognized language code.")

    # Collect SRT files
    srt_files_to_translate = collect_srt_files(args.input_paths)

    if not srt_files_to_translate:
        print("No SRT files found to translate.")
        return

    # Print summary
    worker_info = f" with {workers} workers" if workers > 1 else ""
    print(f'Translating {len(srt_files_to_translate)} SRT file(s) to {args.output_lang} '
          f'using {args.translator}{worker_info}...\n')

    # Translate files
    results = []
    for srt_file in srt_files_to_translate:
        result = translate_single_srt(
            srt_file, args.output_lang, args.source_lang,
            args.translator, output_dir=args.output_dir, workers=workers, _batch_size=args.batch_size
        )
        results.append(result)
        print(result)

    # Summary
    success_count = sum(1 for r in results if r.startswith('✓'))
    error_count = len(results) - success_count
    print(f"\n--- Summary: {success_count} succeeded, {error_count} failed ---")


if __name__ == '__main__':
    main()
