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

    # Практическое задание mark 4
    tokens = tokenize(de_text)
    if tokens is None:
        return

    tokens_without_stopwords = remove_stop_words(tokens, stopwords)
    if tokens_without_stopwords is None:
        return

    freq_dict = calculate_frequencies(tokens_without_stopwords)
    if freq_dict is None:
        return

    result = get_top_n_words(freq_dict, 7)
    print(result)

    # Практическое задание mark 6
    de_profile = create_language_profile("de", de_text, stopwords)
    en_profile = create_language_profile("en", en_text, stopwords)
    unknown_profile = create_language_profile("unknown", unknown_text, stopwords)
    if (de_profile is None
        or en_profile is None
        or unknown_profile is None
    ):
        return

    result = detect_language_by_top_n(unknown_profile, de_profile, en_profile, 15)
    if isinstance(result,tuple) is False:
        return
    print(result)

    # Практическое задание mark 8
    result = detect_language_by_mse(
        unknown_profile,
        en_profile,
        de_profile,
    )
    if isinstance(result,tuple) is False:
        return

    print(result)

    assert result, "Detection result is None"


if __name__ == "__main__":
    main()
