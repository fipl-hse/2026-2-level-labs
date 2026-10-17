"""
BPE Tokenizer starter
"""

# pylint:disable=too-many-locals, unused-variable
from lab_2_tokenize_by_bpe.main import (
    collect_frequencies,
    count_tokens_pairs,
    train
)

def main() -> None:
    """
    Launches an implementation
    """
    with open("lab_2_tokenize_by_bpe/assets/text.txt", "r", encoding="utf-8") as text_file:
        text = text_file.read()
    with open("lab_2_tokenize_by_bpe/assets/en_raw.txt", "r", encoding="utf-8") as text_file:
        text_reference_translation = text_file.read()
    with open("lab_2_tokenize_by_bpe/assets/en_encoded.txt", "r", encoding="utf-8") as text_file:
        translation_encoded_raw = text_file.read()

    result = None

    word_frequencies = collect_frequencies(text, None, "</s>")
    if word_frequencies is None:
        return None

    result = word_frequencies

    assert result, "Collect frequencies result is None"

    pairs = count_tokens_pairs(word_frequencies)
    if pairs is None:
        return None

    trained = train(word_frequencies, 100)
    if trained is None:
        return None
    print(f"unique words(step 5: {len(trained)}")

    result = trained
    assert result, "Training result is None"
    return None




if __name__ == "__main__":
    main()
