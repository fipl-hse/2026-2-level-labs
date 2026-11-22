"""
Generation by NGrams starter
"""


from pathlib import Path

from main import TextProcessor

# pylint:disable=too-many-locals, unused-import, unused-variable








def main() -> None:
    """
    Launches an implementation.

    In any case returns, None is returned
    """
    file_path = Path(__file__).parent / "assets" / "Harry_Potter.txt"
    with open(file_path, "r", encoding="utf-8") as text_file:
        text = text_file.read()
    resault = None

    processor = TextProcessor("_")
    _result = processor.encode(text)
    if _result is not None:
        result = processor.decode(_result)
    else:
        result = None
    print(result)
    assert result

if __name__ == "__main__":
    main()
