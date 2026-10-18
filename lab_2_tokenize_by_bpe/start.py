"""
BPE Tokenizer starter
"""

# pylint:disable=too-many-locals, unused-variable

import os

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
    assets = "lab_2_tokenize_by_bpe/assets"

    with open(os.path.join(assets, "text.txt"), "r", encoding="utf-8") as text_file:
        text = text_file.read()

    word_frequencies = collect_frequencies(text, start_of_word=None, end_of_word="</s>")
    assert word_frequencies is not None, "Ошибка: частотный словарь"
    print(f"Частотный словарь собран: {len(word_frequencies)} уникальных слов")

    trained = train(word_frequencies, num_merges=100)
    assert trained is not None, "Ошибка: обучение токенизатора"
    print(f"Токенизатор обучен: {len(trained)} уникальных слов после слияний")
    vocabulary = get_vocabulary(trained, unknown_token="<unk>")
    assert vocabulary is not None, "Ошибка: построение словаря"
    print(f"Размер словаря: {len(vocabulary)} токенов")

    secrets_dir = os.path.join(assets, "secrets")
    secret_files = os.listdir(secrets_dir) if os.path.exists(secrets_dir) else []
    if secret_files:
        secret_path = os.path.join(secrets_dir, secret_files[0])
        with open(secret_path, "r", encoding="utf-8") as secret_file:
            content = secret_file.read().strip().replace("[", "").replace("]", "")
        secret_encoded = [int(x) for x in content.replace(",", " ").split()]
        secret_decoded = decode(secret_encoded, vocabulary, end_of_word_token="</s>")
        print(f"Секретное сообщение: {secret_decoded}")

    model_vocab = load_vocabulary(os.path.join(assets, "vocab.json"))
    assert model_vocab is not None, "Ошибка: загрузка vocab.json"
    print(f"Загружен словарь модели: {len(model_vocab)} токенов")

    with open(os.path.join(assets, "ru_raw.txt"), "r", encoding="utf-8") as ru_file:
        ru_text = ru_file.read()
    encoded_ru = encode(ru_text, model_vocab, "\u2581", None, "<unk>")
    assert encoded_ru is not None, "Ошибка: кодирование текста"
    print(f"Русский текст закодирован: {len(encoded_ru)} идентификаторов")

    ru_encoded_path = os.path.join(assets, "ru_encoded.txt")
    if os.path.exists(ru_encoded_path):
        with open(ru_encoded_path, "r", encoding="utf-8") as ru_enc_file:
            ru_enc_content = ru_enc_file.read().strip().replace("[", "").replace("]", "")
        ru_encoded = [int(x) for x in ru_enc_content.replace(",", " ").split()]
        status = "совпадает" if encoded_ru == ru_encoded else "НЕ совпадает"
        print(f"Кодирование {status} с эталоном ru_encoded.txt")

    with open(os.path.join(assets, "en_encoded.txt"), "r", encoding="utf-8") as en_enc_file:
        en_content = en_enc_file.read().strip().replace("[", "").replace("]", "")
    en_encoded = [int(x) for x in en_content.replace(",", " ").split()]
    en_decoded = decode(en_encoded, model_vocab, end_of_word_token=None)
    assert en_decoded is not None, "Ошибка: декодирование предсказаний"
    en_decoded_clean = en_decoded.replace("\u2581", " ").strip()

    with open(os.path.join(assets, "en_raw.txt"), "r", encoding="utf-8") as en_raw_file:
        en_raw = en_raw_file.read()
    bleu_score = calculate_bleu(en_decoded_clean, en_raw, max_order=3)
    assert bleu_score is not None, "Ошибка: вычисление BLEU"
    print(f"BLEU score: {bleu_score:.2f}")

    assert encoded_ru, "Translation not working"


if __name__ == "__main__":
    main()
