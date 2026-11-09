"""
BPE Tokenizer starter
"""

# pylint:disable=too-many-locals, unused-variable

from lab_2_tokenize_by_bpe.main import (
    collect_frequencies,
    count_tokens_pairs,
    merge_tokens,
    prepare_word,
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

    assert prepare_word("It's", None, "</s>") == ("I", "t", "'", "s", "</s>")

    frequencies = collect_frequencies(text, None, "</s>")
    assert frequencies is not None, "collect_frequencies failed"
    assert frequencies, "Frequencies dictionary is empty"

    most_common = sorted(
        frequencies.items(), key=lambda item: item[1], reverse=True
    )[:10]
    for word, count in most_common:
        print("".join(word), "->", count)

    pairs = count_tokens_pairs(frequencies)
    assert pairs is not None, "count_tokens_pairs failed"
    assert pairs, "Pairs dictionary is empty"

    top_pairs = sorted(
        pairs.items(), key=lambda item: item[1], reverse=True
    )[:10]
    for pair, count in top_pairs:
        print(pair, "->", count)

    if pairs:
        top_pair = max(pairs.items(), key=lambda item: item[1])[0]
        merged_frequencies = merge_tokens(frequencies, top_pair)
        assert merged_frequencies is not None, "merge_tokens failed"

        for word in merged_frequencies:
            for token in word:
                assert token != "", "empty token found"

        merged_top = sorted(
            merged_frequencies.items(), key=lambda item: item[1], reverse=True
        )[:10]
        for word, count in merged_top:
            print("".join(word), "->", count)

    training_result = train(frequencies, 100)
    assert training_result is not None, "train failed"
    trained_frequencies, merges = training_result

    print(f"Performed {len(merges)} merges (target: 100)")

    for pair in merges[-20:]:
        print(f"merged {pair} -> {pair[0] + pair[1]}")

    final_top = sorted(
        trained_frequencies.items(), key=lambda item: item[1], reverse=True
    )[:10]
    for word, count in final_top:
        print(" ".join(word), "->", count)

    result = frequencies
    assert result, "Translation not working"


if __name__ == "__main__":
    main()