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
    with open("lab_2_tokenize_by_bpe/assets/text.txt", "r", encoding="utf-8") as text_file:
        text = text_file.read()
    with open(
        "lab_2_tokenize_by_bpe/assets/secrets/secret_5.txt",
        "r",
        encoding="utf-8"
    ) as text_file:
        secret  = text_file.read()
    with open("lab_2_tokenize_by_bpe/assets/ru_raw.txt", "r", encoding="utf-8") as text_file:
        ru_raw = text_file.read()
    with open(
        "lab_2_tokenize_by_bpe/assets/ru_encoded.txt",
        "r",
        encoding="utf-8"
    ) as text_file:
        reference_encoded_raw = text_file.read()
    with open("lab_2_tokenize_by_bpe/assets/en_raw.txt", "r", encoding="utf-8") as text_file:
        text_reference_translation = text_file.read()
    with open("lab_2_tokenize_by_bpe/assets/en_encoded.txt", "r", encoding="utf-8") as text_file:
        translation_encoded_raw = text_file.read()
    #result = None
    #assert result, "Translation not working"

    #mark 4
    result = collect_frequencies(text, None, "</s>")
    if result is None:
        return
    #print(result)

    #step5
    result_1 = train(result, 100)
    if result_1 is None:
        return
   #print(result_1)

    #secret
    vocabulary = get_vocabulary(result_1,'<unk>')
    assert vocabulary, "Voc is None"

    secret_ids = [int(number) for number in secret.split()]
    result_2 = decode(secret_ids, vocabulary, '</s>')
    assert result_2, "Decode is None"
    # print(result_2)

    #mark8
    vocabulary = load_vocabulary("lab_2_tokenize_by_bpe/assets/vocab.json")
    if vocabulary is None:
        return

    encoded = encode (ru_raw, vocabulary, "\u2581", None, "<unk>")
    if encoded is None:
        return

    reference_encoded = [int(x) for x in reference_encoded_raw.split()]
    n = 20
    # print("полученные токены: ", encoded[:n])
    # print("эталонные токены: ", reference_encoded[:n])
    # print("совпадают ли токены:", encoded[:n] == reference_encoded[:n])

    #mark10
    translation_encoded = [int(x) for x in translation_encoded_raw.split()]

    translation_decoded = decode(translation_encoded, vocabulary, None)
    translation_decoded = translation_decoded.replace("\u2581", " ")

    bleu = calculate_bleu(translation_decoded, text_reference_translation)

    print("Полученный перевод:", translation_decoded)
    print("Эталонный перевод:", text_reference_translation)
    print("BLEU:", bleu)

if __name__ == "__main__":
    main()
