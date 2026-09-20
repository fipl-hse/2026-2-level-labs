"""
Language detection starter.
"""

# pylint: disable=unused-variable, duplicate-code
from lab_1_classify_profile.main import (
    tokenize,
    remove_stop_words,
    calculate_frequencies,
    get_top_n_words,
    create_language_profile,
    detect_language_by_top_n,
    detect_language_by_mse
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
    # result = None
    # assert result, "Detection result is None"

    tokens = tokenize(de_text)
    assert tokens is not None, "tokenize resulted as None"
    tokens_without_stop_words = remove_stop_words(tokens, stopwords)
    assert tokens_without_stop_words is not None, "tokens_without_stop_words resulted as None"
    freq_dict = calculate_frequencies(tokens_without_stop_words)
    assert freq_dict is not None, "freq_dict resulted as None"
    top_words = get_top_n_words(freq_dict, 7)
    assert top_words is not None, "get_top_n_words resulted as None"
    print(top_words)

    en_profile = create_language_profile("en", en_text, stopwords)
    de_profile = create_language_profile("de", de_text, stopwords)
    unknown_profile = create_language_profile("unknown", unknown_text, stopwords)
    assert en_profile is not None, "English profile is None"
    assert de_profile is not None, "Deutsch profile is None"
    assert unknown_profile is not None, "Unknown profile is None"

    result_by_top_n = detect_language_by_top_n(unknown_profile, en_profile, de_profile, 15)
    assert result_by_top_n, "Detection by top n words is None"
    print(result_by_top_n)

    result_by_mse = detect_language_by_mse(unknown_profile, en_profile, de_profile)
    assert result_by_mse, "Detection by mse is None"
    print(result_by_mse)

if __name__ == "__main__":
    main()
