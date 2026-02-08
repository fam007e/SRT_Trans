# SRT Translator

[![Build Status](https://github.com/fam007e/SRT_Trans/workflows/Test%20Suite/badge.svg)](https://github.com/fam007e/SRT_Trans/actions)
[![Pylint Score](https://github.com/fam007e/SRT_Trans/workflows/Pylint/badge.svg)](https://github.com/fam007e/SRT_Trans/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A robust and feature-rich Python command-line tool for translating SubRip (SRT) subtitle files. Supports Google Translate, DeepL, and MyMemory with intelligent mixed-language handling and HTML tag preservation.

## ✨ Features

*   **Modular Architecture:** Easy to extend with new translation services.
*   **Multiple Services:** Google Translate (default), DeepL, and MyMemory.
*   **Parallel Processing:** Use `--workers` to speed up translation of large files.
*   **Mixed-Language Handling:** Sentence-level language detection for mixed subtitles.
*   **HTML Tag Preservation:** Keeps `<i>`, `<b>`, etc., styling intact.
*   **Batch Processing:** Translate multiple files or entire directories at once.
*   **Automatic Output Naming:** Standardization output file names (e.g., `_es.srt`).

## 🚀 Quick Start

### Installation

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/fam007e/SRT_Trans.git
    cd SRT_Trans
    ```

2.  **Setup Virtual Environment**:
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # Linux/macOS
    # .venv\Scripts\activate  # Windows
    ```

3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    pip install -e .
    python -c "import nltk; nltk.download('punkt'); nltk.download('punkt_tab')"
    ```

### Basic Usage

```bash
translate-srt movie.srt -t es
```

## 📚 Documentation

For more detailed information, please see our dedicated documentation:

*   [**Usage Guide**](docs/USAGE.md) - Deep dive into CLI options and examples.
*   [**API Reference**](docs/API.md) - How to use SRT Translator as a library.
*   [**Contributing**](CONTRIBUTING.md) - How to help improve this project.

## 🛠 Supported Languages

SRT Translator supports over 70 languages. Run the following command to see the full list:

```bash
translate-srt --list-languages
```

## ⚖ License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgements

*   [deep-translator](https://github.com/nidhaloff/deep-translator)
*   [pysrt](https://github.com/byroot/pysrt)
*   [langdetect](https://github.com/Mimino666/langdetect)
*   [nltk](https://github.com/nltk/nltk)
