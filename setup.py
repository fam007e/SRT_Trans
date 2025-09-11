"""Setup configuration for the SRT Translator package."""

import os
from setuptools import setup

# Read the content of the README file
with open(
    os.path.join(os.path.dirname(__file__), 'README.md'),
    encoding='utf-8'
) as f:
    long_description = f.read()

setup(
    name='srt-translator',
    version='0.1',
    author='Faisal Ahmed Moshiur',
    author_email='faisalmoshiur+gitSRT@gmail.com',
    description='A script to translate .srt files using GoogleTranslator.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    py_modules=['srt_tr'],
    install_requires=[
        'deep-translator',
        'tqdm',
        'chardet',
    ],
    entry_points={
        'console_scripts': [
            'translate-srt=srt_tr:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
