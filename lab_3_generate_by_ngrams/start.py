"""
Generation by NGrams starter
"""

from lab_3_generate_by_ngrams.main import (
    BeamSearchTextGenerator,
    GreedyTextGenerator,
    NGramLanguageModel,
    TextProcessor,
)

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

    processor = TextProcessor("_")

    encoded = processor.encode(text)
    if encoded is None:
        print("Encoding error")
        return

    print(f"Encoded corpus length: {len(encoded)} tokens")
    print(f"Storage size: {len(processor._storage)} unique characters")
    print(f"First 100 encoded tokens: {encoded[:100]}")

    decoded = processor.decode(encoded)
    if decoded is None:
        print("Decoding error")
        return

    print(f"Decoded text length: {len(decoded)} characters")
    print(f"First 500 characters of decoded text:\n{decoded[:500]}\n")

    n_gram_size = 7
    model = NGramLanguageModel(encoded, n_gram_size)

    if not model.build():
        print("Model build error")
        return

    print(f"Model successfully built for N={n_gram_size}.")
    print(f"Number of unique {n_gram_size}-grams: {len(model._n_gram_frequencies)}")

    print("\nExamples of n-grams and their probabilities:")
    count = 0
    for ngram, prob in model._n_gram_frequencies.items():
        letters = tuple(processor.get_token(token_id) for token_id in ngram)
        print(f"  {ngram} (letters: {letters}) -> probability: {prob:.4f}")
        count += 1
        if count >= 5:
            break

    sequence = tuple(encoded[:n_gram_size])
    print(f"\nPrediction for context {sequence}:")

    next_tokens = model.generate_next_token(sequence)
    if next_tokens is None:
        print("Failed to get next token")
    else:
        print(f"Possible next tokens (id: probability): {next_tokens}")
        for token_id, prob in next_tokens.items():
            token_letter = processor.get_token(token_id)
            print(f"  Token {token_id} ('{token_letter}') with probability: {prob:.4f}")

    generator = GreedyTextGenerator(model, processor)

    prompt = "Vernon"
    seq_len = 51

    print(f"Generating text for prompt: '{prompt}'")
    generated_text = generator.run(prompt, seq_len)

    if generated_text is None:
        print("Generation error")
    else:
        print(f"Generation result:\n{generated_text}")

    beam_width = 3
    beam_generator = BeamSearchTextGenerator(model, processor, beam_width)

    seq_len_beam = 56
    print(f"Generating text for prompt: '{prompt}'")
    print(f"Beam Search Algorithm, Beam width: {beam_width}, Sequence length: {seq_len_beam} tokens")

    beam_generated_text = beam_generator.run(prompt, seq_len_beam)

    if beam_generated_text is None:
        print("Beam Search generation error")
    else:
        print(f"Beam Search result:\n{beam_generated_text}")

    result = beam_generated_text
    assert result


if __name__ == "__main__":
    main()
