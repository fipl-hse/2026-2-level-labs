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

    result = tokens
    assert result

if __name__ == "__main__":
    main()
