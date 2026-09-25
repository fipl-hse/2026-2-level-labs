"""
Language detection starter.
"""

# pylint: disable=unused-variable, duplicate-code

from main import (
    tokenize,
    remove_stop_words,
    calculate_frequencies,
    get_top_n_words
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
    result = None
    assert result, "Detection result is None"

    #demonstration of getting top-7 words
    tokens = tokenize(de_text)
    filtered_tokens = remove_stop_words(tokens, stopwords)
    freq_dict = calculate_frequencies(filtered_tokens)
    top_7_words = get_top_n_words(freq_dict, 7)

    print(top_7_words)


if __name__ == "__main__":
    main()

