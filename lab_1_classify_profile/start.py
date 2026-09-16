"""
Language detection starter.
"""

# pylint: disable=unused-variable, duplicate-code

from lab_1_classify_profile.main import (
    calculate_frequencies,
    get_top_n_words,
    remove_stop_words,
    tokenize,
)


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
    tokens = tokenize(de_text)
    tokens = remove_stop_words(tokens, stopwords)
    frequencies = calculate_frequencies(tokens)
    result = get_top_n_words(frequencies, 7)
    print(result)


if __name__ == "__main__":
    main()
