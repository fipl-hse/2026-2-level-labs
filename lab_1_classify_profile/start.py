"""
Language detection starter.
"""
from main import (
    tokenize,
    create_language_profile,
    detect_language_by_top_n
)

# pylint: disable=unused-variable, duplicate-code


def main() -> None:
    """
    Launches an implementation.
    """
    with open("lab_1_classify_profile/assets/texts/de.txt", "r", encoding="utf-8") as file:
        de_text = file.read()
    tokens = tokenize(de_text)
    if tokens:
        print(tokens[:20])
    with open("lab_1_classify_profile/assets/texts/unknown.txt", "r", encoding="utf-8") as file:
        unknown_text = file.read()
    with open("lab_1_classify_profile/assets/stopwords.txt", "r", encoding="utf-8") as file:
        stopwords = file.read().split("\n")
    with open("lab_1_classify_profile/assets/texts/en.txt", "r", encoding="utf-8") as file:
        en_text = file.read()
    en_profile = create_language_profile("en", en_text, stopwords)
    de_profile = create_language_profile("de", de_text, stopwords)
    unknown_profile = create_language_profile("unknown", unknown_text, [])
    result = None
    if en_profile and de_profile and unknown_profile:
        result = detect_language_by_top_n(unknown_profile, en_profile, de_profile, 15)
        print(f"\nLanguage of the unknown text is: {result}")
    assert result, "Detection result is None"


if __name__ == "__main__":
    main()

