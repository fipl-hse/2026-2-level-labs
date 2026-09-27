"""
Language detection starter.
"""
from main import (
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

    print("Top 7 words:")
    for word in get_top_n_words(
        calculate_frequencies(remove_stop_words(tokenize(de_text), stopwords)), 7
    ):
            print(word)

    print()

    unk_lang_profile = create_language_profile("unk", unknown_text, stopwords)
    de_lang_profile = create_language_profile("de", de_text, stopwords)
    en_lang_profile = create_language_profile("en", en_text, stopwords)

    print("Language by top_n:",
    f"{detect_language_by_top_n(unk_lang_profile, de_lang_profile, en_lang_profile, 15)}")
    print("Language by MSE:",
    f"{detect_language_by_mse(unk_lang_profile, de_lang_profile, en_lang_profile)}")

    print()

    for profile in [de_lang_profile, en_lang_profile, unk_lang_profile]:
        save_profile(profile, "lab_1_classify_profile/assets/profiles/")

    paths_to_profiles = [
        f"lab_1_classify_profile/assets/profiles/{de_lang_profile[0]}.json",
        f"lab_1_classify_profile/assets/profiles/{en_lang_profile[0]}.json",
        f"lab_1_classify_profile/assets/profiles/{unk_lang_profile[0]}.json",
        "lab_1_classify_profile/assets/profiles/la.json"
    ]

    profiles_collected = collect_profiles(paths_to_profiles)

    unk_metrics = detect_language_advanced(
         unk_lang_profile,
         [profile for profile in profiles_collected if profile[0] != unk_lang_profile[0]],
         15
         )

    print_report(unk_lang_profile, unk_metrics, 15)
    result = unk_metrics
    assert result, "Detection result is None"


if __name__ == "__main__":
    main()
