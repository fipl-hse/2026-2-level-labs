"""
Language detection starter.
"""

# pylint: disable=unused-variable, duplicate-code
from main import (
    calculate_frequencies,
    check_profile,
    compare_profiles_by_top_n,
    create_language_profile,
    detect_language_by_top_n,
    get_top_n_words,
    remove_stop_words,
    tokenize,
)


def main():
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


    print("Tokens: ", tokenize(de_text))
    print("Tokens without stopwords: ", remove_stop_words(tokenize(de_text), stopwords))
    frequencies = calculate_frequencies(remove_stop_words(tokenize(de_text), stopwords))
    print("Frequency dictionary: ", frequencies)
    top_words = get_top_n_words(frequencies, 7)
    print("Top 7 popular words: ", top_words)

    en_profile = create_language_profile('en', en_text, stopwords)
    de_profile = create_language_profile('de', de_text, stopwords)
    unknown_profile = create_language_profile('unknown', unknown_text, stopwords)
    if not check_profile(en_profile) or not check_profile(de_profile) or not check_profile(unknown_profile):
        return

    comparison_en = compare_profiles_by_top_n(unknown_profile, en_profile, 15)
    comparison_de = compare_profiles_by_top_n(unknown_profile, de_profile, 15)
    if comparison_en is None or comparison_de is None:
        return

    result = detect_language_by_top_n(unknown_profile, en_profile, de_profile, 15)
    print('Detected Language: ', result)


if __name__ == "__main__":
    main()