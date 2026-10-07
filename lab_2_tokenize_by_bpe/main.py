"""
Lab 2.

BPE and machine translation evaluation
"""

# pylint:disable=unused-argument
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
    if not all((
        isinstance(raw_word, str),
        isinstance(start_of_word, (str, type(None))),
        isinstance(end_of_word, (str, type(None))),
    )):
        return None

    result = []
    if start_of_word is not None:
        result.append(start_of_word)
    result.extend(raw_word)
    if end_of_word is not None:
        result.append(end_of_word)
    return tuple(result)

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
    if not all((
        isinstance(text, str),
        isinstance(start_of_word, (str, type(None))),
        isinstance(end_of_word, str),
    )):
        return None

    frequencies = {}
    for raw_word in text.split():
        prepared = prepare_word(raw_word, start_of_word, end_of_word)
        if prepared is None:
            return None
        frequencies[prepared] = frequencies.get(prepared, 0) + 1
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
    for tokens, frequency in word_frequencies.items():
        if not isinstance(tokens, tuple) or not isinstance(frequency, int):
            return None
        for index in range(len(tokens) - 1):
            pair = (tokens[index], tokens[index + 1])
            pair_frequencies[pair] = pair_frequencies.get(pair, 0) + frequency
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
    if not isinstance(word_frequencies, dict):
        return None
    if not isinstance(pair, tuple) or len(pair) != 2:
        return None

    merged_token = pair[0] + pair[1]
    merged_frequencies = {}

    for tokens, frequency in word_frequencies.items():
        if not isinstance(tokens, tuple) or not isinstance(frequency, int):
            return None

        merged_word = []
        position = 0
        while position < len(tokens):
            if tokens[position:position + 2] == pair:
                merged_word.append(merged_token)
                position += 2
            else:
                merged_word.append(tokens[position])
                position += 1

        merged_word_tuple = tuple(merged_word)
        merged_frequencies[merged_word_tuple] = (
            merged_frequencies.get(merged_word_tuple, 0) + frequency
        )
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
    if not isinstance(word_frequencies, dict):
        return None
    if not isinstance(num_merges, int) or num_merges < 0:
        return None

    def sort_key(pair_and_frequency):
        pair, frequency = pair_and_frequency
        merged_token = pair[0] + pair[1]
        return (-frequency, -len(merged_token), merged_token)

    current_frequencies = dict(word_frequencies)

    for _ in range(num_merges):
        pair_frequencies = count_tokens_pairs(current_frequencies)
        if not pair_frequencies:
            break

        best_item = min(pair_frequencies.items(), key=sort_key)
        pair_to_merge = best_item[0]

        current_frequencies = merge_tokens(current_frequencies, pair_to_merge)
        if current_frequencies is None:
            return None

    return current_frequencies

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
    if not isinstance(word_frequencies, dict):
        return None
    if not isinstance(unknown_token, str):
        return None

    unique_tokens = {unknown_token}
    for tokens in word_frequencies.keys():
        for token in tokens:
            unique_tokens.add(token)
            unique_tokens.update(token)

    ordered_tokens = sorted(unique_tokens, key=lambda token: (-len(token), token))

    vocabulary = {}
    for identifier, token in enumerate(ordered_tokens):
        vocabulary[token] = identifier
    return vocabulary

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
    if not isinstance(encoded_text, (list, tuple)):
        return None
    if not encoded_text:
        return None
    if not isinstance(vocabulary, dict):
        return None
    if end_of_word_token is not None and not isinstance(end_of_word_token, str):
        return None

    id_to_token = {}
    for token, identifier in vocabulary.items():
        if not isinstance(token, str) or not isinstance(identifier, int):
            return None
        id_to_token[identifier] = token

    parts = []
    for identifier in encoded_text:
        if not isinstance(identifier, int):
            return None
        if identifier not in id_to_token:
            return None

        token = id_to_token[identifier]

        if token == end_of_word_token:
            parts.append(" ")
        else:
            parts.append(token)

    return ''.join(parts)


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


def load_vocabulary(vocab_path: str) -> dict[str, int] | None:
    """
    Read and retrieve dictionary of type <token: identifier>.

    Args:
        vocab_path (str): A path to the saved vocabulary

    Returns:
        dict[str, int] | None: A dictionary where key - token, value - identifier

    In case of corrupt input arguments, None is returned
    """


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
