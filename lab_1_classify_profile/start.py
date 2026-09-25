"""
Language detection starter.
"""

from lab_1_classify_profile.main import (
    calculate_frequencies,
    create_language_profile,
    detect_language_by_mse,
    detect_language_by_top_n,
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

    # Mark 4
    de_tokens = tokenize(de_text)

    de_tokens = remove_stop_words(de_tokens, stopwords)

    de_frequency = calculate_frequencies(de_tokens)

    de_get_top_n_words = get_top_n_words(de_frequency, 7)

    result = de_get_top_n_words

    print(result)

    # определение языка
    unknown_profile = create_language_profile("unknown", unknown_text, stopwords)

    en_profile = create_language_profile("en", en_text, stopwords)

    de_profile = create_language_profile("de", de_text, stopwords)

    if unknown_profile is None or en_profile is None or de_profile is None:
        return None

    detected = detect_language_by_top_n(unknown_profile, en_profile, de_profile, 15)
    print(f"Detected language: {detected}")


if __name__ == "__main__":
    main()
