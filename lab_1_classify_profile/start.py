"""
Language detection starter.
"""

# pylint: disable=unused-variable, duplicate-code
from main import(tokenize, remove_stop_words, calculate_frequencies, get_top_n_words)

def main() -> None:
    """
    Launches an implementation.
    """
    with open(r"C:\Users\HomePC\Desktop\popa_muroja\2026-2-level-labs\lab_1_classify_profile\assets\texts\de.txt", "r", encoding="utf-8") as file:
        de_text = file.read()
    with open(r"C:\Users\HomePC\Desktop\popa_muroja\2026-2-level-labs\lab_1_classify_profile\assets\texts\de.txt", "r", encoding="utf-8") as file:
        unknown_text = file.read()
    with open(r"C:\Users\HomePC\Desktop\popa_muroja\2026-2-level-labs\lab_1_classify_profile\assets\texts\de.txt", "r", encoding="utf-8") as file:
        stopwords = file.read().split("\n")
    with open(r"C:\Users\HomePC\Desktop\popa_muroja\2026-2-level-labs\lab_1_classify_profile\assets\texts\de.txt", "r", encoding="utf-8") as file:
        en_text = file.read()
    tokens = tokenize(de_text)
    clean = remove_stop_words(tokens, stopwords)
    result = calculate_frequencies(clean)
    print(get_top_n_words(result, 7))
    assert result, "Detection result is None"


if __name__ == "__main__":
    main()
