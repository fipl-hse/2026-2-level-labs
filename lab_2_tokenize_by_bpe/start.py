"""
BPE Tokenizer starter
"""

# pylint:disable=too-many-locals, unused-variable


from lab_2_tokenize_by_bpe.main import collect_frequencies, train


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
    assert result, "Translation not working"

word_frequencies = collect_frequencies(text, start_of_word=None, end_of_word="</s>")
assert word_frequencies is not None, "Word frequencies should be built successfully"

trained_tokens = train(word_frequencies, 100)
assert trained_tokens is not None, "BPE training should produce a vocabulary"

result = tuple(token for token in trained_tokens if len(token) > 1)
print(f"Total tokens after training: {len(trained_tokens)}")
print(f"Merged tokens found: {len(result)}")
print("First merged tokens:")
for token in result[:10]:
    print(token)
assert result, "Translation not working"


if __name__ == "__main__":
    main()
