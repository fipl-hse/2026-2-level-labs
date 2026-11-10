"""
Generation by NGrams starter
"""
from lab_3_generate_by_ngrams.main import TextProcessor, WordProcessor, NGramLanguageModel, GreedyTextGenerator
# pylint:disable=too-many-locals, unused-import, unused-variable


def main() -> None:
    """
    Launches an implementation.

    In any case returns, None is returned
    """
    with open(
        "./lab_3_generate_by_ngrams/assets/Harry_Potter.txt", "r", encoding="utf-8"
    ) as text_file:
        text = text_file.read()

    result = None
    assert result

processor = TextProcessor('_')

encoded_text = processor.encode(text[:30])
decoded_text = processor.decode(encoded_text)
assert decoded_text is not None
print(f"Decoded text: {decoded_text}")

processor = WordProcessor('</s>')

encoded_text = processor.encode(text[:100])
decoded_text = processor.decode(encoded_text)
assert encoded_text is not None
print(f"Decoded text: {decoded_text}")

ngram_processor = TextProcessor('_')
encoded_corpus = ngram_processor.encode(text)

if encoded_corpus is not None:
    model = NGramLanguageModel(encoded_corpus, 7)
    build_success = model.build()
    generator = GreedyTextGenerator(model, ngram_processor)
    result_text = generator.run('Vernon', 51)

    print(f"---Result generation (N=7, length=51) ---")
    print(f"'Vernon'")
    print(f"Generated text: {result_text}")
else:
    print("Error")



if __name__ == "__main__":
    main()
