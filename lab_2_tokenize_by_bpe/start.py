"""
BPE Tokenizer starter
"""

# pylint:disable=too-many-locals, unused-variable
from lab_2_tokenize_by_bpe.main import (
    calculate_bleu,
    collect_frequencies,
    decode,
    encode,
    get_vocabulary,
    load_vocabulary,
    train,
)


def main() -> None:
    """
    Launches an implementation
    """
    with open(
        "lab_2_tokenize_by_bpe/assets/text.txt", "r", encoding="utf-8"
        )as text_file:
        text = text_file.read()
    with open(
        "lab_2_tokenize_by_bpe/assets/secrets/secret_3.txt", "r", encoding="utf-8"
        ) as text_file:
        secret3_raw = text_file.read()
    with open(
        "lab_2_tokenize_by_bpe/assets/en_raw.txt", "r", encoding="utf-8"
        ) as text_file:
        text_reference_translation = text_file.read()
    with open(
        "lab_2_tokenize_by_bpe/assets/en_encoded.txt", "r", encoding="utf-8"
        ) as text_file:
        translation_encoded_raw = text_file.read()

<<<<<<< HEAD
    print('Mark 4: Word frequency dictionary.')
    freq_dict = collect_frequencies(text, None, '</s>')
    for i, (tokenized_word, freq) in enumerate(freq_dict.items()):
        if i < 5:
            print(f'{tokenized_word}: {freq}')

    print('Mark 6: Decoded text.')
    trained_freq = train(freq_dict, 10)

    if trained_freq is None:
        return

    vocabulary = get_vocabulary(trained_freq, '<unk>')
    encoded = [int(token_id) for token_id in translation_encoded_raw.replace(',', ' ').split()]
    result = decode(encoded, vocabulary, '</s>')
=======
    result = collect_frequencies(text, None, "</s>")

    assert result, "Frequency dictionary is None"
>>>>>>> bf876d9f25982c189f00f967f9e15b23da42abc8
    print(result)

    bpe_train = train(result, 100)
    if bpe_train is None:
        return
    print(bpe_train)

<<<<<<< HEAD
    print('Mark 8: Encoded texts.')
    load_vocab = load_vocabulary("lab_2_tokenize_by_bpe/assets/vocab.json")
    rus_encoded = encode(russian_text, load_vocab, '\u2581', None, '<unk>')
=======
    vocabulary = get_vocabulary(bpe_train,'<unk>')
    if vocabulary is None:
        return
>>>>>>> bf876d9f25982c189f00f967f9e15b23da42abc8

    # "secret"
    secret3 = [int(number) for number in secret3_raw.split()]
    secret = decode(secret3, vocabulary, '</s>')
    if secret is None:
        return
    print(secret)

<<<<<<< HEAD
    print('Mark 10: Comparison and BLEU')
    model_decoded = decode(encoded, load_vocab, None)
    model_decoded = model_decoded.replace('\u2581', ' ')
=======
    # "mark 8"
    with open("lab_2_tokenize_by_bpe/assets/ru_raw.txt", "r", encoding="utf-8") as text_file:
        ru_text = text_file.read()
>>>>>>> bf876d9f25982c189f00f967f9e15b23da42abc8

    ru_vocabulary = load_vocabulary("lab_2_tokenize_by_bpe/assets/vocab.json")
    if ru_vocabulary is None:
        return

    encoded_ru = encode(
        ru_text,
        ru_vocabulary,
        start_of_word_token="\u2581",
        end_of_word_token=None,
        unknown_token="<unk>",
    )
    if encoded_ru is None:
        return
    # "comparison"
    with open("lab_2_tokenize_by_bpe/assets/ru_encoded.txt", "r", encoding="utf-8") as encoded_file:
        ru_to_compare_raw = encoded_file.read()

    ru_to_compare = [int(number) for number in ru_to_compare_raw.split()]

    n = 20
    # print("Encoded: ", encoded_ru[:n])
    # print("To compare: ", ru_to_compare[:n])

    # "mark 10"
    translation_encoded = [int(number) for number in translation_encoded_raw.split()]

    en_vocabulary = load_vocabulary("lab_2_tokenize_by_bpe/assets/vocab.json")
    if en_vocabulary is None:
        return

    translation_decoded = decode(
        translation_encoded,
        en_vocabulary,
        None,
    )
    assert translation_decoded, "Decoded translation is None"

    translation_decoded = translation_decoded.replace("\u2581", " ")

    bleu = calculate_bleu(
        translation_decoded,
        text_reference_translation,
    )

    assert bleu, "BLEU is None"

    print("Predicted translation:", translation_decoded)
    print("Reference translation:", text_reference_translation)
    print("BLEU:", bleu)

if __name__ == "__main__":
    main()
