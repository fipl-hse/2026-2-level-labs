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

    tokens_de = tokenize(de_text)
    tokens_de_clean = remove_stop_words(tokens_de, stopwords)
    freq_de = calculate_frequencies(tokens_de_clean)
    top_7_de = get_top_n_words(freq_de, 7)
    print("Top-7 DE:", top_7_de)

    en_profile = create_language_profile("en", en_text, stopwords)
    de_profile = create_language_profile("de", de_text, stopwords)
    unknown_profile = create_language_profile("unknown", unknown_text, stopwords)

    result_top_n = detect_language_by_top_n(unknown_profile, en_profile, de_profile, 15)
    print("Detected by Top-N:", result_top_n)

    result_mse = detect_language_by_mse(unknown_profile, en_profile, de_profile)
    print("Detected by MSE:", result_mse)

    result = result_mse
    assert result, "Detection result is None"


if __name__ == "__main__":
    main()
