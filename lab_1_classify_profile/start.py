"""
Language detection starter.
"""


# pylint: disable=unused-variable, duplicate-code


from lab_1_classify_profile.main import (
    check_profile,
    create_language_profile,
    detect_language_by_mse,
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


    unknown_profile = create_language_profile('unknown', unknown_text, stopwords)
    de_profile = create_language_profile('de', de_text, stopwords)
    en_profile = create_language_profile('en', en_text, stopwords)

    assert unknown_profile is not None, 'Error: Unknown profile is None'
    assert de_profile is not None, 'Error: De profile is None'
    assert en_profile is not None, 'Error: En profile is None'

    assert check_profile(unknown_profile), 'Error: Unknown profile invalid'
    assert check_profile(de_profile), 'Error: De profile invalid'
    assert check_profile(en_profile), 'Error: En profile invalid'

    detected_lang = detect_language_by_mse(unknown_profile, de_profile, en_profile)

    print(f'Detected language: {detected_lang}')


    result = detected_lang
    assert result, 'Detection result is None'


if __name__ == "__main__":
    main()
