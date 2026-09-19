from collections import Counter

from caesar_cipher.constants import ENGLISH_LETTER_FREQUENCY

class FrequencyAnalyzer: 

    def __init__(self) -> None:
        self.reference_frequencies = ENGLISH_LETTER_FREQUENCY

    def calc_chi_squared(self, text: str) -> float:
            text_upper = text.upper()
            letter_counts = Counter(char for char in text_upper if char.isalpha())

            if not letter_counts:
                return float("inf")

            total_letters = sum(letter_counts.values())
            chi_squared = 0.0

            for letter, expected_freq in self.reference_frequencies.items():
                observed_count = letter_counts.get(letter, 0)
                expected_count = (expected_freq / 100) * total_letters

                if expected_count > 0:
                    chi_squared += ((observed_count - expected_count)**2) / expected_count

            return chi_squared

    def score_text(self, text: str) -> float:
        return self.calc_chi_squared(text)
    
    def rank_candidates(self,
                        candidates: list[tuple[int, str]]
                        ) -> list[tuple[int, str, float]]:
        scored = [
            (shift, text, self.score_text(text))
            for shift, text in candidates
        ]
        return sorted(scored, key=lambda x: x[2])
  