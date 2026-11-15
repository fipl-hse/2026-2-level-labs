"""
Generation by NGrams starter
"""

# pylint:disable=too-many-locals, unused-import, unused-variable

from lab_3_generate_by_ngrams.main import TextProcessor

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
    print("Encoded corpus (first 100 tokens):")
    print(encoded[:100] if encoded is not None else None)

    decoded = processor.decode(encoded) if encoded is not None else None
    print("\nDecoded text (first 300 chars):")
    print(decoded[:300] if decoded is not None else None)

    result = decoded
    assert result

if __name__ == "__main__":
    main()
