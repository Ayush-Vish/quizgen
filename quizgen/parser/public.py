"""
Pieces of the parsing infrastructure that are exposed for public use.
Code outside this package should generally only use these resources.
"""

import os

import quizgen.parser.parse
import quizgen.util.serial
import quizgen.util.file

class ParsedText(quizgen.util.serial.PODSerializer):
    """
    A representation of text that has been successfully parsed.
    """

    def __init__(self, text, document):
        self.text = text
        self.document = document

    def to_pod(self, **kwargs):
        return self.text

def parse_text(text, base_dir = '.'):
    text, document = quizgen.parser.parse._parse_text(text, base_dir = base_dir)
    return ParsedText(text, document)

def parse_file(path):
    if (not os.path.isfile(path)):
        raise ValueError(f"Path to parse ('{path}') is not a file.")

    text = quizgen.util.file.read(path)
    base_dir = os.path.dirname(path)

    return parse_text(text, base_dir = base_dir)
