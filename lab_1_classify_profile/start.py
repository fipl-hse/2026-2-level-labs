"""
Language detection starter.
"""

# pylint: disable=unused-variable, duplicate-code, too-many-return-statements, too-many-locals

from lab_1_classify_profile.main import (
    calculate_frequencies,
    check_profile,
    compare_profiles_by_top_n,
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
    with open("lab_1_classify_profile/assets/texts/en.txt", "r", encoding="utf-8") as file:
        en_text = file.read()
    with open("lab_1_classify_profile/assets/texts/de.txt", "r", encoding="utf-8") as file:
        de_text = file.read()
    with open("lab_1_classify_profile/assets/texts/unknown.txt", "r", encoding="utf-8") as file:
        unknown_text = file.read()
    with open("lab_1_classify_profile/assets/stopwords.txt", "r", encoding="utf-8") as file:
        stopwords = file.read().splitlines()

    tokens = tokenize(en_text)
    if tokens is None:
        print("Ошибка токенизации")
        return

    filtered_tokens = remove_stop_words(tokens, stopwords)
    if filtered_tokens is None:
        print("Ошибка удаления стоп-слов")
        return

    freq_dict = calculate_frequencies(filtered_tokens)
    if freq_dict is None:
        print("Ошибка подсчета частот")
        return

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

    print("Профиль en корректен:", check_profile(en_profile))

    en_score = compare_profiles_by_top_n(unknown_profile, en_profile, 15)
    de_score = compare_profiles_by_top_n(unknown_profile, de_profile, 15)
    print("Доля пересечения с en:", en_score)
    print("Доля пересечения с de:", de_score)

    result = detect_language_by_top_n(unknown_profile, en_profile, de_profile, 15)

    assert result is not None, "Detection result is None"
    print("Определённый язык:", result)

    result_mse = detect_language_by_mse(unknown_profile, en_profile, de_profile)

    assert result_mse is not None, "Detection result by MSE is None"
    print("Определённый язык (MSE):", result_mse)

if __name__ == "__main__":
    main()
