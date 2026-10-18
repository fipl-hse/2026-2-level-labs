"""
BPE Tokenizer starter
"""

# pylint:disable=too-many-locals, unused-variable
from main import (
    collect_frequencies,
    count_tokens_pairs,
    decode,
    encode,
    get_vocabulary,
    load_vocabulary,
    merge_tokens,
    prepare_word,
    tokenize_word,
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

    # Mark 4
    frequencies = collect_frequencies(text, None, "</s>")
    # print(frequencies)

    # Mark 6
    train_tokenizer = train(frequencies, 100)
    print(train_tokenizer)

    # Mark 6

    train_tokenizer = train(frequencies, 2000)
    vocabulary = get_vocabulary(train_tokenizer, "<unk>")

    if vocabulary is not None:
        with open("lab_2_tokenize_by_bpe/assets/secrets/secret_1.txt", "r", encoding="utf-8") as secret_file:
            secret_content = secret_file.read()

        encoded_secret = [int(num) for num in secret_content.split()]
        decoded_secret = decode(encoded_secret, vocabulary, "</s>")
        result6 = decoded_secret
        print("Секретное содержимое файла secret_1:", result6)

    # Mark 8

    vocabulary_path = "lab_2_tokenize_by_bpe/assets/vocab.json"
    reference_vocabulary = load_vocabulary(vocabulary_path)

    if reference_vocabulary is not None:
        print(f"\nСловарь успешно загружен, кол-во токенов: {len(reference_vocabulary)}")


        with open("lab_2_tokenize_by_bpe/assets/ru_raw.txt", "r", encoding="utf-8") as file:
            ru_text = file.read()

        encoded_ru_text = encode(ru_text, reference_vocabulary, "\u2581", None, "<unk>")

        if encoded_ru_text is not None:
            print("Текст успешно закодирован")
            print("Первые 20 токенов:", encoded_ru_text[:20])
            result = encoded_ru_text
        else:
            print("Ошибка в encode")
    else:
        print("Не удалось загрузить словарь")

    assert result, "Translation not working"



if __name__ == "__main__":
    main()
