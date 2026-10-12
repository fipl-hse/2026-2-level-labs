"""
Language detection starter.
"""

# pylint: disable=unused-variable, duplicate-code, too-many-return-statements

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
    with open("lab_1_classify_profile/assets/texts/en.txt", "r", encoding="utf-8") as file:
        en_text = file.read()
    with open("lab_1_classify_profile/assets/texts/de.txt", "r", encoding="utf-8") as file:
        de_text = file.read()
    with open("lab_1_classify_profile/assets/texts/unknown.txt", "r", encoding="utf-8") as file:
        unknown_text = file.read()
    with open("lab_1_classify_profile/assets/stopwords.txt", "r", encoding="utf-8") as file:
        stopwords = file.read().splitlines()

    tokens = tokenize(en_text)
    filtered_tokens = remove_stop_words(tokens, stopwords)
    freq_dict = calculate_frequencies(filtered_tokens)
    top_7 = get_top_n_words(freq_dict, 7)

    print("Токены (первые 20):", tokens[:20])
    print("Без стоп-слов (первые 20):", filtered_tokens[:20])
    print("Топ-7 популярных слов:", top_7)

    en_profile = create_language_profile("en", en_text, stopwords)
    de_profile = create_language_profile("de", de_text, stopwords)
    unknown_profile = create_language_profile("unknown", unknown_text, stopwords)

    if en_profile is None or de_profile is None or unknown_profile is None:
        print("Не удалось создать профили")
        return

    detected = detect_language_by_top_n(unknown_profile, en_profile, de_profile, 15)

    if detected is None:
        print("Не удалось определить язык")
        return

    print("Определённый язык:", detected)


if __name__ == "__main__":
    main()
