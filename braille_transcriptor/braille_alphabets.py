from enum import Enum


class Language(Enum):
    English = "english"
    French = "french"
    Arabic = "arabic"
    Russian = "russian"


class BrailleAlphabet:
    """Base class for Braille alphabet mappings"""
    def __init__(self):
        self.grade1_map = {}
        self.grade2_map = {}


class EnglishBrailleAlphabet(BrailleAlphabet):
    """English Braille alphabet mappings"""
    def __init__(self):
        super().__init__()
        self.grade1_map = {
            'alpha': {
                'capital_word': '⠨',
                'capital_symbol': '⠘',
                'capital_terminator': '⠱',
                'alpha': '⠰',
            },
            'numeric': {
                'numeric': '⠼',
            },
            'char': {
                ' ': '⠀',
            }
        }
        self.grade2_map = {}


class FrenchBrailleAlphabet(BrailleAlphabet):
    """French Braille alphabet mappings"""
    def __init__(self):
        super().__init__()
        self.grade1_map = {
            'alpha': {
                'capital_word': '⠨',
                'capital_symbol': '⠘',
                'capital_terminator': '⠱',
                'alpha': '⠰',
            },
            'numeric': {
                'numeric': '⠼',
            },
            'char': {
                ' ': '⠀',
            }
        }


class ArabicBrailleAlphabet(BrailleAlphabet):
    """Arabic Braille alphabet mappings"""
    def __init__(self):
        super().__init__()
        self.grade1_map = {
            'alpha': {
                'capital_word': '⠨',
                'capital_symbol': '⠘',
                'capital_terminator': '⠱',
                'alpha': '⠰',
            },
            'numeric': {
                'numeric': '⠼',
            },
            'char': {
                ' ': '⠀',
            }
        }


class RussianBrailleAlphabet(BrailleAlphabet):
    """Russian Braille alphabet mappings - corrected based on standard Russian Braille"""
    def __init__(self):
        super().__init__()
        self.grade1_map = {
            'alpha': {
                'capital_word': '⠨',
                'capital_symbol': '⠘',
                'capital_terminator': '⠱',
                'alpha': '⠰',
                'а': '⠁', 'б': '⠃', 'в': '⠺', 'г': '⠛', 'д': '⠙',
                'е': '⠑', 'ё': '⠡', 'ж': '⠚', 'з': '⠵', 'и': '⠊',
                'й': '⠯', 'к': '⠅', 'л': '⠇', 'м': '⠍', 'н': '⠝',
                'о': '⠕', 'п': '⠏', 'р': '⠗', 'с': '⠎', 'т': '⠞',
                'у': '⠥', 'ф': '⠋', 'х': '⠓', 'ц': '⠉', 'ч': '⠟',
                'ш': '⠱', 'щ': '⠳', 'ъ': '⠷', 'ы': '⠮', 'ь': '⠾',
                'э': '⠪', 'ю': '⠳', 'я': '⠫'
            },
            'numeric': {
                'numeric': '⠼',
                '0': '⠚', '1': '⠁', '2': '⠃', '3': '⠉', '4': '⠙', 
                '5': '⠑', '6': '⠋', '7': '⠛', '8': '⠓', '9': '⠊'
            },
            'char': {
                ' ': '⠀',
                ',': '⠂',
                '.': '⠲',
                ';': '⠆',
                ':': '⠿',
                '!': '⠖',
                '?': '⠦',
                '-': '⠤',
                '"': '⠶',
                '(': '⠣',
                ')': '⠜'
            }
        }
        self.grade2_map = {}


class Dictionary(Enum):
    English = EnglishBrailleAlphabet()
    French = FrenchBrailleAlphabet()
    Arabic = ArabicBrailleAlphabet()
    Russian = RussianBrailleAlphabet()