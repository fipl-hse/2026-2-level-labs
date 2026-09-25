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
    result = None

    #mark 4
    tokens = tokenize(de_text)
    if tokens is None:
        return

    processed_tokens = remove_stop_words(tokens, stopwords)
    if processed_tokens is None:
        return

    freq_dict = calculate_frequencies(processed_tokens)
    if freq_dict is None:
        return

    result = get_top_n_words(freq_dict, 7)
    print(result)

    #mark 6
    en_profile = create_language_profile("en", en_text, stopwords)
    assert en_profile is not None, "en_profile resulted as None"
    de_profile = create_language_profile("de", de_text, stopwords)
    assert de_profile is not None, "de_profile resulted as None"
    unknown_profile = create_language_profile("unknown", unknown_text, stopwords)
    assert unknown_profile is not None, "unknown_profile resulted as None"
    result = detect_language_by_top_n(unknown_profile, de_profile, en_profile, 15)
    print(result)

    #mark 8

    result = detect_language_by_mse(
        unknown_profile,
        en_profile,
        de_profile,
    )
    print(result)
    assert result, "Detection result is None"


if __name__ == "__main__":
    main()
