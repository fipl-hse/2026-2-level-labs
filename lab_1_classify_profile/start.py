"""
Language detection starter.
"""

# pylint: disable=unused-variable, duplicate-code

from lab_1_classify_profile.main import (
    calculate_frequencies,
    collect_profiles,
    create_language_profile,
    detect_language_advanced,
    detect_language_by_mse,
    detect_language_by_top_n,
    get_top_n_words,
    print_report,
    remove_stop_words,
    save_profile,
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

    tokens_de = tokenize(de_text)
    assert tokens_de is not None

    tokens_de_clean = remove_stop_words(tokens_de, stopwords)
    assert tokens_de_clean is not None

    freq_de = calculate_frequencies(tokens_de_clean)
    assert freq_de is not None

    top_7_de = get_top_n_words(freq_de, 7)
    assert top_7_de is not None
    print("Top-7 DE:", top_7_de)

    en_profile = create_language_profile("en", en_text, stopwords)
    de_profile = create_language_profile("de", de_text, stopwords)
    unknown_profile = create_language_profile("unknown", unknown_text, stopwords)
    assert en_profile is not None
    assert de_profile is not None
    assert unknown_profile is not None

    print(
        "Detected by Top-N:",
        detect_language_by_top_n(unknown_profile, en_profile, de_profile, 15),
    )

    result_mse = detect_language_by_mse(unknown_profile, en_profile, de_profile)
    print("Detected by MSE:", result_mse)

    save_profile(en_profile, "lab_1_classify_profile/assets/profiles")
    save_profile(de_profile, "lab_1_classify_profile/assets/profiles")

    profiles = collect_profiles(
        [
            "lab_1_classify_profile/assets/profiles/en.json",
            "lab_1_classify_profile/assets/profiles/de.json",
            "lab_1_classify_profile/assets/profiles/la.json",
        ]
    )
    assert profiles is not None

    results = detect_language_advanced(unknown_profile, profiles, 15)
    assert results is not None
    print_report(unknown_profile, results, 15)

    assert result_mse, "Detection result is None"


if __name__ == "__main__":
    main()
