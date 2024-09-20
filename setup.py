"""Setup configuration for the SRT Translator package."""

import os  # Standard library import
from setuptools import setup  # Third-party import

# Read the content of the README file
with open(os.path.join(os.path.dirname(__file__), 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='srt-translator',
    version='0.1',
    author='Your Name',
    author_email='your.email@example.com',
    description='A script to translate .srt files from one language to another using GoogleTranslator.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    py_modules=['translate_srt'],
    install_requires=[
        'deep-translator',
        'tqdm',
    ],
    entry_points={
        'console_scripts': [
            'translate-srt=translate_srt:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
