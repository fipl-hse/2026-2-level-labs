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
    if (not isinstance(raw_word, str)
        or (not isinstance(start_of_word, str) and start_of_word is not None)
            or (not isinstance(end_of_word, str) and end_of_word is not None)):
        return None

    res = []
    if start_of_word is not None:
        res.append(start_of_word)

    res.extend(list(raw_word))

    if end_of_word is not None:
        res.append(end_of_word)

    return tuple(res)


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
    if (not isinstance(text, str)
            or (not isinstance(start_of_word, str) and start_of_word is not None)
            or not isinstance(end_of_word, str)):
        return None

    freq_dict = {}

    for word in text.split():
        prepared = prepare_word(word, start_of_word, end_of_word)
        if prepared is None:
            return None
        freq_dict[prepared] = freq_dict.get(prepared, 0) + 1

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
    if (not all(isinstance(k,  tuple)
                    and isinstance(v, (bool, int))
                    and isinstance(token, str)
                    for k, v in word_frequencies.items() for token in k)
            ):
        return None

    res = {}
    for word, freq in reversed(list(word_frequencies.items())):
        for pos in range(len(word) - 1, 0, -1):
            pair = (word[pos - 1], word[pos])
            res[pair] = res.get(pair, 0) + freq

    return res


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
    if (not isinstance(word_frequencies, dict)
        or not isinstance(pair, tuple)
        or len(pair) != 2
        or not all(isinstance(token, str) for token in pair)
        or not all(isinstance(k, tuple)
                   and isinstance(v, (int, bool))
                   and isinstance(token, str)
                   for k, v in word_frequencies.items() for token in k)):
        return None

    merged = ''.join(pair)
    res = {}

    for word, freq in word_frequencies.items():
        new_word = []
        i = 0
        while i < len(word):
            if i < len(word) - 1 and word[i] == pair[0] and word[i + 1] == pair[1]:
                new_word.append(merged)
                i += 2
            else:
                new_word.append(word[i])
                i += 1
        res[tuple(new_word)] = freq

    return res


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
    if (not isinstance(word_frequencies, dict)
        or not isinstance(num_merges, int)
        or not all(isinstance(k, tuple)
                   and isinstance(v, (int, bool))
                   and all(isinstance(token, str) for token in k)
                   for k, v in word_frequencies.items())):

        return None

    corpus = word_frequencies
    merges_done = 0

    while merges_done < num_merges:
        stats = count_tokens_pairs(corpus)
        if not stats:
            break

        chosen_pair = min(
            stats.items(),
            key=lambda item: (
                -item[1],
                -len(''.join(item[0])),
                ''.join(item[0])
            )
        )[0]
        new_corpus = merge_tokens(corpus, chosen_pair)

        if new_corpus is None:
            return None

        if new_corpus == corpus:
            break

        corpus = new_corpus
        merges_done += 1

    return corpus


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
    if (
        not isinstance(word_frequencies, dict)
        or not isinstance(unknown_token, str)
    ):
        return None

    if not all(
        isinstance(k, tuple) and isinstance(v, int)
        for k, v in word_frequencies.items()
    ):
        return None

    candidates: list[str] = []
    for word in word_frequencies:
        for token in word:
            candidates.append(token)
            candidates.extend(token)

    candidates.append(unknown_token)

    unique_tokens: list[str] = []
    for candidate in candidates:
        if candidate not in unique_tokens:
            unique_tokens.append(candidate)

    ordered_tokens = sorted(
        unique_tokens, key=lambda token: (-len(token), token))

    return {token: identifier for identifier, token in enumerate(ordered_tokens)}


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
    if end_of_word_token is not None and not isinstance(end_of_word_token, str):
        return None

    if not isinstance(encoded_text, Sequence) or isinstance(encoded_text, str):
        return None
    if not encoded_text:
        return None
    if not all(isinstance(identifier, int) for identifier in encoded_text):
        return None

    if not isinstance(vocabulary, dict) or not vocabulary:
        return None
    for token, identifier in vocabulary.items():
        if not isinstance(token, str):
            return None
        if not isinstance(identifier, int):
            return None

    identifier_to_token = {
        identifier: token for token, identifier in vocabulary.items()
    }

    decoded_tokens = [identifier_to_token[identifier]
                      for identifier in encoded_text]
    sentence = "".join(decoded_tokens)

    if end_of_word_token:
        sentence = sentence.replace(end_of_word_token, " ")

    return sentence


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
    if not all(isinstance(part, str) for part in word):
        return None

    if not (isinstance(end_of_word, str) or end_of_word is None):
        return None
    if not isinstance(unknown_token, str):
        return None

    if not isinstance(vocabulary, dict):
        return None
    for token, identifier in vocabulary.items():
        if not isinstance(token, str):
            return None
        if not isinstance(identifier, int):
            return None

    raw_text = "".join(word)

    matching_tokens = [token for token in vocabulary if token in raw_text]
    matching_tokens.sort(key=lambda token: (-len(token), token))

    pieces: list[str | int] = [raw_text]
    for token in matching_tokens:
        updated_pieces: list[str | int] = []
        for piece in pieces:
            if isinstance(piece, int) or token not in piece:
                updated_pieces.append(piece)
                continue

            fragments = piece.split(token)
            for position, fragment in enumerate(fragments):
                if position > 0:
                    updated_pieces.append(vocabulary[token])
                if fragment:
                    updated_pieces.append(fragment)
        pieces = updated_pieces

    unknown_identifier = vocabulary[unknown_token]
    encoded: list[int] = []
    for piece in pieces:
        if isinstance(piece, int):
            encoded.append(piece)
        else:
            encoded.extend([unknown_identifier] * len(piece))

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

    with open(vocab_path, "r", encoding="utf-8") as file_handle:
        loaded_data = json.load(file_handle)

    if not isinstance(loaded_data, dict):
        return None

    for token, identifier in loaded_data.items():
        if not isinstance(token, str):
            return None
        if not isinstance(identifier, int):
            return None

    return loaded_data


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
    if (not isinstance(original_text, str)
        or not (isinstance(start_of_word_token, str) or start_of_word_token is None)
        or not (isinstance(end_of_word_token, str) or end_of_word_token is None)
        or not isinstance(unknown_token, str)
        or not isinstance(vocabulary, dict)
        or not all(isinstance(token, str) and isinstance(identifier, int)
                   for token, identifier in vocabulary.items())):
        return None

    encoded: list[int] = []
    for raw_word in original_text.split():
        prepared = prepare_word(
            raw_word, start_of_word_token, end_of_word_token)
        if prepared is None:
            return None

        encoded_word = tokenize_word(
            prepared, vocabulary, end_of_word_token, unknown_token
        )
        if encoded_word is None:
            return None

        encoded.extend(encoded_word)

    return encoded


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
