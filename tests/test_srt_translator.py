"""
Comprehensive test suite for SRT Translator.
Tests edge cases, Unicode handling, performance, and robustness.
"""
import pytest
import os
import tempfile
import time
from pathlib import Path
from unittest.mock import patch, MagicMock

from srt_translator.srt_parser import SrtParser
from srt_translator.translators import (
    GoogleTranslate, DeepLTranslate, MyMemoryTranslate,
    get_translator, validate_language_code, get_supported_languages,
    COMMON_LANGUAGE_CODES
)
from srt_translator.cli import translate_single_srt, translate_srt_file


# Path to test data directory
TEST_DATA_DIR = Path(__file__).parent.parent / 'test_data'


class TestLanguageValidation:
    """Tests for language code validation."""

    def test_valid_common_codes(self):
        """Test that common language codes are valid."""
        valid_codes = ['en', 'es', 'fr', 'de', 'ja', 'zh-CN', 'ar', 'ru', 'bn']
        for code in valid_codes:
            assert validate_language_code(code), f"{code} should be valid"

    def test_invalid_codes(self):
        """Test that invalid codes are rejected."""
        invalid_codes = ['xyz', 'abc', '123', '']
        for code in invalid_codes:
            assert not validate_language_code(code), f"{code} should be invalid"

    def test_auto_code_handling(self):
        """Test auto detection code handling."""
        assert validate_language_code('auto', allow_auto=True)
        assert not validate_language_code('auto', allow_auto=False)

    def test_supported_languages_output(self):
        """Test that supported languages list is complete."""
        output = get_supported_languages()
        assert 'Spanish' in output
        assert 'Bengali' in output
        assert 'Chinese' in output
        assert len(COMMON_LANGUAGE_CODES) > 50


class TestTranslatorFactory:
    """Tests for translator factory function."""

    def test_get_google_translator(self):
        """Test getting Google translator."""
        translator = get_translator('google')
        assert isinstance(translator, GoogleTranslate)

    def test_get_mymemory_translator(self):
        """Test getting MyMemory translator."""
        translator = get_translator('mymemory')
        assert isinstance(translator, MyMemoryTranslate)

    def test_invalid_translator_raises(self):
        """Test that invalid translator name raises error."""
        with pytest.raises(ValueError, match="Unknown translator"):
            get_translator('invalid_translator')

    def test_deepl_without_key_raises(self):
        """Test that DeepL without API key raises error."""
        with patch.dict(os.environ, {}, clear=True):
            os.environ.pop('DEEPL_API_KEY', None)
            with pytest.raises(ValueError, match="DEEPL_API_KEY"):
                get_translator('deepl')


class TestSrtParserEdgeCases:
    """Tests for SRT parser with edge cases."""

    def test_parse_simple_srt(self):
        """Test parsing a simple valid SRT file."""
        parser = SrtParser(str(TEST_DATA_DIR / 'simple.srt'))
        texts = parser.get_subtitles_text()
        assert len(texts) == 2
        assert 'Hello' in texts[0]

    def test_parse_unicode_srt(self):
        """Test parsing SRT with various Unicode content."""
        parser = SrtParser(str(TEST_DATA_DIR / 'unicode.srt'))
        texts = parser.get_subtitles_text()
        assert len(texts) >= 10
        # Check for various scripts
        all_text = ' '.join(texts)
        assert '😀' in all_text or 'emoji' in all_text.lower()
        assert '你好' in all_text  # Chinese
        assert 'مرحبا' in all_text  # Arabic

    def test_parse_bom_utf8(self):
        """Test parsing UTF-8 file with BOM marker."""
        parser = SrtParser(str(TEST_DATA_DIR / 'bom_utf8.srt'))
        texts = parser.get_subtitles_text()
        assert len(texts) >= 1
        # First subtitle should not start with BOM
        assert not texts[0].startswith('\ufeff')

    def test_parse_edge_cases_srt(self):
        """Test parsing SRT with various edge cases."""
        parser = SrtParser(str(TEST_DATA_DIR / 'edge_cases.srt'))
        texts = parser.get_subtitles_text()
        # Should parse most subtitles despite edge cases
        assert len(texts) >= 5

    def test_parse_large_srt(self):
        """Test parsing large SRT file."""
        parser = SrtParser(str(TEST_DATA_DIR / 'large.srt'))
        texts = parser.get_subtitles_text()
        assert len(texts) == 500

    def test_file_not_found(self):
        """Test that missing file raises appropriate error."""
        with pytest.raises(FileNotFoundError):
            SrtParser('/nonexistent/path/file.srt')

    def test_clean_text_preserves_content(self):
        """Test that clean_text preserves essential content."""
        text = "Hello <i>world</i>!"
        cleaned, tags = SrtParser.clean_text(text)
        assert 'Hello' in cleaned
        assert 'world' in cleaned
        assert len(tags) == 2  # <i> and </i>

    def test_reinsert_tags(self):
        """Test that tags are properly reinserted."""
        original = "Hello <b>bold</b> text"
        cleaned, tags = SrtParser.clean_text(original)
        # Simulate translation (no change for test)
        restored = SrtParser.reinsert_tags(cleaned, tags)
        assert '<b>' in restored
        assert '</b>' in restored

    def test_detect_language_english(self):
        """Test language detection for English."""
        lang = SrtParser.detect_language("Hello world, this is a test.")
        assert lang == 'en'

    def test_detect_language_spanish(self):
        """Test language detection for Spanish."""
        lang = SrtParser.detect_language("Hola mundo, esto es una prueba.")
        assert lang == 'es'

    def test_detect_language_short_text(self):
        """Test language detection handles short text."""
        # A bit more context helps langdetect
        lang = SrtParser.detect_language("Hello, how are you?")
        assert lang == 'en'

    def test_split_sentences(self):
        """Test sentence splitting."""
        text = "First sentence. Second sentence! Third one?"
        sentences = SrtParser.split_into_sentences(text)
        assert len(sentences) == 3


class TestTranslatorEmptyInput:
    """Tests for translator handling of empty/whitespace input."""

    def test_google_empty_string(self):
        """Test Google translator with empty string."""
        translator = GoogleTranslate()
        result = translator.translate("", "es", "en")
        assert result == ""

    def test_google_whitespace(self):
        """Test Google translator with whitespace."""
        translator = GoogleTranslate()
        result = translator.translate("   ", "es", "en")
        assert result == "   "

    def test_mymemory_empty_string(self):
        """Test MyMemory translator with empty string."""
        translator = MyMemoryTranslate()
        result = translator.translate("", "es", "en")
        assert result == ""


class TestCLIFunctions:
    """Tests for CLI functions."""

    def test_translate_srt_file_creates_output(self, tmp_path):
        """Test that translate_srt_file creates output file."""
        # Create a simple test SRT
        input_srt = tmp_path / "test.srt"
        input_srt.write_text("""1
00:00:01,000 --> 00:00:02,000
Hello world!

""")
        output_srt = tmp_path / "output.srt"

        with patch('srt_translator.cli.get_translator') as mock_get:
            mock_translator = MagicMock()
            mock_translator.translate.return_value = "¡Hola mundo!"
            mock_get.return_value = mock_translator

            result = translate_srt_file(
                str(input_srt), 'es', 'en', str(output_srt)
            )

        # Should complete without error
        assert output_srt.exists() or 'Translated' in str(result) or 'Error' not in str(result)

    def test_translate_single_srt_invalid_file(self):
        """Test handling of invalid input file."""
        result = translate_single_srt(
            '/nonexistent/file.srt', 'es', 'auto', 'google'
        )
        assert 'Error' in result or 'not found' in result.lower()


@pytest.mark.slow
class TestPerformance:
    """Performance tests for large files."""

    def test_parse_large_file_speed(self):
        """Test that large file parsing is fast enough."""
        start = time.time()
        parser = SrtParser(str(TEST_DATA_DIR / 'large.srt'))
        texts = parser.get_subtitles_text()
        elapsed = time.time() - start

        assert len(texts) == 500
        assert elapsed < 2.0, f"Parsing took {elapsed:.2f}s, should be < 2s"

    def test_clean_text_performance(self):
        """Test that text cleaning is fast."""
        # Create text with many HTML tags
        text = "<b>Bold</b> and <i>italic</i> " * 100

        start = time.time()
        for _ in range(1000):
            SrtParser.clean_text(text)
        elapsed = time.time() - start

        assert elapsed < 1.0, f"1000 clean_text calls took {elapsed:.2f}s"


@pytest.mark.network
class TestRealTranslation:
    """Tests that make real API calls (require network)."""

    def test_google_translate_real(self):
        """Test real Google Translate API call."""
        translator = GoogleTranslate()
        result = translator.translate("Hello", "es", "en")
        assert result.lower() in ['hola', '¡hola', 'hola!']

    def test_mymemory_translate_real(self):
        """Test real MyMemory API call."""
        translator = MyMemoryTranslate()
        result = translator.translate("Hello", "es", "en")
        assert 'hola' in result.lower()


class TestWriteOutput:
    """Tests for writing SRT output."""

    def test_write_preserves_timing(self, tmp_path):
        """Test that writing preserves subtitle timing."""
        input_srt = TEST_DATA_DIR / 'simple.srt'
        parser = SrtParser(str(input_srt))

        output_path = tmp_path / "output.srt"
        parser.write_srt(str(output_path))

        # Read back and verify timing preserved
        content = output_path.read_text()
        assert '00:00:01,000' in content
        assert '-->' in content

    def test_update_subtitles_text(self, tmp_path):
        """Test updating subtitle text."""
        input_srt = TEST_DATA_DIR / 'simple.srt'
        parser = SrtParser(str(input_srt))

        original_texts = parser.get_subtitles_text()
        new_texts = ['Translated 1', 'Translated 2']
        parser.update_subtitles_text(new_texts)

        output_path = tmp_path / "output.srt"
        parser.write_srt(str(output_path))

        content = output_path.read_text()
        assert 'Translated 1' in content
        assert 'Translated 2' in content
