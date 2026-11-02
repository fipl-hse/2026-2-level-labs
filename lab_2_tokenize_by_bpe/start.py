"""
BPE Tokenizer starter
"""

# pylint:disable=too-many-locals, unused-variable
import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(current_dir)
sys.path.append(root_dir)

from lab_2_tokenize_by_bpe.main import (
    collect_frequencies,
)


def main() -> None:
    """
    Launches an implementation
    """
    base_dir = os.path.dirname(os.path.abspath(__file__))
    assets_dir = os.path.join(base_dir, "assets")

    with open(os.path.join(assets_dir, "text.txt"), "r", encoding="utf-8") as text_file:
        text = text_file.read()
    with open(os.path.join(assets_dir, "en_raw.txt"), "r", encoding="utf-8") as text_file:
        text_reference_translation = text_file.read()
    with open(os.path.join(assets_dir, "en_encoded.txt"), "r", encoding="utf-8") as text_file:
        translation_encoded_raw = text_file.read()



    frequency = collect_frequencies(text, start_of_word=None, end_of_word="</s>")
    print(frequency)

    assert frequency, "Translation not working"


if __name__ == "__main__":
    main()

 