"""
BPE Tokenizer starter
"""

# pylint:disable=too-many-locals, unused-variable

from lab_2_tokenize_by_bpe.main import collect_frequencies, prepare_word


def main() -> None:
    """
    Launches an implementation
    """
    with open("lab_2_tokenize_by_bpe/assets/text.txt", "r", encoding="utf-8") as text_file:
        text = text_file.read()
    with open("lab_2_tokenize_by_bpe/assets/en_raw.txt", "r", encoding="utf-8") as text_file:
        text_reference_translation = text_file.read()
    with open("lab_2_tokenize_by_bpe/assets/en_encoded.txt", "r", encoding="utf-8") as text_file:
        translation_encoded_raw = text_file.read()
    result = None

    assert prepare_word("It's", None, "</s>") == ("I", "t", "'", "s", "</s>")

    frequencies = collect_frequencies(text, None, "</s>")
    assert frequencies is not None, "collect_frequencies failed"
    assert frequencies, "Frequencies dictionary is empty"

    most_common = sorted(
        frequencies.items(), key=lambda item: item[1], reverse=True
    )[:10]
    for word, count in most_common:
        print("".join(word), "->", count)

    result = frequencies

    assert result, "Translation not working"


if __name__ == "__main__":
    main()
