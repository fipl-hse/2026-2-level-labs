"""
BPE Tokenizer starter
"""

# pylint:disable=too-many-locals, unused-variable

from main import (
    collect_frequencies,
    train,
    get_vocabulary,
    decode,
    load_vocabulary,
    encode,
)

def _read_text(path: str) -> str:
    with open(path, "r", encoding="utf-8") as file:
        return file.read()

def main() -> None:
    """
    Launches an implementation
    """

    base = "lab_2_tokenize_by_bpe/assets"

    text = _read_text(f"{base}/text.txt")
    word_frequencies = collect_frequencies(
        text, start_of_word=None, end_of_word="</s>"
    )

    with open("lab_2_tokenize_by_bpe/assets/text.txt", "r", encoding="utf-8") as text_file:
        text = text_file.read()
    with open("lab_2_tokenize_by_bpe/assets/en_raw.txt", "r", encoding="utf-8") as text_file:
        text_reference_translation = text_file.read()
    with open("lab_2_tokenize_by_bpe/assets/en_encoded.txt", "r", encoding="utf-8") as text_file:
        translation_encoded_raw = text_file.read()

    print("== Шаг 2. Частотный словарь (первые 5 записей) ===")
    for index, (word, freq) in enumerate(word_frequencies.items()):
        if index >= 5:
            break
        print(f" {word}: {freq}")
    print(f" ... всего уникальных слов: {len(word_frequencies)}")

    result = None
    assert result, "Translation not working"


if __name__ == "__main__":
    main()
