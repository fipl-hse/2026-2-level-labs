"""
Language detection starter.
"""

# pylint: disable=unused-variable, duplicate-code

from lab_1_classify_profile.main import (
        create_language_profile,
        detect_language_by_mse,
        check_profile
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
    en_profile = create_language_profile("en", en_text, stopwords)
    de_profile = create_language_profile("de", de_text, stopwords)
    unknown_profile = create_language_profile("unknown", unknown_text, stopwords)
    if not check_profile(en_profile):
        return

    if not check_profile(de_profile):
        return

    if not check_profile(unknown_profile):
        return
    result = detect_language_by_mse(
        unknown_profile,
        en_profile,
        de_profile,
    )
    print(result)
    # assert result, "Detection result is None"


if __name__ == "__main__":
    main()
