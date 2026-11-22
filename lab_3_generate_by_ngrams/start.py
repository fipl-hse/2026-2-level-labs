"""
Generation by NGrams starter
"""

# pylint:disable=too-many-locals, unused-import, unused-variable
from pathlib import Path

from main import TextProcessor

def main() -> None:
    """
    Launches an implementation.

    In any case returns, None is returned
    """
    file_path = Path(__file__).parent / "assets" / "Harry_Potter.txt"
    with open(file_path, "r", encoding="utf-8") as text_file:
        text = text_file.read()
    result = None


    processor = TextProcessor("_")
    _result = processor.encode(text)
    print(_result)
    result = processor.decode(_result)
    print(result)
    assert result

if __name__ == "__main__":
    main()
