"""
Lab 2.

BPE and machine translation evaluation
"""

# pylint:disable=unused-argument
import json
from typing import Sequence


def prepare_word(
    raw_word: str, start_of_word: str | None, end_of_word: str | None
) -> tuple[str, ...] | None:
    """
    Tokenize a word into characters and attach optional boundary tokens.

    Args:
        raw_word (str): Original word
        start_of_word (str | None): A token that signifies the start of word
        end_of_word (str | None): A token that signifies the end of word

    Returns:
        tuple[str, ...] | None: Preprocessed word

    In case of corrupt input arguments, None is returned
    """
    if not isinstance(raw_word, str):
        return None
    if start_of_word is not None and not isinstance(start_of_word, str):
        return None
    if end_of_word is not None and not isinstance(end_of_word, str):
        return None

    tokens = list(raw_word)

    if start_of_word is not None:
        tokens.insert(0, start_of_word)

    if end_of_word is not None:
        tokens.append(end_of_word)

    return tuple(tokens)


def collect_frequencies(
    text: str, start_of_word: str | None, end_of_word: str
) -> dict[tuple[str, ...], int] | None:
    """
    Count number of occurrences of each word.

    Args:
        text (str): Original text with no preprocessing
        start_of_word (str | None): A token that signifies the start of word
        end_of_word (str): A token that signifies the end of word

    Returns:
        dict[tuple[str, ...], int] | None: Dictionary where key - preprocessed word,
            value - number of occurrences

    In case of corrupt input arguments or functions used return None,
    None is returned
    """
    if not isinstance(text, str):
        return None
    if start_of_word is not None and not isinstance(start_of_word, str):
        return None
    if not isinstance(end_of_word, str):
        return None

    frequencies = {}
    words = text.split()

    for word in words:
        prepared_word = prepare_word(word, start_of_word, end_of_word)

        if prepared_word is None:
            return None

        frequencies[prepared_word] = frequencies.get(prepared_word, 0) + 1

    return frequencies


def count_tokens_pairs(
    word_frequencies: dict[tuple[str, ...], int],
) -> dict[tuple[str, str], int] | None:
    """
    Count number of occurrences of each pair of subsequent tokens.

    Args:
        word_frequencies (dict[tuple[str, ...], int]): A dictionary where
            key - preprocessed word, value - number of occurrences

    Returns:
        dict[tuple[str, str], int] | None: A dictionary where
            key - token pair, value - number of occurrences

    In case of corrupt input arguments, None is returned
    """
    if not isinstance(word_frequencies, dict):
        return None
    pair_frequencies = {}

    for word, freq in word_frequencies.items():
        for i in range(len(word) - 1):
            pair = (word[i], word[i + 1])
            pair_frequencies[pair] = pair_frequencies.get(pair, 0) + freq

    return pair_frequencies



def merge_tokens(
    word_frequencies: dict[tuple[str, ...], int], pair: tuple[str, str]
) -> dict[tuple[str, ...], int] | None:
    """
    Update word frequency dictionary by replacing a pair of tokens with a merged one.

    Args:
        word_frequencies (dict[tuple[str, ...], int]): A dictionary where
            key - preprocessed word, value - number of occurrences
        pair (tuple[str, str]): A pair of tokens to be merged

    Returns:
        dict[tuple[str, ...], int] | None: A dictionary where
            key - preprocessed word, value - number of occurrences

    In case of corrupt input arguments, None is returned
    """
    if not isinstance(word_frequencies, dict) or not isinstance(pair, tuple):
        return None
    merged_frequencies = {}

    for word, freq in word_frequencies.items():
        new_word = []
        i = 0

        while i < len(word):
            if i < len(word) - 1 and (word[i], word[i + 1]) == pair:
                new_word.append(word[i] + word[i + 1])
                i += 2
            else:
                new_word.append(word[i])
                i += 1

        merged_frequencies[tuple(new_word)] = freq

    return merged_frequencies


def train(
    word_frequencies: dict[tuple[str, ...], int] | None, num_merges: int
) -> dict[tuple[str, ...], int] | None:
    """
    Create required number of new tokens by merging existing ones.

    Args:
        word_frequencies (dict[tuple[str, ...], int] | None): A dictionary where
            key - preprocessed word, value - number of occurrences
        num_merges (int): Required number of new tokens

    Returns:
        dict[tuple[str, ...], int] | None: A dictionary where
            key - preprocessed word, value - number of occurrences

    In case of corrupt input arguments or functions used return None,
    None is returned
    """
    if not isinstance(word_frequencies, dict) or not isinstance(num_merges, int):
        return None
    trained_frequencies = dict(word_frequencies)

    for _ in range(num_merges):
        pairs = count_tokens_pairs(trained_frequencies)
        if not pairs:
            break
        def sort_key(p: tuple[str, str]) -> tuple[int, int, str]:
            # pylint: disable=cell-var-from-loop
            assert pairs is not None
            return -pairs[p], -len("".join(p)), "".join(p)
        
        best_pair = sorted(pairs.keys(), key=sort_key)[0]

        new_frequencies = merge_tokens(trained_frequencies, best_pair)
        if new_frequencies is None:
            return None
        trained_frequencies = new_frequencies

    return trained_frequencies

def get_vocabulary(
    word_frequencies: dict[tuple[str, ...], int], unknown_token: str
) -> dict[str, int] | None:
    """
    Establish correspondence between tokens and its integer identifier.

    Args:
        word_frequencies (dict[tuple[str, ...], int]): A dictionary where
            key - preprocessed word, value - number of occurrences
        unknown_token (str): A token to signify an unknown token

    Returns:
        dict[str, int] | None: A dictionary where key - token, value - identifier

    In case of corrupt input arguments, None is returned
    """
    if not isinstance(word_frequencies, dict) or not isinstance(unknown_token, str):
        return None
    unique_tokens = {unknown_token}

    for word in word_frequencies.keys():
        for token in word:
            unique_tokens.add(token)
            for char in token:
                unique_tokens.add(char)

    sorted_tokens = sorted(unique_tokens, key=lambda x: (-len(x), x))

    return {token: i for i, token in enumerate(sorted_tokens)}


def decode(
    encoded_text: Sequence[int] | None,
    vocabulary: dict[str, int] | None,
    end_of_word_token: str | None,
) -> str | None:
    """
    Translate encoded sequence into decoded one.

    Args:
        encoded_text (Sequence[int] | None): A sequence of token identifiers
        vocabulary (dict[str, int] | None): A dictionary where
            key - token, value - identifier
        end_of_word_token (str | None): An end-of-word token

    Returns:
        str | None: Decoded sequence

    In case of corrupt input arguments, None is returned
    """
    if not isinstance(encoded_text, list) or not isinstance(vocabulary, dict):
        return None
    if end_of_word_token is not None and not isinstance(end_of_word_token, str):
        return None
    inverted_vocab = {v: k for k, v in vocabulary.items()}
    decoded_tokens = []

    for token_id in encoded_text:
        token = inverted_vocab.get(token_id)
        if token is not None:
            decoded_tokens.append(token)

    result_text = "".join(decoded_tokens)
    if end_of_word_token is not None:
        result_text = result_text.replace(end_of_word_token, " ")

    return result_text

def tokenize_word(
    word: tuple[str, ...], vocabulary: dict[str, int], end_of_word: str | None, unknown_token: str
) -> list[int] | None:
    """
    Split word into tokens.

    Args:
        word (tuple[str, ...]): Preprocessed word
        vocabulary (dict[str, int]): A dictionary where key - token, value - identifier
        end_of_word (str | None): An end-of-word token
        unknown_token (str): A token that signifies unknown sequence

    Returns:
        list[int] | None: A list of token identifiers

    In case of corrupt input arguments, None is returned
    """
    if not isinstance(word, tuple) or not isinstance(vocabulary, dict) or not isinstance(unknown_token, str):
        return None
    if end_of_word is not None and not isinstance(end_of_word, str):
        return None

    sorted_tokens = sorted(vocabulary.keys(), key=lambda x: (-len(x), x))
    result_list = list(word)

    for token in sorted_tokens:
        i = 0
        while i < len(result_list):
            span_str = ""
            for j in range(i, len(result_list)):
                span_str += result_list[j]

                if span_str == token:
                    result_list[i:j + 1] = [token]
                    break
                if len(span_str) > len(token):
                    break
            i += 1

    return [
        vocabulary.get(token, vocabulary.get(unknown_token, 0))
        for token in result_list
    ]



def load_vocabulary(vocab_path: str) -> dict[str, int] | None:
    """
    Read and retrieve dictionary of type <token: identifier>.

    Args:
        vocab_path (str): A path to the saved vocabulary

    Returns:
        dict[str, int] | None: A dictionary where key - token, value - identifier

    In case of corrupt input arguments, None is returned
    """
    if not isinstance(vocab_path, str):
        return None

    with open(vocab_path, 'r', encoding='utf-8') as f:
        vocabulary = json.load(f)

    if not isinstance(vocabulary, dict):
        return None

    return vocabulary



def encode(
    original_text: str,
    vocabulary: dict[str, int] | None,
    start_of_word_token: str | None,
    end_of_word_token: str | None,
    unknown_token: str,
) -> list[int] | None:
    """
    Translate original text into a sequence of token identifiers.

    Args:
        original_text (str): Original text
        vocabulary (dict[str, int] | None): A dictionary where key - token, value - identifier
        start_of_word_token (str | None): A start-of-word token
        end_of_word_token (str | None): An end-of-word token
        unknown_token (str): A token that signifies unknown sequence

    Returns:
        list[int] | None: A list of token identifiers

    In case of corrupt input arguments or functions used return None,
    None is returned
    """
    if (
        not isinstance(original_text, str)
        or not isinstance(vocabulary, dict)
        or not isinstance(unknown_token, str)
    ):
        return None
    if start_of_word_token is not None and not isinstance(start_of_word_token, str):
        return None
    if end_of_word_token is not None and not isinstance(end_of_word_token, str):
        return None

    encoded_text = []

    for word in original_text.split():
        prepared = prepare_word(word, start_of_word_token, end_of_word_token)
        if prepared is None:
            return None

        tokenized = tokenize_word(prepared, vocabulary, end_of_word_token, unknown_token)
        if tokenized is None:
            return None

        encoded_text.extend(tokenized)

    return encoded_text


def collect_ngrams(text: str, order: int) -> list[tuple[str, ...]] | None:
    """
    Extract n-grams from the given sequence.

    Args:
        text (str): Original text
        order (int): Required number of elements in a single n-gram

    Returns:
        list[tuple[str, ...]] | None: A sequence of n-grams

    In case of corrupt input arguments, None is returned
    """


def calculate_precision(
    actual: Sequence[tuple[str, ...]], reference: Sequence[tuple[str, ...]]
) -> float | None:
    """
    Compare two sequences by virtue of Precision metric.

    Args:
        actual (Sequence[tuple[str, ...]]): Predicted sequence of n-grams
        reference (Sequence[tuple[str, ...]]): Expected sequence of n-grams

    Returns:
        float | None: Value of Precision metric

    In case of corrupt input arguments, None is returned.
    """


def calculate_geo_mean(precisions: Sequence[float], max_order: int) -> float | None:
    """
    Compute geometric mean of sequence of values.

    Args:
        precisions (Sequence[float]): A sequence of Precision values
        max_order (int): Maximum length of n-gram considered

    Returns:
        float | None: A value of geometric mean of Precision metric

    In case of corrupt input arguments, None is returned
    """


def calculate_bleu(actual: str | None, reference: str, max_order: int = 3) -> float | None:
    """
    Compare two sequences by virtue of BLEU metric.

    Args:
        actual (str | None): Predicted sequence
        reference (str): Expected sequence
        max_order (int, optional): Max length of n-gram to consider for comparison. Defaults to 3

    Returns:
        float | None: A value of BLEU metric

    In case of corrupt input arguments or functions used return None,
    None is returned
    """
