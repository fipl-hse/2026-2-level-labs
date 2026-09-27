"""
Language detection starter.
"""
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
    tokens = tokenize(de_text)
    assert tokens is not None
    print(f"Tokenised text:{tokens}")
    cleaned_tokens = remove_stop_words(tokens,stopwords)
    assert cleaned_tokens is not None
    print(f"Cleaned tokens from stop-words{cleaned_tokens}")
    counts = calculate_frequencies(cleaned_tokens)
    assert counts is not None
    print(f"Dictionary with frequences:{counts}")
    result = get_top_n_words(counts,7)
    assert result is not None
    print(f"top-7 words from the text:{result}")
    en_profile = create_language_profile('en', en_text, stopwords)
    de_profile = create_language_profile('de', de_text, stopwords)
    unk_profile = create_language_profile('unk', unknown_text, stopwords)
    assert en_profile is not None                          
    assert de_profile is not None
    assert unk_profile is not None
    detect_lang = detect_language_by_top_n(unk_profile,de_profile,en_profile,15)
    print(f"Unknown language is {detect_lang}")
    detect_lang_by_mse = detect_language_by_mse(unk_profile,en_profile,de_profile)
    print(f"Unknown language detected by mse is {detect_lang_by_mse}")
    assert result, "Detection result is None"


if __name__ == "__main__":
    main()
