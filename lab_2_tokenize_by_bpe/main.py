"""
Lab 2.

BPE and machine translation evaluation
"""

import json

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

    if not isinstance(raw_word, str):
        return None
    if start_of_word is not None and not isinstance(start_of_word, str):
        return None
    if end_of_word is not None and not isinstance(end_of_word, str):
        return None
    word = tuple(raw_word)
    if start_of_word is not None:
        word = (start_of_word,) + word
    if end_of_word is not None:
        word = word + (end_of_word,)
    return word


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
    for word in text.split():
        prepared = prepare_word(word, start_of_word, end_of_word)
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
    for word in word_frequencies.keys():
        if not isinstance(word, tuple):
            return None
    pairs = {}
    for word, freq in word_frequencies.items():
        for i, token in enumerate(word[:-1]):
            pair = (token, word[i + 1])
            pairs[pair] = pairs.get(pair, 0) + freq
    return pairs


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
    for word in word_frequencies.keys():
        if not isinstance(word, tuple):
            return None
    merged = pair[0] + pair[1]
    new_frequencies = {}
    for word, freq in word_frequencies.items():
        new_word = []
        i = 0
        while i < len(word):
            if i < len(word) - 1 and word[i] == pair[0] and word[i + 1] == pair[1]:
                new_word.append(merged)
                i += 2
                continue
            new_word.append(word[i])
            i += 1
        new_word_tuple = tuple(new_word)
        new_frequencies[new_word_tuple] = new_frequencies.get(new_word_tuple, 0) + freq
    return new_frequencies


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

    for _ in range(num_merges):
        pairs = count_tokens_pairs(word_frequencies)
        if pairs is None:
            return None
        if not pairs:
            break

        best_pair = sorted(
            pairs.items(),
            key=lambda item: (
                -item[1],
                -len(item[0][0] + item[0][1]),
                item[0][0] + item[0][1],
            ),
        )[0][0]

        result = merge_tokens(word_frequencies, best_pair)
        if result is None:
            return None
        word_frequencies = result

    return word_frequencies


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
    for word in word_frequencies.keys():
        if not isinstance(word, tuple):
            return None
        for token in word:
            if not isinstance(token, str):
                return None

    unique_tokens = {unknown_token}
    for word in word_frequencies.keys():
        for token in word:
            unique_tokens.add(token)
            for char in token:
                unique_tokens.add(char)

    sorted_tokens = sorted(unique_tokens, key=lambda t: (-len(t), t))
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

    if not isinstance(encoded_text, (list, tuple)) or len(encoded_text) == 0:
        return None
    if not isinstance(vocabulary, dict):
        return None
    if end_of_word_token is not None and not isinstance(end_of_word_token, str):
        return None

    id_to_token = {}
    for key, value in vocabulary.items():
        id_to_token[value] = key
    decoded_tokens = []
    for identifier in encoded_text:
        found = id_to_token.get(identifier)
        if found is None:
            return None
        decoded_tokens.append(found)
    text = "".join(decoded_tokens)
    if end_of_word_token is not None:
        text = text.replace(end_of_word_token, " ")
    return text


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

    if (
        not isinstance(word, tuple)
        or not isinstance(vocabulary, dict)
        or (end_of_word is not None and not isinstance(end_of_word, str))
        or not isinstance(unknown_token, str)
    ):
        return None

    word_str = "".join(word)
    sorted_tokens = sorted(vocabulary.keys(), key=lambda t: (-len(t), t))

    result = []
    i = 0
    while i < len(word_str):
        found = None
        for token in sorted_tokens:
            if token == unknown_token:
                continue
            if word_str.startswith(token, i):
                found = token
                break
        if found is not None:
            result.append(vocabulary[found])
            i += len(found)
        else:
            result.append(vocabulary[unknown_token])
            i += 1
    return result


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
    try:
        with open(vocab_path, "r", encoding="utf-8") as f:
            vocab = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return None
    if not isinstance(vocab, dict):
        return None
    for key, value in vocab.items():
        if not isinstance(key, str):
            return None
        if not isinstance(value, int):
            return None
    return vocab


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

    if not isinstance(original_text, str) or not isinstance(vocabulary, dict):
        return None
    if (
        (start_of_word_token is not None and not isinstance(start_of_word_token, str))
        or (end_of_word_token is not None and not isinstance(end_of_word_token, str))
        or not isinstance(unknown_token, str)
    ):
        return None

    result = []
    for raw_word in original_text.split():
        prepared = prepare_word(raw_word, start_of_word_token, end_of_word_token)
        if prepared is None:
            return None
        ids = tokenize_word(prepared, vocabulary, end_of_word_token, unknown_token)
        if ids is None:
            return None
        result.extend(ids)
    return result


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
