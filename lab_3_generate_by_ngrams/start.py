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
    result = None

    text_processor = TextProcessor('_')
    encoded_text = text_processor.encode(text)
    if encoded_text is None:
        return

    result = text_processor.decode(encoded_text)
    if result is None:
        return

    print(
        f'Encoded text:\n{encoded_text[-100:]}gi\n\n'
        f'Decoded text:\n{result[-100:]}'
    )

    assert result


if __name__ == "__main__":
    main()