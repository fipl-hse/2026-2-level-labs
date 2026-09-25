"""
Language detection starter.
"""

# pylint: disable=unused-variable, duplicate-code

from lab_1_classify_profile.main import (
    calculate_frequencies,
    compare_profiles_by_mse,
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
    with open("lab_1_classify_profile/assets/texts/de.txt", "r", encoding="utf-8") as file:
        de_text = file.read()
    with open("lab_1_classify_profile/assets/texts/unknown.txt", "r", encoding="utf-8") as file:
        unknown_text = file.read()
    with open("lab_1_classify_profile/assets/stopwords.txt", "r", encoding="utf-8") as file:
        stopwords = file.read().split("\n")
    with open("lab_1_classify_profile/assets/texts/en.txt", "r", encoding="utf-8") as file:
        en_text = file.read()
    result = None


    de_tokens = tokenize(de_text)
    if de_tokens is None:
        raise TypeError("Tokenization failed for de text")

    de_tokens = remove_stop_words(de_tokens, stopwords)
    if de_tokens is None:
        raise TypeError("Stop-word removal failed for de text")

    de_frequencies = calculate_frequencies(de_tokens)
    if de_frequencies is None:
        raise TypeError("Frequency calculation failed for de text")

    top_7_words = get_top_n_words(de_frequencies, 7)
    if top_7_words is None:
        raise TypeError("Top words extraction failed for de text")

    print(top_7_words)

    en_profile = create_language_profile("en", en_text, stopwords)
    if en_profile is None:
        raise TypeError("English profile creation failed")

    de_profile = create_language_profile("de", de_text, stopwords)
    if de_profile is None:
        raise TypeError("German profile creation failed")

    unknown_profile = create_language_profile("unknown", unknown_text, stopwords)
    if unknown_profile is None:
        raise TypeError("Unknown profile creation failed")

    result = detect_language_by_top_n(
        unknown_profile,
        en_profile,
        de_profile,
        15,
    )
    if result is None:
        raise TypeError("Top-n language detection failed")

    mse_to_en = compare_profiles_by_mse(unknown_profile, en_profile)
    mse_to_de = compare_profiles_by_mse(unknown_profile, de_profile)
    result_by_mse = detect_language_by_mse(unknown_profile, en_profile, de_profile)
    if result_by_mse is None:
        raise TypeError("MSE language detection failed")

    print("Top-n result:", result)
    print("MSE to en:", mse_to_en)
    print("MSE to de:", mse_to_de)
    print("MSE result:", result_by_mse)

    assert result, "Detection result is None"
    assert result_by_mse, "MSE detection result is None"


if __name__ == "__main__":
    main()
