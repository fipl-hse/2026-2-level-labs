"""
Language detection starter.
"""
from main import (
    calculate_frequencies,
    create_language_profile,
    detect_language_by_mse,
    detect_language_by_top_n,
    get_top_n_words,
    remove_stop_words,
    tokenize,
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
        stopwords = [word.lower() for word in file.read().splitlines() if word.strip()]
    with open("lab_1_classify_profile/assets/texts/en.txt", "r", encoding="utf-8") as file:
        en_text = file.read()


    tokenized_de_text = tokenize(de_text)
    cleaned_de_tokens = remove_stop_words(tokenized_de_text, stopwords)
    freq_dict = calculate_frequencies(cleaned_de_tokens)
    top_n_words = get_top_n_words(freq_dict, 7)

    for word in top_n_words:
        print(word)

    unk_lang_profile = create_language_profile("unk", unknown_text, stopwords)
    de_lang_profile = create_language_profile("de", de_text, stopwords)
    en_lang_profile = create_language_profile("en", en_text, stopwords)

    lang_by_top_n = detect_language_by_top_n(unk_lang_profile, de_lang_profile, en_lang_profile, 15)
    print(lang_by_top_n)

    lang_by_mse = detect_language_by_mse(unk_lang_profile, de_lang_profile, en_lang_profile)
    print(lang_by_mse)

    result = lang_by_mse
    assert result, "Detection result is None"


if __name__ == "__main__":
    main()
