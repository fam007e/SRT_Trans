import os
import unittest
from unittest.mock import patch
import shutil

from srt_translator.srt_parser import SrtParser
from srt_translator.translators import GoogleTranslate, DeepLTranslate
from srt_translator.cli import translate_single_srt

class TestSrtTranslator(unittest.TestCase):
    """Test suite for the SRT translator script."""

    def setUp(self):
        """Set up test environment; create a directory for test files."""
        self.test_dir = "test_files"
        os.makedirs(self.test_dir, exist_ok=True)
        self.output_dir = os.path.join(self.test_dir, "output")
        os.makedirs(self.output_dir, exist_ok=True)

    def tearDown(self):
        """Clean up test environment; remove created files and directory."""
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def _create_test_srt(self, filename, content):
        """Helper function to create a test SRT file with full path."""
        path = os.path.join(self.test_dir, filename)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        return path

    @patch.object(GoogleTranslate, 'translate')
    @patch.object(SrtParser, 'split_into_sentences')
    @patch.object(SrtParser, 'detect_language')
    def test_translate_single_srt_google(self, mock_detect_language, mock_split_into_sentences, mock_google_translate):
        """Test translate_single_srt with GoogleTranslate and mixed languages."""
        srt_content = """
1
00:00:00,000 --> 00:00:01,000
Hello. ¿Cómo estás?
"""
        input_path = self._create_test_srt("mixed_google.srt", srt_content)
        output_file = os.path.join(self.output_dir, "mixed_google_bn.srt")

        mock_split_into_sentences.return_value = ["Hello.", "¿Cómo estás?"]
        mock_detect_language.side_effect = ["en", "es"]
        mock_google_translate.side_effect = ["হ্যালো।", "কেমন আছেন?"] # Bangla for Hello. and How are you?

        result = translate_single_srt(input_path, 'bn', 'auto', 'google', self.output_dir)
        self.assertIn("Translated", result)
        self.assertTrue(os.path.exists(output_file))

        with open(output_file, 'r', encoding='utf-8') as f:
            output_content = f.read()
            self.assertIn("হ্যালো। কেমন আছেন?", output_content)

        mock_split_into_sentences.assert_called_once_with("Hello. ¿Cómo estás?")
        self.assertEqual(mock_detect_language.call_count, 2)
        mock_google_translate.assert_any_call("Hello.", 'bn', 'en')
        mock_google_translate.assert_any_call("¿Cómo estás?", 'bn', 'es')

    @patch.dict(os.environ, {'DEEPL_API_KEY': 'mock_key'})
    @patch.object(DeepLTranslate, 'translate')
    @patch.object(SrtParser, 'split_into_sentences')
    @patch.object(SrtParser, 'detect_language')
    def test_translate_single_srt_deepl(self, mock_detect_language, mock_split_into_sentences, mock_deepl_translate):
        """Test translate_single_srt with DeepLTranslate and mixed languages."""
        srt_content = """
1
00:00:00,000 --> 00:00:01,000
Hello. ¿Cómo estás?
"""
        input_path = self._create_test_srt("mixed_deepl.srt", srt_content)
        output_file = os.path.join(self.output_dir, "mixed_deepl_bn.srt")

        mock_split_into_sentences.return_value = ["Hello.", "¿Cómo estás?"]
        mock_detect_language.side_effect = ["en", "es"]
        mock_deepl_translate.side_effect = ["হ্যালো।", "কেমন আছেন?"] # Bangla for Hello. and How are you?

        result = translate_single_srt(input_path, 'bn', 'auto', 'deepl', self.output_dir)
        self.assertIn("Translated", result)
        self.assertTrue(os.path.exists(output_file))

        with open(output_file, 'r', encoding='utf-8') as f:
            output_content = f.read()
            self.assertIn("হ্যালো। কেমন আছেন?", output_content)

        mock_split_into_sentences.assert_called_once_with("Hello. ¿Cómo estás?")
        self.assertEqual(mock_detect_language.call_count, 2)
        mock_deepl_translate.assert_any_call("Hello.", 'bn', 'en')
        mock_deepl_translate.assert_any_call("¿Cómo estás?", 'bn', 'es')

    @patch.object(GoogleTranslate, 'translate')
    @patch.object(SrtParser, 'split_into_sentences')
    @patch.object(SrtParser, 'detect_language')
    def test_translate_single_srt_html_preservation(self, mock_detect_language, mock_split_into_sentences, mock_google_translate):
        """Test HTML tag preservation with translate_single_srt."""
        srt_content = """
1
00:00:00,000 --> 00:00:01,000
<i>Hello</i> <b>world</b>.
"""
        input_path = self._create_test_srt("html_preservation.srt", srt_content)
        output_file = os.path.join(self.output_dir, "html_preservation_es.srt")

        mock_split_into_sentences.return_value = ["__TAG_0__Hello__TAG_1__ __TAG_2__world__TAG_3__."]
        mock_detect_language.return_value = "en"
        mock_google_translate.return_value = "<i>Hola</i> <b>mundo</b>."

        result = translate_single_srt(input_path, 'es', 'auto', 'google', self.output_dir)
        self.assertIn("Translated", result)
        self.assertTrue(os.path.exists(output_file))

        with open(output_file, 'r', encoding='utf-8') as f:
            output_content = f.read()
            self.assertIn("<i>Hola</i> <b>mundo</b>.", output_content)

        mock_split_into_sentences.assert_called_once()
        mock_detect_language.assert_called_once()
        mock_google_translate.assert_called_once_with("__TAG_0__Hello__TAG_1__ __TAG_2__world__TAG_3__.", 'es', 'en')

    @patch.object(GoogleTranslate, 'translate')
    @patch.object(SrtParser, 'split_into_sentences')
    @patch.object(SrtParser, 'detect_language')
    def test_translate_single_srt_batch_processing(self, mock_detect_language, mock_split_into_sentences, mock_google_translate):
        """Test batch processing with translate_single_srt."""
        srt_content_1 = """
1
00:00:00,000 --> 00:00:01,000
Hello world 1.
"""
        srt_content_2 = """
1
00:00:00,000 --> 00:00:01,000
Hello world 2.
"""
        input_path_1 = self._create_test_srt("batch_1.srt", srt_content_1)
        input_path_2 = self._create_test_srt("batch_2.srt", srt_content_2)

        mock_split_into_sentences.side_effect = [["Hello world 1."], ["Hello world 2."]]
        mock_detect_language.side_effect = ["en", "en"]
        mock_google_translate.side_effect = ["Hola mundo 1.", "Hola mundo 2."]

        # Simulate the main function's loop calling translate_single_srt
        result1 = translate_single_srt(input_path_1, 'es', 'auto', 'google', self.output_dir)
        result2 = translate_single_srt(input_path_2, 'es', 'auto', 'google', self.output_dir)

        self.assertIn("Translated", result1)
        self.assertIn("Translated", result2)

        output_file_1 = os.path.join(self.output_dir, "batch_1_es.srt")
        output_file_2 = os.path.join(self.output_dir, "batch_2_es.srt")

        self.assertTrue(os.path.exists(output_file_1))
        self.assertTrue(os.path.exists(output_file_2))

        with open(output_file_1, 'r', encoding='utf-8') as f:
            self.assertIn("Hola mundo 1.", f.read())
        with open(output_file_2, 'r', encoding='utf-8') as f:
            self.assertIn("Hola mundo 2.", f.read())

        self.assertEqual(mock_google_translate.call_count, 2)
        self.assertEqual(mock_split_into_sentences.call_count, 2)
        self.assertEqual(mock_detect_language.call_count, 2)

    def test_srt_parser_read_write(self):
        """Test if SrtParser can read and write SRT files correctly."""
        srt_content = """
1
00:00:00,000 --> 00:00:01,000
Test line 1

2
00:00:01,500 --> 00:00:02,500
Test line 2
"""
        input_path = self._create_test_srt("test_parser.srt", srt_content)

        parser = SrtParser(input_path)
        texts = parser.get_subtitles_text()
        self.assertEqual(texts, ["Test line 1", "Test line 2"])

        parser.update_subtitles_text(["Translated line 1", "Translated line 2"])
        output_file = os.path.join(self.output_dir, "test_parser_translated.srt")
        parser.write_srt(output_file)

        with open(output_file, 'r', encoding='utf-8') as f:
            output_content = f.read()
            self.assertIn("Translated line 1", output_content)
            self.assertIn("Translated line 2", output_content)

    def test_srt_parser_clean_text(self):
        """Test the clean_text static method."""
        text_with_html = "<i>Hello</i> <b>World</b> <br>  extra spaces"
        cleaned_text, tags = SrtParser.clean_text(text_with_html)
        self.assertEqual(cleaned_text, "__TAG_0__Hello__TAG_1__ __TAG_2__World__TAG_3__ __TAG_4__ extra spaces")
        self.assertEqual(tags, [('__TAG_0__', '<i>'), ('__TAG_1__', '</i>'), ('__TAG_2__', '<b>'), ('__TAG_3__', '</b>'), ('__TAG_4__', '<br>')])

    def test_srt_parser_reinsert_tags(self):
        """Test the reinsert_tags static method."""

        tags = [('__TAG_0__', '<i>'), ('__TAG_1__', '</i>')]
        reinserted_text = SrtParser.reinsert_tags("__TAG_0__Hola mundo__TAG_1__", tags)
        self.assertEqual(reinserted_text, "<i>Hola mundo</i>")

if __name__ == '__main__':
    unittest.main()
