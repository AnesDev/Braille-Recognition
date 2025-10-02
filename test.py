# Test file to verify Russian Braille transcription works

from braille_transcriptor.strategies.russian import RussianStrategy

def test_russian_transcription():
    strategy = RussianStrategy()
    
    # Test sample Braille text
    test_braille = "⠘⠊⠺⠁⠝ ⠘⠎⠑⠗⠛⠑⠑⠺⠊⠟ ⠘⠞⠥⠗⠛⠑⠝⠑⠺"
    
    print("Original Braille:", test_braille)
    
    try:
        translated = strategy.grade1.from_braille(test_braille)
        print("Translated to Cyrillic:", translated)
    except Exception as e:
        print("Error:", e)
    
    # Test encoding back to Braille
    test_text = "Иван Сергеевич"
    try:
        braille_encoded = strategy.grade1.to_braille(test_text)
        print(f"'{test_text}' -> '{braille_encoded}'")
    except Exception as e:
        print("Encoding error:", e)
        
    # Test individual character mappings
    print("\n--- Character mapping test ---")
    test_chars = ['ч', 'я', 'и', 'в', 'а', 'н']
    for char in test_chars:
        try:
            braille_char = strategy.grade1.to_braille(char)
            decoded = strategy.grade1.from_braille(braille_char)
            print(f"'{char}' -> '{braille_char}' -> '{decoded}'")
        except Exception as e:
            print(f"Error with '{char}': {e}")
    
    # Test the specific sequence causing issues
    print("\n--- Testing specific sequence ---")
    test_sequence = "⠎⠑⠗⠛⠑⠑⠺⠊⠟"  # серге⠑⠺⠊⠟ -> should be сергеевич but getting сергеевия
    try:
        result = strategy.grade1.from_braille(test_sequence)
        print(f"'{test_sequence}' -> '{result}' (currently getting)")
    except Exception as e:
        print(f"Error: {e}")
    
    # Show what the correct Braille should be for "сергеевич"
    print("\n--- What should 'сергеевич' look like in Braille? ---")
    correct_text = "сергеевич"
    correct_braille = strategy.grade1.to_braille(correct_text)
    print(f"'{correct_text}' should be: '{correct_braille}'")
    
    # analyze each character in the problematic sequence
    print("\n--- Character-by-character analysis ---")
    problematic = "⠎⠑⠗⠛⠑⠑⠺⠊⠟"
    print(f"Analyzing: {problematic}")
    for i, char in enumerate(problematic):
        try:
            decoded = strategy.grade1.from_braille(char)
            print(f"Position {i}: '{char}' -> '{decoded}'")
        except:
            print(f"Position {i}: '{char}' -> unknown")
    
    # Compare with what it should be
    print("\n--- Expected vs Actual ---")
    expected_braille = "⠎⠑⠗⠛⠑⠑⠺⠊⠯"  # сергеевич with ⠯ for 'ч'
    print(f"Expected: {expected_braille}")
    print(f"Actual:   {problematic}")
    print(f"Expected decodes to: {strategy.grade1.from_braille(expected_braille)}")
    print(f"Actual decodes to:   {strategy.grade1.from_braille(problematic)}")

if __name__ == "__main__":
    test_russian_transcription()
