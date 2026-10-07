"""
BPE Tokenizer starter
"""

# pylint:disable=too-many-locals, unused-variable
from lab_2_tokenize_by_bpe.main import (
    collect_frequencies,
    decode,
    get_vocabulary,
    train,
)


def main() -> None:
    """
    Launches an implementation
    """
    with open("lab_2_tokenize_by_bpe/assets/text.txt", "r", encoding="utf-8") as text_file:
        text = text_file.read()
    with open("lab_2_tokenize_by_bpe/assets/secrets/secret_5.txt", "r", encoding="utf-8") as text_file:
        secret  = text_file.read()
    # with open("lab_2_tokenize_by_bpe/assets/en_raw.txt", "r", encoding="utf-8") as text_file:
    #     text_reference_translation = text_file.read()
    # with open("lab_2_tokenize_by_bpe/assets/en_encoded.txt", "r", encoding="utf-8") as text_file:
    #     translation_encoded_raw = text_file.read()
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

    secret = [int(number) for number in secret.split()]
    result_2 = decode(secret, vocabulary, '</s>')
    assert result_2, "Decode is None"
    print(result_2)



if __name__ == "__main__":
    main()
