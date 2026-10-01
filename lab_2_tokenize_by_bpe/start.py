"""
BPE Tokenizer starter
"""

# pylint:disable=too-many-locals, unused-variable
from lab_2_tokenize_by_bpe.main import (
    collect_frequencies,
    train,
    get_vocabulary,
)


def main() -> None:
    """
    Launches an implementation
    """
    with open("lab_2_tokenize_by_bpe/assets/text.txt", "r", encoding="utf-8") as text_file:
        text = text_file.read()

    word_frequencies = collect_frequencies(text, start_of_word=None, end_of_word="</s>")
    if word_frequencies is None:
        print("Error: Failed to collect word frequencies.")
        return
    trained_frequencies = train(word_frequencies, num_merges=100)
    if trained_frequencies is None:
        print("Error: Failed to train tokenizer.")
        return
    print("Trained word frequencies (first 10):")
    for i, (word, freq) in enumerate(trained_frequencies.items()):
        if i >= 10:
            break
        print(f"  {word}: {freq}")
    vocabulary = get_vocabulary(trained_frequencies, unknown_token="<unk>")
    if vocabulary is None:
        print("Error: Failed to build vocabulary.")
        return
    print("\nVocabulary (first 20):")
    for i, (token, identifier) in enumerate(vocabulary.items()):
        if i >= 20:
            break
        print(f"  {repr(token)}: {identifier}")

    result = None
    assert result, "Translation not working"


if __name__ == "__main__":
    main()
