"""
Language detection starter.
"""

# pylint: disable=unused-variable, duplicate-code

from main import (
    calculate_frequencies,
    create_language_profile,
    detect_language_by_top_n,
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
    cl_tokens = remove_stop_words(tokens, stopwords)
    freq_dict = calculate_frequencies(cl_tokens)
    result = get_top_n_words(freq_dict, 7)
    assert result, "Detection result is None"

    en_profile = create_language_profile('en',en_text, stopwords)
    de_profile = create_language_profile('de', de_text, stopwords)
    unknown_profile = create_language_profile("unknown", unknown_text, stopwords)

    language = detect_language_by_top_n(unknown_profile, en_profile, de_profile, 15)
    print(language)

if __name__ == "__main__":
    main()


