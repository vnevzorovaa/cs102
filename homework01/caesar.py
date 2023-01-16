import typing as tp


def encrypt_caesar(plaintext: str, shift: int = 3) -> str:
    """
    Encrypts plaintext using a Caesar cipher.
    >>> encrypt_caesar("PYTHON")
    'SBWKRQ'
    >>> encrypt_caesar("python")
    'sbwkrq'
    >>> encrypt_caesar("Python3.6")
    'Sbwkrq3.6'
    >>> encrypt_caesar("")
    ''
    """
    chiphertext = ""
    for i, bukv in enumerate(plaintext):
        if bukv.isalpha():
            a = ord(bukv)
            if bukv.isupper() and a >= 91 - shift:
                chiphertext += chr(a - 26 + shift)
            elif bukv.islower() and a >= 123 - shift:
                chiphertext += chr(a - 26 + shift)
            else:
                chiphertext += chr(a + shift)
        else:
            chiphertext += bukv
    return chiphertext


def decrypt_caesar(chiphertext: str, shift: int = 3) -> str:
    """
    Decrypts a chiphertext using a Caesar cipher.
    >>> decrypt_caesar("SBWKRQ")
    'PYTHON'
    >>> decrypt_caesar("sbwkrq")
    'python'
    >>> decrypt_caesar("Sbwkrq3.6")
    'Python3.6'
    >>> decrypt_caesar("")
    ''
    """
    plaintext = ""
    for i, bukv in enumerate(chiphertext):
        if bukv.isalpha():
            a = ord(bukv)
            if bukv.isupper() and a <= 64 + shift:
                plaintext += chr(a + 26 - shift)
            elif bukv.islower() and a <= 96 + shift:
                plaintext += chr(a + 26 - shift)
            else:
                plaintext += chr(a - shift)
        elif chiphertext.isspace():
            continue
        else:
            plaintext += bukv
    return plaintext


def caesar_breaker_brute_force(chiphertext: str, dictionary: tp.Set[str]) -> int:
    """
    Brute force breaking a Caesar cipher.
    """
    best_shift = 0
    # PUT YOUR CODE HERE
    return best_shift
