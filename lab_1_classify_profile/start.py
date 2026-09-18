"""
Language detection starter.
"""

# pylint: disable=unused-variable, duplicate-code
try:
    from .main import (
        tokenize,
        remove_stop_words,
        calculate_frequencies,
        get_top_n_words,
        create_language_profile,
        compare_profiles_by_top_n,
        detect_language_by_top_n,
    )
except ImportError:
    from main import (
        tokenize,
        remove_stop_words,
        calculate_frequencies,
        get_top_n_words,
        create_language_profile,
        compare_profiles_by_top_n,
        detect_language_by_top_n,
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


    de_tokens = tokenize(de_text)
    de_tokens = remove_stop_words(de_tokens, stopwords)
    de_frequencies = calculate_frequencies(de_tokens)
    top_7_words = get_top_n_words(de_frequencies, 7)

    print(top_7_words)

    en_profile = create_language_profile(
        "en",
        en_text,
        stopwords
    )

    de_profile = create_language_profile(
        "de",
        de_text,
        stopwords
    )

    unknown_profile = create_language_profile(
        "unknown",
        unknown_text,
        stopwords
    )

    result = detect_language_by_top_n(
        unknown_profile,
        en_profile,
        de_profile,
        15
    )

    print(result)

    assert result, "Detection result is None"


if __name__ == "__main__":
    main()
