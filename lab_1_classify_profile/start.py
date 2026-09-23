"""
Language detection starter.
"""
from main import (
    calculate_frequencies,
    get_top_n_words,
    remove_stop_words,
    tokenize,
    create_language_profile,
    check_profile,
    compare_profiles_by_top_n,
    detect_language_by_top_n
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
    result = None
    # Mark 4
    de_tokens = tokenize(de_text)
    de_tokens = remove_stop_words(de_tokens, stopwords)
    de_frequency = calculate_frequencies(de_tokens)
    de_get_top_n_words = get_top_n_words(de_frequency, 7)
    result = de_get_top_n_words
    print(result)

    # Mark 6

    en_language_profile = create_language_profile("English", en_text, stopwords)
    de_language_profile = create_language_profile("German", de_text, stopwords)
    unknown_language_profile = create_language_profile("Unknown", unknown_text, stopwords)

    compare_languages = detect_language_by_top_n(unknown_language_profile, en_language_profile, de_language_profile, 15)

    print(compare_languages)


    assert result, "Detection result is None"

if __name__ == "__main__":
    main()
