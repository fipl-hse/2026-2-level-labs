"""
Language detection starter.
"""

# pylint: disable=unused-variable, duplicate-code
from main import (
    calculate_frequencies,
    calculate_mse,
    compare_profiles_by_mse,
    create_language_profile,
    detect_language_by_mse,
    detect_language_by_top_n,
    get_top_n_words,
    remove_stop_words,
    tokenize,
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
    if de_tokens is None:
        return None

    de_tokens = remove_stop_words(de_tokens, stopwords)
    if de_tokens is None:
        return None

    de_freq = calculate_frequencies(de_tokens)
    if de_freq is None:
        return None

    de_top_words = get_top_n_words(de_freq, 7)
    if de_top_words is None:
        return None

    en_tokens = tokenize(en_text)
    if en_tokens is None:
        return None

    en_tokens = remove_stop_words(en_tokens, stopwords)
    if en_tokens is None:
        return None

    en_freq = calculate_frequencies(en_tokens)
    if en_freq is None:
        return None

    en_top_words = get_top_n_words(en_freq, 7)
    if en_top_words is None:
        return None

    print(f"Top 7 words from German text: {de_top_words}")

    de_profile = create_language_profile("de", de_text, stopwords)
    en_profile = create_language_profile("en", en_text, stopwords)
    unknown_profile = create_language_profile("unknown", unknown_text, stopwords)

    if (de_profile is None or \
    en_profile is None or \
    unknown_profile is None):
        return None

    result_detected_lang = detect_language_by_top_n(unknown_profile, de_profile, en_profile, 15)
    print(f"Language detected by top 15 words: {result_detected_lang}")

    result = detect_language_by_mse(
        unknown_profile=unknown_profile,
        profile_1=de_profile,
        profile_2=en_profile
    )
    print(f"Language detected by MSE: {result}")

    de_mse = compare_profiles_by_mse(unknown_profile, de_profile)
    en_mse = compare_profiles_by_mse(unknown_profile, en_profile)

    print(f"MSE of German language: {de_mse}")
    print(f"MSE of English language: {en_mse}")

    assert result, "Detection result is None"
    return None

if __name__ == "__main__":
    main()
