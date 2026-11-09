"""
BPE Tokenizer starter
"""

# pylint:disable=too-many-locals, unused-variable

from lab_2_tokenize_by_bpe.main import (
    collect_frequencies,
    count_tokens_pairs,
    decode,
    get_vocabulary,
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

    trained_frequencies = train(frequencies, 100)
assert trained_frequencies is not None, "train failed"

final_top = sorted(
    trained_frequencies.items(), key=lambda item: item[1], reverse=True
)[:10]
for word, count in final_top:
    print(" ".join(word), "->", count)

    vocabulary = get_vocabulary(trained_frequencies, "<unk>")
    assert vocabulary is not None, "get_vocabulary failed"
    assert vocabulary, "Vocabulary is empty"

    print(f"Vocabulary size: {len(vocabulary)}")
    top_tokens = sorted(vocabulary.items(), key=lambda item: item[1])[:20]
    for token, token_id in top_tokens:
        print(f"{token_id}: {token!r}")

    result = vocabulary

    import os

    secrets_dir = "lab_2_tokenize_by_bpe/assets/secrets"
    secret_files = sorted(os.listdir(secrets_dir)) if os.path.isdir(secrets_dir) else []
    assert secret_files, "No secret files found"

    secret_path = os.path.join(secrets_dir, secret_files[0])
    with open(secret_path, "r", encoding="utf-8") as secret_file:
        secret_raw = secret_file.read()

    cleaned = secret_raw.replace("[", " ").replace("]", " ").replace(",", " ")
    secret_ids = [int(x) for x in cleaned.split()]

    decoded_secret = decode(secret_ids, vocabulary, "</s>")
    assert decoded_secret is not None, "decode failed"
    print(f"Secret ({secret_files[0]}): {decoded_secret}")

    result = decoded_secret

    result = frequencies
    assert result, "Translation not working"


if __name__ == "__main__":
    main()