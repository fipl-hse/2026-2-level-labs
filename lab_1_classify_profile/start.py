"""
Language detection starter.
"""

# pylint: disable=unused-variable, duplicate-code
from lab_1_classify_profile.main import (
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
    result = None
    tokens = tokenize(de_text)

    if tokens is not None:
        cleaned_tokens = remove_stop_words(tokens, stopwords)

    if cleaned_tokens is not None:
        freq_dict = calculate_frequencies(cleaned_tokens)

    if freq_dict is not None:
        result = get_top_n_words(freq_dict, 7)

    print("Топ 7 популярных слов (нем):", result)

    de_profile = create_language_profile("de", de_text, stopwords)
    en_profile = create_language_profile("en", en_text, stopwords)
    unknown_profile = create_language_profile("unknown", unknown_text, stopwords)

    if de_profile is not None and en_profile is not None and unknown_profile is not None:
        result = detect_language_by_top_n(unknown_profile, en_profile, de_profile, 15)

    print("Язык текста:", result)

    assert result, "Detection result is None"


if __name__ == "__main__":
    main()
