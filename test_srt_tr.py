"""
Unit tests for the srt_tr.py script.
"""

import os
import sys
import unittest
from unittest.mock import patch, MagicMock

from srt_tr import (
    parse_srt,
    translate_subtitle_block,
    translate_srt_file
)

# Add the script's directory to the Python path to allow importing
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))


class TestSrtTranslator(unittest.TestCase):
    """Test suite for the SRT translator script."""

    def setUp(self):
        """Set up test environment; create a directory for test files."""
        self.test_dir = "test_files"
        os.makedirs(self.test_dir, exist_ok=True)

    def tearDown(self):
        """Clean up test environment; remove created files and directory."""
        for f in os.listdir(self.test_dir):
            os.remove(os.path.join(self.test_dir, f))
        os.rmdir(self.test_dir)

    def _create_test_file(self, filename, content):
        """Helper function to create a test file with given content."""
        path = os.path.join(self.test_dir, filename)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        return path

    def test_parse_srt_malformed(self):
        """Test parsing of a malformed SRT file."""
        content = """
1
00:00:01,000 --> 00:00:02,000
Hello


2
00:00:03,000 --> 00:00:04,000
World



3
00:00:05,000 --> 00:00:06,000

This is a test
"""
        path = self._create_test_file("malformed.srt", content)
        subtitles = parse_srt(path)
        self.assertEqual(len(subtitles), 3)
        self.assertEqual(subtitles[0].text, "Hello")
        self.assertEqual(subtitles[1].text, "World")
        self.assertEqual(subtitles[2].text, "This is a test")

    def test_empty_srt_file(self):
        """Test the script with an empty SRT file."""
        path = self._create_test_file("empty.srt", "")
        subtitles = parse_srt(path)
        self.assertEqual(len(subtitles), 0)

    def test_no_subtitles_in_file(self):
        """Test with a file that contains text but no valid subtitles."""
        path = self._create_test_file("no_subs.srt", "Just some random text.")
        subtitles = parse_srt(path)
        self.assertEqual(len(subtitles), 0)

    @patch('srt_tr.GoogleTranslator')
    def test_multi_language_translation(self, mock_translator):
        """Test translation of a file with multiple languages."""
        # Mock the translator to return different translations based on input
        def translate_side_effect(text):
            if text == "Hello":
                return "Hola"
            if text == "Bonjour":
                return "Hello"
            return text

        mock_instance = MagicMock()
        mock_instance.translate.side_effect = translate_side_effect
        mock_translator.return_value = mock_instance

        content = """
1
00:00:01,000 --> 00:00:02,000
Hello

2
00:00:03,000 --> 00:00:04,000
Bonjour
"""
        path = self._create_test_file("multi_lang.srt", content)
        output_path = os.path.join(self.test_dir, "multi_lang_translated.srt")

        translate_srt_file(path, 'en', source_language='auto', output_file=output_path)

        with open(output_path, 'r', encoding='utf-8') as f:
            translated_content = f.read()

        self.assertIn("Hola", translated_content)
        self.assertIn("Hello", translated_content)

    @patch('srt_tr.GoogleTranslator')
    def test_translation_failure(self, mock_translator):
        """Test that the original text is used when translation fails."""
        mock_instance = MagicMock()
        mock_instance.translate.side_effect = Exception("API Error")
        mock_translator.return_value = mock_instance

        original_text = "This should not be translated"
        translated_text = translate_subtitle_block(original_text, 'en', 'es')

        self.assertEqual(translated_text, original_text)

    def test_html_tag_preservation(self):
        """Test that HTML tags are preserved during translation."""
        text = "<i>Hello</i> <b>World</b>"
        with patch('srt_tr.GoogleTranslator') as mock_translator:
            mock_instance = MagicMock()
            # The translator should be called with the text stripped of tags
            mock_instance.translate.return_value = "Hola Mundo"
            mock_translator.return_value = mock_instance

            translated_text = translate_subtitle_block(text, 'en', 'es')

            self.assertIn("<i>", translated_text)
            self.assertIn("</i>", translated_text)
            self.assertIn("<b>", translated_text)
            self.assertIn("</b>", translated_text)
            self.assertIn("Hola Mundo", translated_text)

if __name__ == '__main__':
    unittest.main()
