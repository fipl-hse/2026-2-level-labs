"""
Generation by NGrams starter
"""

# pylint:disable=too-many-locals, unused-import, unused-variable

from main import TextProcessor


def main() -> None:
    """
    Launches an implementation.

    In any case returns, None is returned
    """
    with open(
        "./lab_3_generate_by_ngrams/assets/Harry_Potter.txt", "r", encoding="utf-8"
    ) as text_file:
        text = text_file.read()
    # result = None
    # assert result

    # Mark 4

    processing_text = TextProcessor(end_of_word_token = "_")
    encoded_text = processing_text.encode(text)
    print(encoded_text)
    decoded_text = processing_text.decode(encoded_text)
    print(decoded_text)

    # print(result)


if __name__ == "__main__":
    main()
