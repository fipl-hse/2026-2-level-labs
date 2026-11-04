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
    intermediate_result = processor.encode(text)
    result = processor.decode(intermediate_result)
    assert result
    print(result)


if __name__ == "__main__":
    main()
