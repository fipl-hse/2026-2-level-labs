"""
Generation by NGrams starter
"""

from lab_3_generate_by_ngrams.main import NGramLanguageModel, TextProcessor

# pylint:disable=too-many-locals, unused-import, unused-variable


def main() -> None:
    """
    Launches an implementation.

    In any case returns, None is returned
    """
    with open(
        "./lab_3_generate_by_ngrams/assets/Harry_Potter.txt", "r", encoding="utf-8"
    ) as text_file:
        text = text_file.read()

    processor = TextProcessor("_")

    encoded = processor.encode(text)
    if encoded is None:
        print("Ошибка кодирования")
        return

    print(f"Длина закодированного корпуса: {len(encoded)}")
    print(f"Первые 100 токенов: {encoded[:100]}")
    print(f"Размер хранилища: {len(processor._storage)}")

    decoded = processor.decode(encoded)
    if decoded is None:
        print("Ошибка декодирования")
        return

    print(f"Длина декодированного текста: {len(decoded)}")
    print(f"Первые 500 символов:\n{decoded[:500]}")

    n_gram_size = 2
    model = NGramLanguageModel(encoded, n_gram_size)

    if not model.build():
        print("Ошибка построения модели")
        return

    print(f"Модель успешно построена для {n_gram_size}-грамм.")
    print(f"Количество уникальных {n_gram_size}-грамм в модели: {len(model._n_gram_frequencies)}")

    print("\nПримеры n-грамм и их вероятностей:")
    count = 0
    for ngram, prob in model._n_gram_frequencies.items():
        letters = tuple(processor.get_token(token_id) for token_id in ngram)
        print(f"  {ngram} (буквы: {letters}) -> {prob:.4f}")
        count += 1
        if count >= 5:
            break

    sequence = tuple(encoded[:n_gram_size])
    print(f"\nПредсказание для контекста {sequence}:")

    next_tokens = model.generate_next_token(sequence)
    if next_tokens is None:
        print("Не удалось получить следующий токен")
    else:
        print(f"Возможные следующие токены (id: вероятность): {next_tokens}")
        for token_id, prob in next_tokens.items():
            token_letter = processor.get_token(token_id)
            print(f"  Токен {token_id} ('{token_letter}') с вероятностью {prob:.4f}")

    result = decoded
    assert result


if __name__ == "__main__":
    main()
