def encrypt_vigenere(plaintext: str, keyword: str) -> str:
    """
    Encrypts plaintext using a Vigenere cipher.

    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """
    ciphertext = ""
    a_a = 0
    while len(plaintext) > len(keyword):
        keyword += keyword[a_a]
        a_a += 1
    for i, bukv in enumerate(keyword):
        if bukv.isupper():
            key = ord(bukv) - 65
        elif bukv.islower():
            key = ord(bukv) - 97
        if plaintext[i].isalpha():
            c_c = ord(plaintext[i])
            if plaintext[i].isupper() and c_c >= 91 - key:
                ciphertext += chr(c_c - 26 + key)
            elif plaintext[i].islower() and c_c >= 123 - key:
                ciphertext += chr(c_c - 26 + key)
            else:
                ciphertext += chr(c_c + key)
        else:
            ciphertext += plaintext[i]
    return ciphertext


def decrypt_vigenere(ciphertext: str, keyword: str) -> str:
    """
    Decrypts a ciphertext using a Vigenere cipher.

    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'
    """
    plaintext = ""
    a_b = 0
    while len(ciphertext) > len(keyword):
        keyword += keyword[a_b]
        a_b += 1
    for i, bukv in enumerate(keyword):
        if bukv.isupper():
            key = ord(bukv) - 65
        elif bukv.islower():
            key = ord(bukv) - 97
        if ciphertext[i].isalpha():
            c_b = ord(ciphertext[i])
            if ciphertext[i].isupper() and c_b <= 64 + key:
                plaintext += chr(c_b + 26 - key)
            elif ciphertext[i].islower() and c_b <= 96 + key:
                plaintext += chr(c_b + 26 - key)
            else:
                plaintext += chr(c_b - key)
        else:
            plaintext += ciphertext[i]
    return plaintext
