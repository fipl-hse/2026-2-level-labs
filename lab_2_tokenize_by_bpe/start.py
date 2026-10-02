"""
BPE Tokenizer starter
"""
import json
from main import(
    collect_frequencies,
    decode,
    get_vocabulary,
    train,
    )
# pylint:disable=too-many-locals, unused-variable


def main() -> None:
    """
    Launches an implementation
    """
    with open("lab_2_tokenize_by_bpe/assets/text.txt", "r", encoding="utf-8") as text_file:
        text = text_file.read()
    # with open("lab_2_tokenize_by_bpe/assets/en_raw.txt", "r", encoding="utf-8") as text_file:
    #     text_reference_translation = text_file.read()
    with open("lab_2_tokenize_by_bpe/assets/en_encoded.txt", "r", encoding="utf-8") as text_file:
        translation_encoded_raw = [int(x) for x in text_file.read().split()]
    with open("lab_2_tokenize_by_bpe/assets/secrets/secret_1.txt", "r", encoding="utf-8") as text_file:
        secret_text = [int(x) for x in text_file.read().split()]
    with open("lab_2_tokenize_by_bpe/assets/vocab.json", "r", encoding="utf-8") as text_file:
        tokens_vocab = json.load(text_file)

    freq_by_words = collect_frequencies(text, None, '/s')
    #print(freq_by_words)
    tokenized_words = train(freq_by_words, 100)
    result = decode(secret_text,tokens_vocab,"</s>")
    print(result)
    assert result, "Translation not working"


if __name__ == "__main__":
    main()
