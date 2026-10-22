"""
BPE Tokenizer starter
"""

# pylint:disable=too-many-locals, unused-variable
import json

from lab_2_tokenize_by_bpe.main import (
    collect_frequencies,
    decode,
    encode,
    get_vocabulary,
    load_vocabulary,
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

    frequencies = collect_frequencies(text, None, '</s>')
    print(frequencies)

    trained = train(frequencies, 100)
    print(trained)
    if trained is None:
        return

    vocabulary = get_vocabulary(trained, "<unk>")
    print(vocabulary)

    with open("lab_2_tokenize_by_bpe/assets/vocab.json", "r", encoding="utf-8") as f:
        big_vocab = json.load(f)

    with open("lab_2_tokenize_by_bpe/assets/secrets/secret_1.txt", "r", encoding="utf-8") as f:
        ids = [int(x) for x in f.read().split()]

    decoded = decode(ids, big_vocab, None)
    decoded = decoded.replace('\u2581', ' ')
    print(decoded)

    vocab = load_vocabulary("lab_2_tokenize_by_bpe/assets/vocab.json")
    if vocab is None:
        return

    with open("lab_2_tokenize_by_bpe/assets/ru_raw.txt", "r", encoding="utf-8") as f:
        ru_text = f.read()

    encoded = encode(ru_text, vocab, '\u2581', None, '<unk>')
    if encoded is None:
        return

    print(encoded[:20])

    result = encoded
    assert result, "Translation not working"

    word = 'исследованиеисследование'
    enc = encode(word, vocab, '\u2581', None, '<unk>')
    rev_vocab = {v: k for k, v in big_vocab.items()}
    for token_id in enc:
        print(rev_vocab[token_id])

if __name__ == "__main__":
    main()
