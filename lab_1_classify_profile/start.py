"""
Language detection starter.
"""

# pylint: disable=unused-variable, duplicate-code

from lab_1_classify_profile.main import(
tokenize,
remove_stop_words,
calculate_frequencies,
get_top_n_words,
detect_language_by_top_n,
create_language_profile,
detect_language_by_mse)

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
    tokens=tokenize(de_text)
    print(f"Tokenised text:{tokens}")
    cleaned_tokens=remove_stop_words(tokens,stopwords)
    print(f"Cleaned tokens from stop-words{cleaned_tokens}")
    counts=calculate_frequencies(cleaned_tokens)
    print(f"Dictionary with frequences:{counts}")
    result = get_top_n_words(counts,7)
    print(f"top-7 words from the text:{result}")
    en_profile = create_language_profile('en', en_text, stopwords)
    de_profile = create_language_profile('de', de_text, stopwords)
    unk_profile = create_language_profile('unk', unknown_text, stopwords)
    detect_lang = detect_language_by_top_n(unk_profile,de_profile,en_profile,15)
    print(f"Unknown language is {detect_lang}")
    detect_lang_by_mse = detect_language_by_mse(unk_profile,en_profile,de_profile)
    print(f"Unknown language detected by mse is {detect_lang_by_mse}")
    assert result, "Detection result is None"


if __name__ == "__main__":
    main()
