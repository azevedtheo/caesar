from caesar_cipher.analyzer import FrequencyAnalyzer


def test_calc_chi_squared_returns_float():
    analyzer = FrequencyAnalyzer()

    score = analyzer.calc_chi_squared("hello world")

    assert isinstance(score, float)


def test_calc_chi_squared_is_non_negative():
    analyzer = FrequencyAnalyzer()

    score = analyzer.calc_chi_squared("hello world")

    assert score >= 0