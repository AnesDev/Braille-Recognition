from typing import List

BRAILLE_BASE = 0x2800

def dotpattern_to_unicode(pattern: str) -> str:
    """
    Convert a dot pattern string like '123' or '16' to a braille unicode character.
    Assumes 6-dot braille (dots 1..6). Returns U+2800 + bits.
    """
    if not pattern or pattern == "?":
        return "?"  # keep unknown marker
    bits = 0
    for ch in pattern:
        if ch.isdigit():
            d = int(ch)
            if 1 <= d <= 6:
                bits |= 1 << (d - 1)
            # if 7/8 appear ignore (extendable)
    return chr(BRAILLE_BASE + bits)

def estimate_space_threshold(widths: List[int], factor: float = 1.2) -> float:
    """
    Choose a gap threshold for inserting spaces.
    widths: list of widths of characters in the row or doc.
    factor: multiply avg width to get threshold.
    """
    if not widths:
        return 20.0
    avg_w = sum(widths) / len(widths)
    return avg_w * factor
