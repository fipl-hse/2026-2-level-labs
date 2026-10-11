"""
BPE Tokenizer starter
"""

# pylint:disable=too-many-locals, unused-variable

from lab_2_tokenize_by_bpe.main import (
    collect_frequencies,
    count_tokens_pairs,
    merge_tokens,
    train,
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

    word_frequencies = collect_frequencies(text, start_of_word=None, end_of_word="</s>")

    token_pairs = count_tokens_pairs(word_frequencies) if word_frequencies else None

    merged_frequencies = None
    if token_pairs:
        # Находим самую частую пару для демонстрации merge_tokens
        best_pair = max(token_pairs.items(), key=lambda x: x[1])[0] if token_pairs else None
        if best_pair:
            merged_frequencies = merge_tokens(word_frequencies, best_pair)

    result = train(word_frequencies, num_merges=100)

    print("Trained frequencies sample:", list(result.items()[:3]) if result else None)
    assert result, "Translation not working"
    assert result, "Translation not working"


if __name__ == "__main__":
    main()
