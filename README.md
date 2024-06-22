# Subtitle Translator Script

This Python script translates subtitle files (.srt) from one language to another using the Google Translator via the `deep_translator` library.

## Features

- Translates subtitle text while preserving timestamps and formatting.
- Automatically generates an output file with a standardized naming convention.
- Supports multiple languages.

## Requirements

- Python 3.6+
- `deep_translator` library

## Installation

1. **Clone the repository** (or download the script):

    ```bash
    git clone https://github.com/yourusername/your-repo-name.git
    cd your-repo-name
    ```

2. **Install the required library**:

    ```bash
    pip install deep-translator
    ```

## Usage

### Command Line Interface

Run the script from the command line with the following format:

```bash
python translate_srt.py input_file.srt source_language target_language
```
-`input_file.srt`: Path to your input .srt file.
-`source_language`: Language code of the input file (e.g., `en` for English).
-`target_language`: Language code to translate to (e.g., `bn` for Bangla).

## Example
```bash
python translate_srt.py movie_subtitles.srt en bn
```
This will read the `movie_subtitles.srt` file, translate the english subtitles to bangla, and save the output to `movie_subtitles_trs_bn.srt`.

## Help
To display help information:
```bash
python translate_srt.py -h
```
This will display:
```sql
usage: translate_srt.py [-h] input_file source_language target_language

Translate subtitles from one language to another.

positional arguments:
  input_file        Input .srt file path
  source_language   Language code of the input file (e.g., en for English)
  target_language   Language code to translate to (e.g., bn for Bangla)

optional arguments:
  -h, --help        show this help message and exit

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
- `en` \- English
- `bn` \- Bangla
- `es` \- Spanish
- `fr` \- French
- `de` \- German
- `zh` \- Chinese
- `ja` \- Japanese
- `ko` \- Korean
- `ru` \- Russian
- `hi` \- Hindi

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.


## Acknowledgements
- This script uses the `deep_translator` library. Special thanks to the contributors of this library.

## Contributions
Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

