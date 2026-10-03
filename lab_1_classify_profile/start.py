"""
Language detection starter.
"""

# pylint: disable=unused-variable, duplicate-code
from main import (
    calculate_frequencies,
    calculate_mse,
    compare_profiles_by_mse,
    create_language_profile,
    detect_language_advanced,
    detect_language_by_mse,
    detect_language_by_top_n,
    get_top_n_words,
    print_report,
    remove_stop_words,
    save_profile,
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

    result = None

    tokenized_text = tokenize(de_text)
    if tokenized_text is None:
        return None

    text_without_stopwords = remove_stop_words(tokenized_text, stopwords)
    if text_without_stopwords is None:
        return None

    calculated_frequencies = calculate_frequencies(text_without_stopwords)

    if calculated_frequencies is None:
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

    if (unk_profile is None
        or de_profile is None
        or en_profile is None):
        return None

    print(get_top_n_words(calculated_frequencies, 7))
    print(detect_language_by_top_n(unk_profile, en_profile, de_profile, 15))
    result = detect_language_by_mse(unk_profile, en_profile, de_profile)

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
