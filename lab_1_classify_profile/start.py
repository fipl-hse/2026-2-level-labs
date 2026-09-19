"""
Language detection starter.
"""

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



    from main import calculate_frequencies, get_top_n_words, remove_stop_words, tokenize


    de_tokens = tokenize(de_text)
    #unknown_tokens = tokenize(unknown_text)
    #en_tokens = tokenize(en_text)

    if de_tokens is None: #or unknown_tokens is None or en_tokens is None:
        return None


    de_filtered = remove_stop_words(de_tokens, stopwords)
    #unknown_filtered = remove_stop_words(unknown_tokens, stopwords)
    #en_filtered = remove_stop_words(en_tokens, stopwords)

    if de_filtered is None: #or unknown_filtered is None or en_filtered is None:
        return None


    de_frequencies = calculate_frequencies(de_filtered)
    #unknown_frequencies = calculate_frequencies(unknown_filtered)
    #en_frequencies = calculate_frequencies(en_filtered)

    if de_frequencies is None: #or unknown_frequencies is None or en_frequencies is None:
        return None


    de_top_n_tokens = get_top_n_words(de_frequencies, 7)
    print(de_top_n_tokens)


    #result = None
    #assert result, "Detection result is None"

if __name__ == "__main__":
    main()
