"""
BPE Tokenizer starter
"""

# pylint:disable=too-many-locals, unused-variable
from lab_2_tokenize_by_bpe.main import (
    collect_frequencies,
    decode,
    get_vocabulary,
    train
)


def main() -> None:
    """
    Launches an implementation
    """
    with open("lab_2_tokenize_by_bpe/assets/text.txt", "r", encoding="utf-8") as text_file:
        text = text_file.read()
    with open("lab_2_tokenize_by_bpe/assets/secrets/secret_4.txt", "r", encoding="utf-8") as text_file:
        secret_text = text_file.read()
    # with open("lab_2_tokenize_by_bpe/assets/en_raw.txt", "r", encoding="utf-8") as text_file:
    #     text_reference_translation = text_file.read()
    with open("lab_2_tokenize_by_bpe/assets/en_encoded.txt", "r", encoding="utf-8") as text_file:
        translation_encoded_raw = text_file.read()
    result = collect_frequencies(text, None, "</s>")
    assert result, "Translation not working"
    new_word_frequencies = train(result, 100)
    vocabulary = get_vocabulary(new_word_frequencies, "<unk>")
    revealed_secret = decode(
        [int(num) for num in secret_text.split()],
        vocabulary,
        "</s>"
    )
    print(revealed_secret)


if __name__ == "__main__":
    main()
