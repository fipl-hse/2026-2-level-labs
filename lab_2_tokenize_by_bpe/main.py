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


    result = []

    if start_of_word is not None:
        result.append(start_of_word)

    for symbol in raw_word:
        result.append(symbol)

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

    if not isinstance(text, str):
        return None

    if start_of_word is not None and not isinstance(start_of_word, str):
        return None

    if not isinstance(end_of_word, str):
        return None


    freq_dict = {}
    words = text.split()

    for word in words:
        tokenized = prepare_word(word, start_of_word, end_of_word)

        if tokenized is None:
            return None

        if tokenized in freq_dict:
            freq_dict[tokenized] += 1
        else:
            freq_dict[tokenized] = 1

    return freq_dict


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

    pairs_dict = {}

    for tokens, number in word_frequencies.items():
        if not isinstance(tokens, tuple) or not isinstance(number, int):
            return None

        for i in range(len(tokens) - 1):
            pair = (tokens[i], tokens[i+1])
            pairs_dict[pair] = pairs_dict.get(pair, 0) + number

    return pairs_dict


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

    if not isinstance(pair[0], str) or not isinstance(pair[1], str):
        return None


    new_freq_dict = {}

    for tokens, freq in word_frequencies.items():
        if not isinstance(tokens, tuple):
            return None

        if not isinstance(freq, int):
            return None

        new_tokens = []
        index = 0

        while index < len(tokens):
            if (
                index < len(tokens) - 1 and
                tokens[index] == pair[0] and
                tokens[index + 1] == pair[1]
            ):
                new_tokens.append(pair[0] + pair[1])
                index += 2
            else:
                new_tokens.append(tokens[index])
                index += 1

        new_word = tuple(new_tokens)

        new_freq_dict[new_word] = new_freq_dict.get(new_word, 0) + freq

    return new_freq_dict


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

    if not isinstance(num_merges, int) or isinstance(num_merges, bool) or num_merges < 0:
        return None


    for _ in range(num_merges):
        pairs = count_tokens_pairs(word_frequencies)

        if pairs is None:
            return None

        if not pairs:
            break

        best_pair = None

        for pair, count in pairs.items():
            if best_pair is None:
                best_pair = pair
                continue

            best_count = pairs[best_pair]
            best_token = best_pair[0] + best_pair[1]
            current_token = pair[0] + pair[1]

            if count > best_count:
                best_pair = pair

            if (count, len(current_token)) > (best_count, len(best_token)):
                best_pair = pair
            elif (
                count == best_count
                and len(current_token) == len(best_token)
                and current_token < best_token
            ):
                best_pair = pair


        if best_pair is None:
            return None

        word_frequencies = merge_tokens(word_frequencies, best_pair)

        if word_frequencies is None:
            return None

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

    tokens = []

    for word in word_frequencies:
        if not isinstance(word, tuple):
            return None

        for token in word:
            if not isinstance(token, str):
                return None

            if token not in tokens:
                tokens.append(token)

            for symb in token:
                if symb not in tokens:
                    tokens.append(symb)

    if unknown_token not in tokens:
        tokens.append(unknown_token)

    tokens.sort(key=lambda token: (-len(token), token))

    vocabulary = {}

    for identifier, token in enumerate(tokens):
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

    if (
        encoded_text is None
        or isinstance(encoded_text, str)
        or not isinstance(encoded_text, (list, tuple))
        or not encoded_text
    ):
        return None

    for token_id in encoded_text:
        if not isinstance(token_id, int) or isinstance(token_id, bool):
            return None

    if not isinstance(vocabulary, dict):
        return None

    for key, value in vocabulary.items():
        if not isinstance(key, str) or not isinstance(value, int) or isinstance(value, bool):
            return None

    if end_of_word_token is not None and not isinstance(end_of_word_token, str):
        return None


    id_to_token = {}

    for token, identifier in vocabulary.items():
        id_to_token[identifier] = token

    decoded = []

    for token_id in encoded_text:
        token = id_to_token.get(token_id, '<unk>')

        if token == end_of_word_token:
            decoded.append(' ')
        else:
            decoded.append(token)

    return ''.join(decoded)


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

    if not isinstance(word, tuple):
        return None

    if not isinstance(vocabulary, dict):
        return None

    if not isinstance(end_of_word, str) and end_of_word is not None:
        return None

    if not isinstance(unknown_token, str):
        return None


    word_to_tokens = []

    for token in vocabulary:
        if token != unknown_token:
            word_to_tokens.append(token)

    word_to_tokens.sort(key = lambda token: (-len(token), token))

    symbols = list(word)

    for token in word_to_tokens:
        length = len(token)
        token_id = 0

        while token_id < len(symbols):
            if ''.join(symbols[token_id : token_id + length]) == token:
                symbols[token_id : token_id + length] = [token]
            token_id += 1

    encoded = []

    for symb in symbols:
        if symb not in vocabulary:
            symb = unknown_token

        encoded.append(vocabulary[symb])

    return encoded


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

    with open(vocab_path, "r", encoding="utf-8") as vocabulary_file:
        vocabulary = json.load(vocabulary_file)

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

    if not isinstance(original_text, str):
        return None

    if (
        not isinstance(vocabulary, dict)
        or not isinstance(unknown_token, str)
    ):
        return None

    if (
        start_of_word_token is not None and not isinstance(start_of_word_token, str)
        or end_of_word_token is not None and not isinstance(end_of_word_token, str)
    ):
        return None


    encoded_text = []

    for raw_word in original_text.split():
        word = prepare_word(raw_word, start_of_word_token, end_of_word_token)

        if word is None:
            return None

        encoded_word = tokenize_word(word, vocabulary, end_of_word_token, unknown_token)

        if encoded_word is None:
            return None

        encoded_text.extend(encoded_word)

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
