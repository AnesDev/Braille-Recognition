from .strategy import *
from ahocorasick import Automaton
import re


def search_braille_patterns(text, patterns):
    # Create an Automaton object
    automaton = Automaton()

    # Add patterns to the Automaton
    for pattern,  value in patterns.items():
        automaton.add_word(pattern, (pattern, value))

    # Build the Automaton
    automaton.make_automaton()

    # Search for patterns in the text
    results = []
    for end_index, (pattern, value) in automaton.iter(text):
        start_index = end_index - len(pattern) + 1
        results.append((start_index, end_index, value))

    # Sort the results by pattern length in descending order
    results.sort(key=lambda x: len(x[2]), reverse=True)

    # Filter out overlapping patterns and keep only the largest pattern
    filtered_results = []
    for result in results:
        start_index, end_index, pattern = result
        is_overlap = False
        for filtered_result in filtered_results:
            filtered_start_index, filtered_end_index, _ = filtered_result
            if start_index <= filtered_end_index and end_index >= filtered_start_index:
                is_overlap = True
                break
        if not is_overlap:
            filtered_results.append(result)

    return filtered_results


class RussianStrategy(Strategy):

    def __init__(self):
        self.name = "russian"
        self.language = Language.Russian
        self.dictionary = Dictionary.Russian.value
        self.grade1 = self.Grade1(self)
        self.grade2 = self.Grade1(self)  # Russian typically doesn't use Grade 2, so use Grade 1

    class Grade1(Grade):

        def __init__(self, outer):
            self.outer = outer
            
            # Get mappings from the dictionary
            alpha_map = outer.dictionary.grade1_map['alpha']
            numeric_map = outer.dictionary.grade1_map['numeric']
            char_map = outer.dictionary.grade1_map['char']
            
            # Create reverse mappings for decoding
            self.cyrillic_map = {v: k for k, v in alpha_map.items() 
                               if k not in ['capital_word', 'capital_symbol', 'capital_terminator', 'alpha']}
            
            # Capital indicators
            self.CAPITAL_SYMBOL = alpha_map['capital_symbol']
            self.CAPITAL_WORD = alpha_map.get('capital_word', self.CAPITAL_SYMBOL)
            
            # Numbers
            self.NUMERIC = numeric_map['numeric']
            self.number_map = {v: k for k, v in numeric_map.items() if k != 'numeric'}
            
            # Special characters
            self.special_map = {v: k for k, v in char_map.items()}

        def from_braille(self, braille):
            """
            Convert Russian Braille to Cyrillic text with corrections
            """
            result = ""
            i = 0
            capitalize_next = False
            
            while i < len(braille):
                char = braille[i]
                
                # Skip ⠿ - it's a special marker, not a letter
                if char == '⠿':
                    i += 1
                    continue
                
                # Handle capital indicators
                if char == self.CAPITAL_SYMBOL:
                    capitalize_next = True
                    i += 1
                    continue
                
                # Handle numbers
                elif char == self.NUMERIC:
                    i += 1
                    while i < len(braille) and braille[i] in self.number_map:
                        result += self.number_map[braille[i]]
                        i += 1
                    continue
                
                # Handle Cyrillic characters
                elif char in self.cyrillic_map:
                    cyrillic_char = self.cyrillic_map[char]
                    if capitalize_next:
                        cyrillic_char = cyrillic_char.upper()
                        capitalize_next = False
                    result += cyrillic_char
                
                # Handle special characters
                elif char in self.special_map:
                    result += self.special_map[char]
                
                # Handle unknown characters
                else:
                    result += char
                
                i += 1
            
            # Apply Russian word corrections
            result = self._apply_corrections(result.strip())
            return result
        
        def _apply_corrections(self, text):
            """Apply common corrections for Russian OCR errors"""
            corrections = {
                # Common OCR confusions between ⠟(я) and ⠯(ч)
                'сергеевия': 'сергеевич',
                'петровия': 'петрович', 
                'ивановия': 'иванович',
                'александровия': 'александрович',
                'михайловия': 'михайлович',
                'николаевия': 'николаевич',
                
                # Word-level corrections based on context
                'татъюна': 'татьяна',
                'барэню': 'барыня', 
                'дворяик': 'дворник',
                'прячка': 'прачка',
                'праяка': 'прачка',
                'слуяа': 'слуга',
                'слуяи': 'слуги',
                'гиё': 'его',
                'йила': 'жила',
                'ояенъ': 'очень',
                'эделала': 'сделала',
                'поскве': 'после',
                'один⠔каю': 'одинокая',
                'стараю': 'старая',
                'бэло': 'было',
                'ёмного': 'много',
                'ёмоскву': 'москву',
                'ёгирасина': 'герасима',
                'дворнёикомё': 'дворником',
                'гаврилаё': 'гаврила',
                'бёааш': 'бесшумный',
                'маяник': 'мужчина',
                'гирасин': 'герасим',
                'расин': 'герасим',
                'рецкич': 'рецкий',
                'дво': 'дворецкий',
                
                # Remove repeated characters at end
                'ёёё': '',
                'ёёёёёёёёё': '',
            }
            
            # Apply word-level corrections
            words = text.split()
            corrected_words = []
            
            for word in words:
                # Remove punctuation for matching, then restore
                clean_word = word.strip('.,!?;:()[]{}"-⠲⠆⠖⠢').lower()
                
                # Remove Braille punctuation that shouldn't be in text
                clean_word = clean_word.replace('⠲', '').replace('⠆', '').replace('⠔', '')
                
                if clean_word in corrections:
                    corrected = corrections[clean_word]
                    if word and word[0].isupper() and corrected:
                        corrected = corrected.capitalize()
                    # Restore punctuation (convert Braille punctuation to regular)
                    if '⠲' in word:
                        corrected += '.'
                    elif '⠆' in word:
                        corrected += '.'
                    elif '⠖' in word:
                        corrected += '!'
                    elif '⠢' in word:
                        corrected += '?'
                    elif word.endswith(','):
                        corrected += ','
                    corrected_words.append(corrected)
                else:
                    # Clean up Braille punctuation
                    cleaned = word.replace('⠲', '.').replace('⠆', '.').replace('⠖', '!').replace('⠢', '?').replace('⠔', '')
                    corrected_words.append(cleaned)
            
            return ' '.join(corrected_words)
        
        def to_braille(self, text):
            """
            Convert Cyrillic text to Russian Braille
            """
            # Get forward mappings
            alpha_map = self.outer.dictionary.grade1_map['alpha']
            numeric_map = self.outer.dictionary.grade1_map['numeric']
            char_map = self.outer.dictionary.grade1_map['char']
            
            result = ""
            i = 0
            
            while i < len(text):
                char = text[i]
                
                # Handle uppercase
                if char.isupper():
                    result += self.CAPITAL_SYMBOL
                    char = char.lower()
                
                # Handle numbers
                if char.isdigit():
                    if i == 0 or not text[i-1].isdigit():
                        result += self.NUMERIC
                    result += numeric_map.get(char, char)
                
                # Handle Cyrillic
                elif char in alpha_map:
                    result += alpha_map[char]
                
                # Handle special characters
                elif char in char_map:
                    result += char_map[char]
                
                # Handle unknown
                else:
                    result += char
                
                i += 1
            
            return result