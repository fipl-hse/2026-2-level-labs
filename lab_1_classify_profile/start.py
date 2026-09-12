"""
Language detection starter.
"""

# pylint: disable=unused-variable, duplicate-code
from main import tokenize

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
    assert result, "Detection result is None"

    cleaned_de_text = tokenize(de_text)
    cleaned_unknown_text = tokenize(unknown_text)
    cleaned_en_text = tokenize(en_text)

if __name__ == "__main__":
    main()
