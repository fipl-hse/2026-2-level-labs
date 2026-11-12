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
    print("File length:", len(text))
    print("First 80 chars:", repr(text[:80]))
    print("Slice [:200] length:", len(text[:200]))

    tp = TextProcessor('_')
    tokens = tp._tokenize(text[:200])
    print("Tokens count:", len(tokens) if tokens else 0)
    print("First 30 tokens:", tokens[:30] if tokens else None)

    encoded_text = tp.encode(text)
    assert encoded_text is not None

    decoded_text = tp.decode(encoded_text)
    assert decoded_text is not None

    print("Original text (first 100 chars):", text[:100])
    print("Encoded text (first 50 ids):", encoded_text[:50])
    print("Decoded text (first 100 chars):", decoded_text[:100])

    result = decoded_text
    assert result


if __name__ == "__main__":
    main()
