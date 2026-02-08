"""
SRT Translator - A tool for translating SRT subtitle files.
"""

from .srt_parser import SrtParser, Subtitle
from .translators import (
    GoogleTranslate,
    DeepLTranslate,
    MyMemoryTranslate,
    get_translator,
    get_supported_languages,
    validate_language_code,
    COMMON_LANGUAGE_CODES,
)
from .cli import translate_srt_file, translate_single_srt, translate_block

__version__ = '0.2'
__all__ = [
    'SrtParser',
    'Subtitle',
    'GoogleTranslate',
    'DeepLTranslate',
    'MyMemoryTranslate',
    'get_translator',
    'get_supported_languages',
    'validate_language_code',
    'COMMON_LANGUAGE_CODES',
    'translate_srt_file',
    'translate_single_srt',
    'translate_block',
]
