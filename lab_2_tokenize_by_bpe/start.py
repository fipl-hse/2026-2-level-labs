"""
BPE Tokenizer starter
"""

# pylint:disable=too-many-locals, unused-variable
from main import collect_frequencies, decode, get_vocabulary, train


def main() -> None:
    """
    Launches an implementation
    """
    with open("lab_2_tokenize_by_bpe/assets/text.txt", "r", encoding="utf-8") as text_file:
        text = text_file.read()
    with open("lab_2_tokenize_by_bpe/assets/en_raw.txt", "r", encoding="utf-8") as text_file:
        text_reference_translation = text_file.read()
    with open(
        "lab_2_tokenize_by_bpe/assets/en_encoded.txt",
        "r",
        encoding="utf-8"
    ) as text_file:
        translation_encoded_raw = [
            int(token) for token in text_file.read().split()
        ]
    freqs = collect_frequencies(en_raw, None, "</s>")
    if freqs is None:
        return
    tokenizer = train(freqs, 100)
    if tokenizer is None:
        return
    vocab = get_vocabulary(tokenizer, "<unk>")
    if vocab is None:
        return
    decoded_text = decode(translation_encoded_raw, vocab, "</s>")
    if decoded_text is None:
        return
    print(decoded_text)
    result = decoded_text
    assert result, "Translation not working"


if __name__ == "__main__":
    main()
