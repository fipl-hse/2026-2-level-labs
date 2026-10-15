"""
BPE Tokenizer starter
"""

from lab_2_tokenize_by_bpe.main import (
    collect_frequencies,
    decode,
    get_vocabulary,
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
    result = None
    word_frequences = collect_frequencies(text, None, '</s>')
    trained = train(word_frequences, 100)
    vocabulary = get_vocabulary(trained, '<unk>')
    with open("lab_2_tokenize_by_bpe/assets/secrets/secret_1.txt", "r", encoding="utf-8") as text_file:
            text_to_decode = text_file.read()
    encoded_text = []
    for i in text_to_decode.split():
        encoded_text.append(int(i))
    result = decode(encoded_text, vocabulary, '</s>')
    if result:
        result = result.replace('</s>', ' ')
    print(result)
    assert result, "Translation not working"


if __name__ == "__main__":
    main()

