"""
BPE Tokenizer starter
"""

# pylint:disable=too-many-locals, unused-variable
from lab_2_tokenize_by_bpe.main import collect_frequencies


def main() -> None:
    """
    Launches an implementation
    """
    with open("lab_2_tokenize_by_bpe/assets/text.txt", "r", encoding="utf-8") as text_file:
        text = text_file.read()

    result = collect_frequencies(text, None, "</s>")
    print(result)
    assert result, "Translation not working"


if __name__ == "__main__":
    main()
