"""
Generation by NGrams starter
"""
from lab_3_generate_by_ngrams.main import TextProcessor
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

    result = decoded
    assert result


if __name__ == "__main__":
    main()
