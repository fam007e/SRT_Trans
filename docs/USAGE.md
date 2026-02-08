# Usage Guide

SRT Translator is a powerful CLI tool for translating SubRip (SRT) subtitle files.

## Basic Usage

The simplest way to use SRT Translator is to specify an input file and a target language:

```bash
translate-srt movie.srt -t es
```

This will create `movie_es.srt` in the same directory.

## Language Codes

SRT Translator supports 70+ languages. You can see the full list by running:

```bash
translate-srt --list-languages
```

Common codes:
* `en`: English
* `es`: Spanish
* `fr`: French
* `de`: German
* `zh-CN`: Chinese (Simplified)
* `ja`: Japanese
* `bn`: Bengali

## Advanced Options

### Source Language Detection

By default, SRT Translator automatically detects the source language per sentence (great for mixed-language subtitles). If you want to force a specific source language:

```bash
translate-srt movie.srt -t fr -s en
```

### Translation Services

SRT Translator supports multiple translation services:

* `google` (default): Fast and robust.
* `mymemory`: Free alternative, no API key required.
* `deepl`: Higher quality (requires `DEEPL_API_KEY` environment variable).

```bash
translate-srt movie.srt -t de --translator mymemory
```

### Parallel Processing (Speed Up)

For large movies or batch processing, you can use multiple workers:

```bash
translate-srt movie.srt -t es --workers 4
```

### Batch Processing

You can translate multiple files or entire directories:

```bash
# Multiple files
translate-srt ep1.srt ep2.srt ep3.srt -t es

# Directory
translate-srt ./subtitles_dir/ -t es
```

### Output Directory

Save all translated files to a specific folder:

```bash
translate-srt movie.srt -t es --output_dir ./translated/
```

## HTML Tags

SRT Translator intelligently preserves HTML tags like `<i>`, `<b>`, `<font>`, etc. The tags are extracted before translation and carefully reinserted into the translated text to maintain styling.

## Troubleshooting

### API Limits

If you are using the free services (`google` or `mymemory`), you might occasionally hit rate limits for very large files. If this happens, try:
* Reducing the number of `--workers`.
* Waiting a few minutes before trying again.

### Encoding Issues

SRT Translator automatically detects file encoding. If you have an unusual encoding, it's recommended to convert the file to UTF-8 first for best results.
