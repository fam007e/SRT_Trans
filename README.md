# SRT Translator

A robust and feature-rich Python command-line tool for translating SubRip (SRT) subtitle files. This application provides an elegant solution for subtitle translation, offering flexibility in translation services, efficient batch processing, and intelligent handling of complex subtitle content.

## Features

-   **Modular Architecture:** Designed for extensibility and maintainability, allowing easy integration of new translation services and features.
-   **Multiple Translation Services:** Supports translation via Google Translate (default) and DeepL, with an extensible design for future services.
-   **Batch Processing:** Efficiently translate multiple SRT files or entire directories containing SRT files.
-   **HTML Tag Preservation:** Intelligently preserves HTML formatting tags (e.g., `<i>`, `<b>`) within subtitles, ensuring translated output retains original styling.
-   **Mixed-Language Handling:** Employs sentence-level language detection to accurately translate subtitle blocks containing a mixture of different languages.
-   **Automatic Output Naming:** Generates translated output files with a clear, standardized naming convention.
-   **Progress Indicators:** Provides a progress bar for batch translation tasks.

## Requirements

-   Python 3.6+
-   The libraries listed in `requirements.txt`

## Installation

1.  **Clone the repository**:

    ```bash
    git clone https://github.com/fam007e/SRT_Trans.git
    cd SRT_Trans
    ```

2.  **Install the required libraries**:

    ```bash
    pip install -r requirements.txt
    ```

3.  **Download NLTK data (for mixed-language detection)**:

    ```bash
    python -c "import nltk; nltk.download('punkt'); nltk.download('punkt_tab')"
    ```

## Usage

### Command Line Interface

The `translate-srt` command is the entry point for the application. It supports translating single files or multiple files/directories.

```bash
translate-srt <input_paths...> <target_language> [--source_lang SOURCE_LANGUAGE] [--translator {google,deepl}] [--output_dir OUTPUT_DIRECTORY]
```

-   `<input_paths...>`: One or more paths to input `.srt` files or directories containing `.srt` files.
-   `<target_language>`: The language code to translate to (e.g., `bn` for Bangla, `es` for Spanish).
-   `--source_lang SOURCE_LANGUAGE`: (Optional) The source language code (e.g., `en`, `es`). Defaults to `auto`-detection. For mixed-language input, `auto` is recommended.
-   `--translator {google,deepl}`: (Optional) Specify the translation service to use. Choose `google` (default) or `deepl`.
-   `--output_dir OUTPUT_DIRECTORY`: (Optional) Specify a directory to save the translated files. If not provided, translated files are saved next to their originals.

### DeepL Translator API Key

If you choose `deepl` as your translator, you must set your DeepL API key as an environment variable named `DEEPL_API_KEY`.

```bash
export DEEPL_API_KEY="YOUR_DEEPL_API_KEY"
# Or for Windows CMD:
# set DEEPL_API_KEY="YOUR_DEEPL_API_KEY"
```

### Examples

1.  **Translate a single SRT file to Bangla using Google Translate (default):**

    ```bash
    translate-srt movie_subtitles.srt bn
    ```
    This will create `movie_subtitles_bn.srt` in the same directory.

2.  **Translate a single SRT file to Spanish using DeepL, saving to a specific directory:**

    ```bash
    translate-srt my_video.srt es --translator deepl --output_dir translated_subs
    ```
    This requires `DEEPL_API_KEY` to be set.

3.  **Batch translate all SRT files in a directory to French:**

    ```bash
    translate-srt ./my_srt_folder fr --output_dir ./french_translations
    ```

4.  **Translate multiple specific SRT files to German:**

    ```bash
    translate-srt episode1.srt episode2.srt de
    ```

### Help

To display help information for the command-line interface:

```bash
translate-srt --help
```

## Supported Languages

The script supports all languages available through the chosen translation service (Google Translate or DeepL). Refer to their respective documentation for a full list of supported language codes.

## Binary Release

For users who prefer not to install Python or its dependencies, pre-compiled binaries are available for Windows and Linux. These binaries allow you to run the `translate-srt` script directly without any installation.

### Download

You can download the latest binaries from the [GitHub Releases page](https://github.com/fam007e/SRT_Trans/releases). Look for `srt_tr_win.exe` for Windows and `srt_tr_linux` for Linux under the "Assets" section of the latest release.

### Usage

#### Windows

1.  Download `srt_tr_win.exe` from the [Releases page](https://github.com/fam007e/SRT_Trans/releases).
2.  Open a Command Prompt or PowerShell window in the directory where you downloaded the executable.
3.  Run the executable with the desired arguments:

    ```bash
    srt_tr_win.exe input_file.srt target_language [...other_options]
    ```

#### Linux

1.  Download `srt_tr_linux` from the [Releases page](https://github.com/fam007e/SRT_Trans/releases).
2.  Open a terminal in the directory where you downloaded the executable.
3.  Make the executable runnable:

    ```bash
    chmod +x srt_tr_linux
    ```

4.  Run the executable with the desired arguments:

    ```bash
    ./srt_tr_linux input_file.srt target_language [...other_options]
    ```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

-   This script utilizes the `deep-translator` library, `pysrt`, `nltk`, and `langdetect`. Special thanks to the contributors of these libraries.

## Contributions

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.
