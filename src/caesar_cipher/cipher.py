from caesar_cipher.constants import(
    ALPHABET_SIZE,
    UPPERCASE_LETTERS,
    LOWERCASE_LETTERS
)

class CaesarCipher:

    def __init__(self, key: int, alphabet: str = "ABCDEFGHIJKLMNOPQRSTUVWXYZ") -> None:

        if not -25 <= key <= 26:
            raise ValueError("Key must be between -25 and 26")

        self.key = key
        self.alphabet = alphabet

        if alphabet and len(set(alphabet)) != len(alphabet):
            raise ValueError("Alphabet must not contain duplicate characters")

    def _shift_char(self, char: str, shift: int) -> str:

        upper_alphabet = self.alphabet.upper()
        lower_alphabet = self.alphabet.lower()

        if char in upper_alphabet:
            alphabet = upper_alphabet
        elif char in lower_alphabet:
            alphabet = lower_alphabet
        else: return char

        index = alphabet.index(char)
        return alphabet[(index + shift) % len(alphabet)]

    def encrypt(self, plaintext: str) -> str:
        return "".join(self._shift_char(char, self.key) for char in plaintext)

    def decrypt(self, ciphertext: str) -> str:
        return "".join(self._shift_char(char, -self.key) for char in ciphertext)

    @staticmethod
    def crack(ciphertext: str) -> list[tuple[int,str]]:
        results = []
        for shift in range(ALPHABET_SIZE):
            cipher = CaesarCipher(key = shift)
            decrypted = cipher.decrypt(ciphertext)
            results.append((shift, decrypted))
        return results