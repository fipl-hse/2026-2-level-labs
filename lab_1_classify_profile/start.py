"""
Language detection starter.
"""

# pylint: disable=unused-variable, duplicate-code

from lab_1_classify_profile.main import create_language_profile, detect_language_by_mse


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
    de_prof = create_language_profile("de", de_text, stopwords)
    en_prof = create_language_profile("en", en_text, stopwords)
    unknown_prof = create_language_profile("en", unknown_text, stopwords)
    if de_prof is None or en_prof is None or unknown_prof is None:
        return
    result = detect_language_by_mse(
        unknown_prof, en_prof, de_prof)
    assert result, "Detection result is None"


if __name__ == "__main__":
    main()
