"""
Language detection starter.
"""

# pylint: disable=unused-variable, duplicate-code
from lab_1_classify_profile.main import (
    collect_profiles,
    create_language_profile,
    detect_language_advanced,
    print_report,
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
    # result = None
    # assert result, "Detection result is None"

    # tokens = tokenize(de_text)
    # assert tokens is not None, "tokenize resulted as None"
    # tokens_without_stop_words = remove_stop_words(tokens, stopwords)
    # assert tokens_without_stop_words is not None, "tokens_without_stop_words resulted as None"
    # freq_dict = calculate_frequencies(tokens_without_stop_words)
    # assert freq_dict is not None, "freq_dict resulted as None"
    # top_words = get_top_n_words(freq_dict, 7)
    # assert top_words is not None, "get_top_n_words resulted as None"
    # print(top_words)

    en_profile = create_language_profile("en", en_text, stopwords)
    de_profile = create_language_profile("de", de_text, stopwords)
    unknown_profile = create_language_profile("unknown", unknown_text, stopwords)
    assert en_profile is not None, "English profile is None"
    assert de_profile is not None, "Deutsch profile is None"
    assert unknown_profile is not None, "Unknown profile is None"

    # result_by_top_n = detect_language_by_top_n(unknown_profile, en_profile, de_profile, 15)
    # assert result_by_top_n, "Detection by top n words is None"
    # print(result_by_top_n)

    # result_by_mse = detect_language_by_mse(unknown_profile, en_profile, de_profile)
    # assert result_by_mse, "Detection by mse is None"
    # print(result_by_mse)

    profiles_folder = "lab_1_classify_profile/assets/profiles"

    # with open("lab_1_classify_profile/assets/texts/es.txt", "r", encoding="utf-8") as file:
    #     es_text = file.read()
    # es_profile = create_language_profile("es", es_text, stopwords)
    # assert es_profile is not None, "Spanish profile is None"
    # assert save_profile(es_profile, profiles_folder), "Failed to save es profile"

    # assert save_profile(en_profile, profiles_folder), "Failed to save en profile"
    # assert save_profile(de_profile, profiles_folder), "Failed to save de profile"
    # assert save_profile(unknown_profile, profiles_folder), "Failed to save unknown profile"

    paths_to_profiles = [
    f"{profiles_folder}/en.json",
    f"{profiles_folder}/de.json",
    f"{profiles_folder}/la.json"
    ]
    known_profiles = collect_profiles(paths_to_profiles)
    assert known_profiles is not None, "collect_profiles returned None"

    metrics_stats= detect_language_advanced(unknown_profile, known_profiles, 15)
    assert metrics_stats is not None

    print_report(unknown_profile, metrics_stats, 15)

if __name__ == "__main__":
    main()
