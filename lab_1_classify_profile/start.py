"""
Language detection starter.
"""

# pylint: disable=unused-variable, duplicate-code


from lab_1_classify_profile.main import (
    calculate_frequencies,
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
    with open("lab_1_classify_profile/assets/texts/de.txt", "r", encoding="utf-8") as file:
        de_text = file.read()
    with open("lab_1_classify_profile/assets/texts/unknown.txt", "r", encoding="utf-8") as file:
        unknown_text = file.read()
    with open("lab_1_classify_profile/assets/stopwords.txt", "r", encoding="utf-8") as file:
        stopwords = file.read().split("\n")
    with open("lab_1_classify_profile/assets/texts/en.txt", "r", encoding="utf-8") as file:
        en_text = file.read()

    de_tokens = tokenize(de_text)

    if de_tokens is None:
        return

    de_tokens = remove_stop_words(de_tokens, stopwords)

    if de_tokens is None:
        return

    de_freq = calculate_frequencies(de_tokens)

    if de_freq is None:
        return

    top_n_words = get_top_n_words(de_freq, 7)

    if top_n_words is None:
        return

    print(f"Топ-7 слов немецкого текста: {top_n_words}")

    de_profile = create_language_profile("de", de_text, stopwords)
    en_profile = create_language_profile("en", en_text, stopwords)
    unknown_profile = create_language_profile("unknown", unknown_text, stopwords)

    if de_profile is None or \
    en_profile is None or \
    unknown_profile is None:
        return

    detected_language_top_n = detect_language_by_top_n(unknown_profile, en_profile, de_profile, 15)

    print(f"Определённый язык (по топ-15 словам): {detected_language_top_n}")

    result = detect_language_by_mse(
        unknown_profile=unknown_profile,
        profile_1=en_profile,
        profile_2=de_profile
    )
    print(result)
    assert result, "Detection result is None"




if __name__ == "__main__":
    main()
