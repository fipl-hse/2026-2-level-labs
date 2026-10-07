"""
BPE Tokenizer starter
"""


# pylint:disable=too-many-locals, unused-variable
from lab_2_tokenize_by_bpe.main import (
    collect_frequencies,
    encode,
    get_vocabulary,
    load_vocabulary,
    train,
)


def main() -> None:
    """
    Launches an implementation
    """
    result = None

    with open("lab_2_tokenize_by_bpe/assets/text.txt", "r", encoding="utf-8") as text_file:
        text = text_file.read()

    word_frequencies = collect_frequencies(text, start_of_word=None, end_of_word="</s>")
    if word_frequencies is None:
        print("Error: Failed to collect word frequencies.")

    if word_frequencies is not None:
        trained = train(word_frequencies, num_merges=100)
        if trained is None:
            print("Error: Failed to train tokenizer.")
        else:
            vocabulary = get_vocabulary(trained, unknown_token="<unk>")
            if vocabulary is None:
                print("Error: Failed to build vocabulary.")

    model_vocab = load_vocabulary("lab_2_tokenize_by_bpe/assets/vocab.json")
    if model_vocab is None:
        print("Error: Failed to load vocabulary.")

    if model_vocab is not None:
        with open("lab_2_tokenize_by_bpe/assets/ru_raw.txt", "r", encoding="utf-8") as ru_file:
            ru_text = ru_file.read()
        encoded_ru = encode(ru_text, model_vocab, "\u2581", None, "<unk>")
        if encoded_ru is None:
            print("Error: Failed to encode Russian text.")
        else:
            result = encoded_ru

    assert result, "Translation not working"


if __name__ == "__main__":
    main()
