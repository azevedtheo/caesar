from caesar_cipher.cipher import CaesarCipher


def test_encrypt():
    cipher = CaesarCipher(key=3)

    assert cipher.encrypt("Hello World!") == "Khoor Zruog!"


def test_decrypt():
    cipher = CaesarCipher(key=3)

    assert cipher.decrypt("Khoor Zruog!") == "Hello World!"


def test_encrypt_preserves_non_letters():
    cipher = CaesarCipher(key=3)

    assert cipher.encrypt("Hello, World! 123") == "Khoor, Zruog! 123"


def test_decrypt_preserves_non_letters():
    cipher = CaesarCipher(key=3)

    assert cipher.decrypt("Khoor, Zruog! 123") == "Hello, World! 123"


def test_key_wraps_around():
    cipher = CaesarCipher(key=3)

    assert cipher.encrypt("XYZ") == "ABC"