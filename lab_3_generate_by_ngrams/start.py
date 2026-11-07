"""
Generation by NGrams starter
"""
from lab_3_generate_by_ngrams.main import TextProcessor, WordProcessor
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

    result = None
    assert result

processor = TextProcessor('_')

encoded_text = processor.encode(text[:30])
assert decoded_text is not None
print(f"Decoded text: {decoded_text}")

decoded_text = processor.decode(encoded_text)
assert decoded_text is not None
print(f"Decoded text: {decoded_text}")

processor = WordProcessor('</s>')

encoded_text = processor.encode(text[:100])
assert encoded_text is not None
print(f"Encoded text: {encoded_text}")

decoded_text = processor.decode(encoded_text)
assert decoded_text is not None
print(f"Decoced text: {decoded_text}")


if __name__ == "__main__":
    main()
