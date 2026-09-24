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

    tokenized_de_text = tokenize(de_text)
    cleaned_de_text = remove_stop_words(tokenized_de_text, stopwords)
    freq_dict = calculate_frequencies(cleaned_de_text)
    top_words = get_top_n_words(freq_dict, 7)

    unknown_profile = create_language_profile("unk", unknown_text, stopwords)
    de_profile = create_language_profile ("de", de_text, stopwords)
    en_profile = create_language_profile("en", en_text, stopwords)
    result = detect_language_by_top_n(unknown_profile, de_profile, en_profile, 15)
    result = detect_language_by_mse(unknown_profile, de_profile, en_profile)

    assert result, "Detection result is None"


if __name__ == "__main__":
    main()
