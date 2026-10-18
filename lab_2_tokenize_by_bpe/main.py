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

    frequencies = {}

    for raw_word in text.split():
        word = prepare_word(raw_word, start_of_word, end_of_word)
        if word is None:
            return None
        frequencies[word] = frequencies.get(word, 0) + 1

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

    for key, value in word_frequencies.items():
        if not isinstance(key, tuple):
            return None
        if not all(isinstance(token, str) for token in key):
            return None
        if not isinstance(value, int) or isinstance(value, bool):
            return None

    pairs = {}

    for word, frequency in word_frequencies.items():
        for i in range(len(word) - 1):
            pair = (word[i], word[i + 1])
            pairs[pair] = pairs.get(pair, 0) + frequency

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

    for key, value in word_frequencies.items():
        if not isinstance(key, tuple):
            return None
        if not all(isinstance(token, str) for token in key):
            return None
        if not isinstance(value, int) or isinstance(value, bool):
            return None

    if not isinstance(pair, tuple):
        return None

    if not all(isinstance(item, str) for item in pair):
        return None

    if len(pair) != 2:
        return None

    new_word_frequencies = {}
    first_token, second_token = pair
    merged_token = first_token + second_token

    for word, freq in word_frequencies.items():
        new_word = []
        i = 0
        while i < len(word):
            if i < len(word) - 1 and word[i] == first_token and word[i + 1] == second_token:
                new_word.append(merged_token)
                i += 2
                continue
            new_word.append(word[i])
            i += 1
        new_word_frequencies[tuple(new_word)] = (
        new_word_frequencies.get(tuple(new_word), 0) + freq
        )

    return new_word_frequencies

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
    if word_frequencies is None or not isinstance(word_frequencies, dict):
        return None

    for key, value in word_frequencies.items():
        if not isinstance(key, tuple):
            return None
        if not all(isinstance(token, str) for token in key):
            return None
        if not isinstance(value, int) or isinstance(value, bool):
            return None

    if not isinstance(num_merges, int):
        return None

    for i in range(num_merges):
        collecting_pairs = count_tokens_pairs(word_frequencies)
        if not collecting_pairs:
            break
        best_pair = sorted(collecting_pairs.items(), key=lambda pair: (-pair[1], -len(pair[0][0] + pair[0][1]), pair[0]))[0][0]
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
    if word_frequencies is None or not isinstance(word_frequencies, dict):
            return None

    for key, value in word_frequencies.items():
        if not isinstance(key, tuple):
            return None
        if not all(isinstance(token, str) for token in key):
            return None
        if not isinstance(value, int) or isinstance(value, bool):
            return None

    if not isinstance(unknown_token, str):
        return None

    all_tokens = set()
    all_tokens.add(unknown_token)

    for word in word_frequencies.keys():
        for token in word:
            all_tokens.add(token)
            for char in token:
                all_tokens.add(char)

    sorted_tokens = sorted(all_tokens, key=lambda token: (-len(token), token))
    vocabulary = {}

    for idx, token in enumerate(sorted_tokens):
        vocabulary[token] = idx

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
    if encoded_text is None or not isinstance(encoded_text, Sequence) or isinstance(encoded_text, str):
        return None

    if len(encoded_text) == 0:
        return None

    for item in encoded_text:
        if not isinstance(item, int) or isinstance(item, bool):
            return None

    if vocabulary is None or not isinstance(vocabulary, dict):
        return None

    for key, value in vocabulary.items():
        if not isinstance(key, str):
            return None
        if not isinstance(value, int) or isinstance(value, bool):
            return None

    if end_of_word_token is not None and not isinstance(end_of_word_token, str):
        return None

    id_to_token = {}
    for key, value in vocabulary.items():
        id_to_token[value] = key

    decoded = []

    for token_id in encoded_text:
        token = id_to_token.get(token_id)
        if token is None:
            continue
        if end_of_word_token is not None:
            token = token.replace(end_of_word_token, " ")
        decoded.append(token)

    decoded_string = "".join(decoded)

    return decoded_string

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
    if not isinstance(word, tuple) or not all(isinstance(t, str) for t in word):
        return None

    if not isinstance(vocabulary, dict):
        return None

    for key, value in vocabulary.items():
        if not isinstance(key, str):
            return None
        if not isinstance(value, int) or isinstance(value, bool):
            return None

    if end_of_word is not None and not isinstance(end_of_word, str):
        return None

    if not isinstance(unknown_token, str):
        return None

    if unknown_token not in vocabulary:
        return None

    if len(word) == 0:
        return []

    word_string = "".join(word)
    letters_used = []

    for i in range(len(word_string)):
        letters_used.append(False)

    found_tokens = {}
    sorted_tokens = sorted(vocabulary.keys(), key=lambda token: (-len(token), token))

    for token in sorted_tokens:
        if token == unknown_token:
            continue

        start = 0
        while True:
            idx = word_string.find(token, start)

            if idx == -1:
                break

            is_overlapping = False

            for i in range(idx, idx + len(token)):
                if letters_used[i] == True:
                    is_overlapping = True
                    break

            if not is_overlapping:
                found_tokens[idx] = (vocabulary[token], len(token))
                for i in range(idx, idx + len(token)):
                    letters_used[i] = True

            start = idx + 1

    result = []
    i = 0

    while i < len(word_string):
        if i in found_tokens:
            token_id, token_length = found_tokens[i]
            result.append(token_id)
            i += token_length
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
        with open("lab_2_tokenize_by_bpe/assets/vocab.json", "r", encoding="utf-8") as file:
            vocabulary = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return None

    if not isinstance(vocabulary, dict):
        return None

    for key, value in vocabulary.items():
        if not isinstance(key, str):
            return None
        if not isinstance(value, int) or isinstance(value, bool):
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

    if vocabulary is None or not isinstance(vocabulary, dict):
            return None

    for key, value in vocabulary.items():
        if not isinstance(key, str):
            return None
        if not isinstance(value, int) or isinstance(value, bool):
            return None

    if start_of_word_token is not None and not isinstance(start_of_word_token, str):
        return None

    if end_of_word_token is not None and not isinstance(end_of_word_token, str):
        return None

    if not isinstance(unknown_token, str):
        return None

    words = original_text.split()
    encoded_tokens = []

    for raw_word in words:
        prepared = prepare_word(raw_word, start_of_word_token, end_of_word_token)
        if prepared is None:
            return None

    token_ids = tokenize_word(prepared, vocabulary, end_of_word_token, unknown_token)

    if token_ids is None:
        return None

    encoded_tokens.extend(token_ids)

    return encoded_tokens

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
