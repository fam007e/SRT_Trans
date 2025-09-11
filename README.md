# Subtitle Translator Script

This Python script translates subtitle files (`.srt`) from one language to another using the Google Translator via the `deep_translator` library.

## Features

- Translates subtitle text while preserving timestamps and formatting.
- Automatically generates an output file with a standardized naming convention.
- Supports multiple languages, including files with mixed languages, by translating each subtitle block individually.
- Robustly handles common SRT formatting errors.
- Preserves HTML tags within subtitles.

## Requirements

- Python 3.6+
- `deep-translator` library
- `tqdm` library
- `chardet` library

## Installation

1. **Clone the repository** (or download the script):

    ```bash
    git clone git@github.com:fam007e/SRT_Trans.git
    cd SRT_Trans
    ```

2. **Install the required libraries**:

    ```bash
    pip install -r requirements.txt
    ```


## Usage

### Command Line Interface

Run the script from the command line with the following format:

```bash
python srt_tr.py input_file.srt target_language [-s source_language] [-o output_file]
```
- `input_file.srt`: Path to your input .srt file.
- `target_language`: Language code to translate to (e.g., `bn` for Bangla).
- `-s, --source_language`: Language code of the input file (default: `auto`).
- `-o, --output_file`: Path to save the translated .srt file.

## Example
```bash
python srt_tr.py movie_subtitles.srt bn
```
This will read the `movie_subtitles.srt` file, automatically detect the source language, translate the subtitles to Bangla, and save the output to `movie_subtitles_trs_bn.srt`.

## Help
To display help information:
```bash
python srt_tr.py -h
```
This will display:
```sql
usage: srt_tr.py [-h] [-s SOURCE_LANGUAGE] [-o OUTPUT_FILE]
                 input_file target_language

Translate subtitles from one language to another.

positional arguments:
  input_file            Input .srt file path
  target_language       Language code to output (e.g., bn for Bangla)

optional arguments:
  -h, --help            show this help message and exit
  -s SOURCE_LANGUAGE, --source_language SOURCE_LANGUAGE
                        Language code for input (default: auto)
  -o OUTPUT_FILE, --output_file OUTPUT_FILE
                        Output .srt file path

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
```
## Supported Languages
The script supports all languages available through the Google Translator API. Some common language codes are:
- `en` - English
- `bn` - Bangla
- `es` - Spanish
- `fr` - French
- `de` - German
- `zh` - Chinese
- `ja` - Japanese
- `ko` - Korean
- `ru` - Russian
- `hi` - Hindi

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.


## Acknowledgements
- This script uses the `deep_translator` library. Special thanks to the contributors of this library.

## Contributions
Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.