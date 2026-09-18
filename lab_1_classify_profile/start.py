"""
Language detection starter.
"""

# pylint: disable=unused-variable, duplicate-code
from main import tokenize, remove_stop_words, calculate_frequencies, get_top_n_words

def main() -> None:
    """
    Launches an implementation.
    """
    with open("assets/texts/de.txt", "r", encoding="utf-8") as file:
        de_text = file.read()
    with open("assets/texts/unknown.txt", "r", encoding="utf-8") as file:
        unknown_text = file.read()
    with open("assets/stopwords.txt", "r", encoding="utf-8") as file:
        stopwords = file.read().split("\n")
    with open("assets/texts/en.txt", "r", encoding="utf-8") as file:
        en_text = file.read()

    tokenized_de_text = tokenize(de_text)
    cleaned_de_text = remove_stop_words(tokenized_de_text, stopwords)
    freq_dict = calculate_frequencies(cleaned_de_text)
    top_words = get_top_n_words(freq_dict, 7)

    #result = None
    #assert result, "Detection result is None"


if __name__ == "__main__":
    main()
