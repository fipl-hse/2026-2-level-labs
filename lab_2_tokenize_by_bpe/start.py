"""
BPE Tokenizer starter
"""

# pylint:disable=too-many-locals, unused-variable
from main import (
    collect_frequencies,
    count_tokens_pairs,
    merge_tokens,
    prepare_word,
    train,
)

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
    # result = None
    # assert result, "Translation not working"

    # Mark 4
    frequencies = collect_frequencies(text, None, "</s>")
    # print(frequencies)

    # Mark 6
    train_tokenizer = train(frequencies, 100)
    print(train_tokenizer)

if __name__ == "__main__":
    main()
