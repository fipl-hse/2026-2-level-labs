"""
BPE Tokenizer starter
"""

# pylint:disable=too-many-locals, unused-variable

from main import (
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

    word_frequencies = collect_frequencies(text, start_of_word=None, end_of_word="</s>")
    print("1. Частотный словарь слов")
    print(word_frequencies)

    if word_frequencies is not None:
        trained_frequencies = train(word_frequencies, num_merges=100)
        print("2. Словарь после 100 слияний")
        print(trained_frequencies)

        if trained_frequencies is not None:
            vocabulary = get_vocabulary(trained_frequencies, unknown_token="<unk>")

            if vocabulary is not None:
                with open("lab_2_tokenize_by_bpe/assets/secrets/secret_1.txt", "r", encoding="utf-8") as secret_file:
                    secret_content = secret_file.read().strip()
                    encoded_secret = [int(token_id) for token_id in secret_content.replace(",", " ").split() if token_id.isdigit()]

                    result = decode(encoded_secret, vocabulary, end_of_word_token = "</s>")
                    print("3. Декодированный текст секретного файла")
                    print(result)
    assert result, "Translation not working"


if __name__ == "__main__":
    main()
