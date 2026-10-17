"""
Lab 2.

BPE and machine translation evaluation
"""

import json
import math

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
    if not isinstance(raw_word, str) or\
    not isinstance(start_of_word, str | None) or\
    not isinstance(end_of_word, str | None):
        return None

    tokens = []

    if start_of_word is not None:
        tokens.append(start_of_word)

    tokens.extend(list(raw_word))

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
    if not isinstance(text, str) or\
    not isinstance(start_of_word, str | None) or\
    not isinstance(end_of_word, str):
        return None

    freq_dict = {}

    words_of_text = text.split()

    for word in words_of_text:
        prepared_word = prepare_word(word, start_of_word, end_of_word)

        if prepared_word is None:
            return None

        key = tuple(prepared_word)
        freq_dict[key] = freq_dict.get(key, 0) + 1

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
    for key, value in word_frequencies.items():
        if not isinstance(key, tuple):
            return None
        if not isinstance(value, int):
            return None
        if not key:
            return None
        if not all(isinstance(el, str) for el in key):
            return None

    pairs_frequencies = {}

    for word, frequency in word_frequencies.items():
        for i in range(len(word) - 1):
            pair = (word[i], word[i+1])
            pairs_frequencies[pair] = pairs_frequencies.get(pair, 0) + frequency

    return pairs_frequencies

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
    if (not isinstance(word_frequencies, dict) or\
        not isinstance(pair, tuple) or\
        len(pair) != 2 or\
        not all(isinstance(el, str) for el in pair)):
        return None

    new_word_frequencies = {}
    for word, frequency in word_frequencies.items():
        if not isinstance(word, tuple):
            return None
        if not isinstance(frequency, int):
            return None
        if not word or not all(isinstance(el, str) for el in word):
            return None
        word_list = list(word)
        new_word_list = []
        i = 0
        while i < len(word_list):
            if word_list[i:i+2] == list(pair):
                new_word_list.append(word_list[i] + word_list[i+1])
                i += 2
            else:
                new_word_list.append(word_list[i])
                i += 1
        new_word = tuple(new_word_list)
        new_word_frequencies[new_word] = new_word_frequencies.get(new_word, 0) + frequency

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
    if not isinstance(word_frequencies, dict) or\
        not isinstance(num_merges, int):
        return None
    for key, value in word_frequencies.items():
        if not isinstance(key, tuple) or\
            not isinstance(value, int) or\
                not key or not all(isinstance(el, str) for el in key):
            return None

    for _ in range(num_merges):
        new_word_frequencies = count_tokens_pairs(word_frequencies)
        if new_word_frequencies is None:
            return None
        if not new_word_frequencies:
            break

        tokens_to_compare = list(new_word_frequencies.items())
        sorted_tokens = sorted(
            tokens_to_compare, key=lambda x: (
                -x[1],
                -len("".join(x[0])),
                "".join(x[0])))

        word_frequencies = merge_tokens(word_frequencies, sorted_tokens[0][0])
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
    if word_frequencies is None or\
        not isinstance(word_frequencies, dict | None) or\
        not isinstance(unknown_token, str):
        return None

    unique_tokens = set()

    for word, frequency in word_frequencies.items():
        if not isinstance(word, tuple):
            return None
        if not isinstance(frequency, int):
            return None
        if not word or not all(isinstance(el, str) for el in word):
            return None

        for token in word:
            unique_tokens.add(token)
            unique_tokens.update(token)


    unique_tokens.add(unknown_token)

    return {
        token: i
        for i, token in enumerate(
            sorted(unique_tokens, key=lambda x: (-len(x), x))
        )
    }

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
    if not isinstance(encoded_text, Sequence | None) or \
    not encoded_text or \
    not isinstance(vocabulary, dict | None) or \
    not vocabulary or \
    not isinstance(end_of_word_token, str | None):
        return None
    if encoded_text is not None:
        if not all (isinstance(item, int) for item in encoded_text):
            return None

    reversed_vocabulary = {}
    if vocabulary is not None:
        for key, value in vocabulary.items():
            if not isinstance(key, str) or not isinstance(value, int):
                return None
            reversed_vocabulary[value] = key
    decoded_text = [reversed_vocabulary.get(token_id, "<unk>")
                    for token_id in encoded_text]

    result = "".join(decoded_text)
    if end_of_word_token is not None:
        result = result.replace(end_of_word_token, " ")
    return result

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
    if (not isinstance(word, tuple) or \
        not isinstance(vocabulary, dict) or \
        not isinstance(end_of_word, str | None) or \
        not isinstance(unknown_token, str)):
        return None
    if not all(isinstance(token, str) for token in word) or \
    not all(isinstance(key, str) and isinstance(value, int)
            for key, value in vocabulary.items()):
        return None

    parts = list(word)

    if end_of_word is not None and len(parts) > 0 and parts[-1] == end_of_word:
        parts.pop()
        parts.extend(list(end_of_word))
    elif end_of_word is not None and len(parts) > 0 and parts[-1] != end_of_word:
        parts.extend(list(end_of_word))

    vocabulary_tokens = sorted(vocabulary, key=lambda x: (-len(x), x))

    for token in vocabulary_tokens:
        if not token:
            continue

        token_len = len(token)

        index = 0

        while index <= len(parts) - token_len:
            if "".join(parts[index:index + token_len]) == token:
                parts[index:index + token_len] = [token]
                index += 1
            else:
                index += 1

    return [vocabulary.get(token, vocabulary[unknown_token]) for token in parts]

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

    with open (vocab_path, "r", encoding="utf-8") as file:
        vocabulary = json.load(file)

    if not isinstance(vocabulary, dict):
        return None

    for key, value in vocabulary.items():
        if not all([isinstance(key, str), isinstance(value, int)]):
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
    if (not isinstance(original_text, str) or\
        not isinstance(start_of_word_token, str | None) or\
        not isinstance(end_of_word_token, str | None) or\
        not isinstance(unknown_token, str) or\
        not isinstance(vocabulary, dict)):
        return None
    if not all(isinstance(key, str) and isinstance(value, int)
               for key, value in vocabulary.items()):
        return None

    splitted_text = original_text.strip().split()
    list_of_tokens = []

    for word in splitted_text:
        prepared_word = prepare_word(word, start_of_word_token, end_of_word_token)
        if prepared_word is None:
            return None
        tokenized_word = tokenize_word(prepared_word, vocabulary, end_of_word_token, unknown_token)
        if tokenized_word is None:
            return None
        list_of_tokens.extend(tokenized_word)

    return list_of_tokens


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
    if (not isinstance(text, str)
        or not isinstance(order, int)):
        return None

    ngrams_list = []
    for i in range(len(text) - order + 1):
        ngrams_list.append(tuple(text[i:i + order]))

    return ngrams_list

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
    if not (isinstance(actual, list)
        and isinstance(reference, list)):
        return None
    for ngram in actual:
        if not isinstance(ngram, tuple) or\
            not all((isinstance(i, str)) for i in ngram):
            return None
    for ngram in reference:
        if not isinstance(ngram, tuple) or\
            not all((isinstance(i, str)) for i in ngram):
            return None
    if not actual or not reference:
        return 0.0

    matches = set(actual) & set(reference)

    return len(matches) / len(set(actual))

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
    if not (isinstance(precisions, Sequence)
            and isinstance(max_order, int)):
        return None
    if not all (isinstance(el, (float, int)) for el in precisions):
        return None
    if not precisions:
        return None
    for element in precisions:
        if element <= 0:
            return 0.0

    logs = [math.log(i) for i in precisions]
    return math.exp(sum(logs) / max_order)


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
    if not isinstance(actual, str) or\
    not isinstance(reference, str) or\
    not isinstance(max_order, int):
        return None

    precisions_list = []

    for i in range(1, max_order + 1):
        actual_ngrams = collect_ngrams(actual, i)
        predicted_ngrams = collect_ngrams(reference, i)

        if actual_ngrams is None or\
            predicted_ngrams is None:
            return None

        precision = calculate_precision(actual_ngrams, predicted_ngrams)
        if precision is None:
            return None
        precisions_list.append(precision)

    result = calculate_geo_mean(precisions_list, max_order)
    if result is None:
        return None

    return result * 100
