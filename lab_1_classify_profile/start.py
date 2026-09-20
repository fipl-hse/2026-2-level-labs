"""
Language detection starter.
"""

# pylint: disable=unused-variable, duplicate-code
from main import (
    tokenize,
    remove_stop_words,
    calculate_frequencies,
    get_top_n_words,
    create_language_profile,
    compare_profiles_by_top_n,
    detect_language_by_top_n
)


def main() -> None:
    """
    Launches an implementation.
    """
    with open(
        "lab_1_classify_profile/assets/texts/de.txt", "r", encoding="utf-8"
    ) as file:
        de_text = file.read()
    with open(
        "lab_1_classify_profile/assets/texts/unknown.txt", "r", encoding="utf-8"
    ) as file:
        unknown_text = file.read()
    with open(
        "lab_1_classify_profile/assets/stopwords.txt", "r", encoding="utf-8"
    ) as file:
        stopwords = file.read().split("\n")
    with open(
        "lab_1_classify_profile/assets/texts/en.txt", "r", encoding="utf-8"
    ) as file:
        en_text = file.read()

    de_tokens = tokenize(de_text)
    en_tokens = tokenize(en_text)
    unknown_tokens = tokenize(unknown_text)

    de_tokens = remove_stop_words(de_tokens, stopwords)
    en_tokens = remove_stop_words(en_tokens, stopwords)
    unknown_tokens = remove_stop_words(unknown_tokens, stopwords)

    de_freq = calculate_frequencies(de_tokens)
    en_freq = calculate_frequencies(en_tokens)
    unknown_freq = calculate_frequencies(unknown_tokens)

    de_top_words = get_top_n_words(de_freq, 15)
    en_top_words = get_top_n_words(en_freq, 15)
    unknown_top_words = get_top_n_words(unknown_freq, 15)

    de_profile = create_language_profile("de", de_text, stopwords)
    en_profile = create_language_profile("en", en_text, stopwords)
    unknown_profile = create_language_profile("unknown", unknown_text, stopwords)

    result = detect_language_by_top_n(unknown_profile, de_profile, en_profile, 15)
    print(result)
    assert result, "Detection result is None"


if __name__ == "__main__":
    main()