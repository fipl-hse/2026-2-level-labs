"""
Language detection starter.
"""
from main import tokenize, remove_stop_words, calculate_frequencies, get_top_n_words

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
    #result = None
    #assert result, "Detection result is None"
    print(stopwords)
    tokenized_de_text = tokenize(de_text)
    cleaned_de_tokens = remove_stop_words(tokenized_de_text, stopwords)
    freq_dict = calculate_frequencies(cleaned_de_tokens)
    top_n_words = get_top_n_words(freq_dict, 7)

    for word in top_n_words:
        print(word)
if __name__ == "__main__":
    main()
