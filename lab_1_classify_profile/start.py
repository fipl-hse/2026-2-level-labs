"""
Language detection starter.
"""

# pylint: disable=unused-variable, duplicate-code


from main import tokenize
from main import remove_stop_words
from main import calculate_frequencies
from main import  get_top_n_words


# Токенизируем тексты
#de_tokens = tokenize(de.txt)
#unknown_tokens = tokenize(unknown.txt)
#en_tokens = tokenize(en.txt)

    # Удаляем стоп-слова
#de_tokens = remove_stop_words(de.txt, stopwords)
#unknown_tokens = remove_stop_words(unknown.txt, stopwords)
#en_tokens = remove_stop_words(en.txt, stopwords)

    # Считаем частоты
#de_freq = calculate_frequencies(de.txt)
#unknown_freq = calculate_frequencies(unknown.txt)
#en_freq = calculate_frequencies(en.txt)

    # Получаем топ-10 слов
#de_top = get_top_n_words(de_freq, 10)
#unknown_top = get_top_n_words(unknown_freq, 10)
#en_top = get_top_n_words(en_freq, 10)


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

    de_tokens = tokenize(de_text)
    unknown_tokens = tokenize(unknown_text)
    en_tokens = tokenize(en_text)

    de_tokens = remove_stop_words(de_tokens, stopwords)
    unknown_tokens = remove_stop_words(unknown_tokens, stopwords)
    en_tokens = remove_stop_words(en_tokens, stopwords)

    de_freq = calculate_frequencies(de_tokens)
    unknown_freq = calculate_frequencies(unknown_tokens)
    en_freq = calculate_frequencies(en_tokens)

    result = None
    assert result, "Detection result is None"


if __name__ == "__main__":
    main()

