"""
Language detection starter.
"""

from lab_1_classify_profile.main import (
    calculate_frequencies,
    get_top_n_words,
    remove_stop_words,
    tokenize,
)

# pylint: disable=unused-variable, duplicate-code


def main() -> None:
    """
    Launches an implementation.
    """
    with open("lab_1_classify_profile/assets/texts/de.txt", "r", encoding="utf-8") as file:
        de_text = file.read()
    with open("lab_1_classify_profile/assets/texts/unknown.txt", "r", encoding="utf-8") as file:
        unknown_text = file.read()
    with open("lab_1_classify_profile/assets/stopwords.txt", "r", encoding="utf-8") as file:
        stopwords = file.read().split("\n")
    with open("lab_1_classify_profile/assets/texts/en.txt", "r", encoding="utf-8") as file:
        en_text = file.read()

    de_tokens = tokenize(de_text)

    de_tokens = remove_stop_words(de_tokens, stopwords)

    de_frequency = calculate_frequencies(de_tokens)

    result = de_frequency

    assert result, "Detection result is None"


if __name__ == "__main__":
    main()
