"""
Language detection starter.
"""

# pylint: disable=unused-variable, duplicate-code

from main import tokenize
from main import remove_stop_words
from main import calculate_frequencies
from main import get_top_n_words
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
    print(f"Выделила токены из текста:{tokens}")
    cleaned_tokens=remove_stop_words(tokens,stopwords)
    print(f"Очистка токенов от стоп слов:{cleaned_tokens}")
    counts=calculate_frequencies(cleaned_tokens)
    print(f"Частотный словарь:{counts}")
    result = get_top_n_words(counts,7)
    print(f"Топ-7 популярных слов текста{result}")
    assert result, "Detection result is None"


if __name__ == "__main__":
    main()
