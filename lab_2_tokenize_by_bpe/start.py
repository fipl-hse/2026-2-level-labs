"""
BPE Tokenizer starter
"""

# pylint:disable=too-many-locals, unused-variable
import lab_2_tokenize_by_bpe.main


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

    with open('lab_2_tokenize_by_bpe/assets/secrets/secret_1.txt', 'r', encoding="utf-8") as secret:
        encoded_text = secret.read()

    word_dictionary = lab_2_tokenize_by_bpe.main.collect_frequencies(text, None, '</s>')
    trained_dictionary = lab_2_tokenize_by_bpe.main.train(word_dictionary, 100)
    sorted_dictionary = lab_2_tokenize_by_bpe.main.get_vocabulary(trained_dictionary, '<unk>')
    result = lab_2_tokenize_by_bpe.main.decode([int(number) for number in encoded_text.split()], sorted_dictionary, '</s>')
    print(result)
    assert result, "Translation not working"


if __name__ == "__main__":
    main()
