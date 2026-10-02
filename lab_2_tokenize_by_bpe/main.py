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
    words = text.split()
    for word in words:
        prepared = prepare_word(word, start_of_word, end_of_word)
        if prepared is None:
            return None
        if prepared in frequencies:
            frequencies[prepared] += 1
        else:
            frequencies[prepared] = 1
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
    pairs = {}
    for word, freq in word_frequencies.items():
        if not isinstance(word, tuple):
            return None
        for i in range(len(word) - 1):
            pair = (word[i], word[i + 1])
            if pair in pairs:
                pairs[pair] += freq
            else:
                pairs[pair] = freq
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
    merged = pair[0] + pair[1]
    new_frequencies = {}
    for word, freq in word_frequencies.items():
        if not isinstance(word, tuple):
            return None
        new_word = []
        i = 0
        while i < len(word):
            if i < len(word) - 1 and word[i] == pair[0] and word[i + 1] == pair[1]:
                new_word.append(merged)
                i += 2
            else:
                new_word.append(word[i])
                i += 1
        new_word_tuple = tuple(new_word)
        if new_word_tuple in new_frequencies:
            new_frequencies[new_word_tuple] += freq
        else:
            new_frequencies[new_word_tuple] = freq
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
        sorted_pairs = sorted(
            pairs.items(),
            key=lambda item: (
                -item[1],
                -len(item[0][0] + item[0][1]),
                item[0][0] + item[0][1]
            ),
        )
        best_pair = sorted_pairs[0][0]
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
    unique_tokens = set()
    unique_tokens.add(unknown_token)
    for word in word_frequencies.keys():
        if not isinstance(word, tuple):
            return None
        for token in word:
            unique_tokens.add(token)
    sorted_tokens = sorted(list(unique_tokens), key=lambda t: (-len(t), t))
    vocabulary = {}
    for i, token in enumerate(sorted_tokens):
        vocabulary[token] = i
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

    if encoded_text is None:
        return None
    if vocabulary is None:
        return None
    if end_of_word_token is not None and not isinstance(end_of_word_token, str):
        return None
    id_to_token = {}
    for token, identifier in vocabulary.items():
        id_to_token[identifier] = token
    decoded_tokens = []
    for identifier in encoded_text:
        token = id_to_token.get(identifier)
        if token is None:
            return None
        decoded_tokens.append(token)
    text = "".join(decoded_tokens)
    if end_of_word_token is not None:
        text = text.replace(end_of_word_token, " ")
    return text.strip()


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
