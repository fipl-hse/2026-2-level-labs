"""
Language detection starter.
"""


from lab_1_classify_profile.main import (
    create_language_profile, detect_language_by_mse)


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

    profile_de = create_language_profile("de", de_text, stopwords)
    profile_en = create_language_profile("en", en_text, stopwords)
    unknown_profile = create_language_profile("en", unknown_text, stopwords)

    if profile_de is None or profile_en is None or unknown_profile is None:
        return

    result = detect_language_by_mse(
        unknown_profile, profile_en, profile_de)
    assert result, "Detection result is None"


if __name__ == "__main__":
    main()
