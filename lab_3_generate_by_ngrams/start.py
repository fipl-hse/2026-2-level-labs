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

    text_processor = TextProcessor("_")

    encoded_corpus = text_processor.encode(text)
    assert encoded_corpus is not None, "The text could not be encoded"

    decoded_text = text_processor.decode(encoded_corpus)
    assert decoded_text is not None, "The text could not be decoded"

    result = decoded_text
    assert result

if __name__ == "__main__":
    main()
