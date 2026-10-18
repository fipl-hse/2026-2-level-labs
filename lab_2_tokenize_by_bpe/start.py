"""
BPE Tokenizer starter
"""
import os

# pylint:disable=too-many-locals, unused-variable
from lab_2_tokenize_by_bpe.main import (
    calculate_bleu,
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
    result = None

    with open("lab_2_tokenize_by_bpe/assets/text.txt", "r", encoding="utf-8") as text_file:
        text = text_file.read()

    word_frequencies = collect_frequencies(text, start_of_word=None, end_of_word="</s>")
    if word_frequencies is None:
        print("Ошибка: не удалось собрать частотный словарь")
        return
    print(f"Частотный словарь собран: {len(word_frequencies)} уникальных слов")

    trained = train(word_frequencies, num_merges=100)
    if trained is None:
        print("Ошибка: не удалось обучить токенизатор")
        return
    print(f"Токенизатор обучен: {len(trained)} уникальных слов после слияний")

    vocabulary = get_vocabulary(trained, unknown_token="<unk>")
    if vocabulary is None:
        print("Ошибка: не удалось построить словарь токенов")
        return
    print(f"Размер словаря: {len(vocabulary)} токенов")

    secrets_dir = "lab_2_tokenize_by_bpe/assets/secrets"
    if os.path.exists(secrets_dir):
        secret_files = os.listdir(secrets_dir)
        if secret_files:
            secret_path = os.path.join(secrets_dir, secret_files[0])
            with open(secret_path, "r", encoding="utf-8") as f:
                content = f.read().strip().replace("[", "").replace("]", "")
                secret_encoded = [int(x) for x in content.replace(",", " ").split()]

            secret_decoded = decode(secret_encoded, vocabulary, end_of_word_token="</s>")
            if secret_decoded is not None:
                print(f"Секретное сообщение: {secret_decoded}")
            else:
                print("Ошибка: не удалось декодировать секретный файл")

    model_vocab = load_vocabulary("lab_2_tokenize_by_bpe/assets/vocab.json")
    if model_vocab is None:
        print("Ошибка: не удалось загрузить словарь vocab.json")
        return
    print(f"Загружен словарь модели: {len(model_vocab)} токенов")

    with open("lab_2_tokenize_by_bpe/assets/ru_raw.txt", "r", encoding="utf-8") as ru_file:
        ru_text = ru_file.read()

    encoded_ru = encode(ru_text, model_vocab, "\u2581", None, "<unk>")
    if encoded_ru is None:
        print("Ошибка: не удалось закодировать текст")
        return
    result = encoded_ru
    print(f"Русский текст закодирован: {len(encoded_ru)} идентификаторов")

    try:
        with open("lab_2_tokenize_by_bpe/assets/ru_encoded.txt", "r", encoding="utf-8") as ru_enc_file:
            ru_enc_content = ru_enc_file.read().strip().replace("[", "").replace("]", "")
            ru_encoded = [int(x) for x in ru_enc_content.replace(",", " ").split()]
        if encoded_ru == ru_encoded:
            print("Кодирование совпадает с эталоном ru_encoded.txt")
        else:
            print("Кодирование НЕ совпадает с эталоном ru_encoded.txt")
    except FileNotFoundError:
        print("ru_encoded.txt не найден, сравнение пропущено")

    with open("lab_2_tokenize_by_bpe/assets/en_encoded.txt", "r", encoding="utf-8") as en_enc_file:
        en_content = en_enc_file.read().strip().replace("[", "").replace("]", "")
        en_encoded = [int(x) for x in en_content.replace(",", " ").split()]

    en_decoded = decode(en_encoded, model_vocab, end_of_word_token=None)
    if en_decoded is None:
        print("Ошибка: не удалось декодировать предсказания модели")
        return

    en_decoded_clean = en_decoded.replace("\u2581", " ").strip()

    with open("lab_2_tokenize_by_bpe/assets/en_raw.txt", "r", encoding="utf-8") as en_raw_file:
        en_raw = en_raw_file.read()

    bleu_score = calculate_bleu(en_decoded_clean, en_raw, max_order=3)
    if bleu_score is not None:
        print(f"BLEU score: {bleu_score:.2f}")
    else:
        print("Ошибка: не удалось вычислить BLEU")

    assert result, "Translation not working"


if __name__ == "__main__":
    main()
