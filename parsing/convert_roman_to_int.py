def roman_to_int(s: str) -> int:
    roman = {
        'I': 1,
        'II': 2,
        'III': 3,
        'IV': 4,
        'V': 5,
        'X': 10,
        'L': 50,
        'C': 100,
        'D': 500,
        'M': 1000
    }
    
    s = s.upper()
    total = 0
    prev = 0
    for c in reversed(s):
        v = roman[c]
        total += v if v >= prev else -v
        prev = v
    return total