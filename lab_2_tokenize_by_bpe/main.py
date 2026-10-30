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
    if not (isinstance(raw_word, str) and
        isinstance(start_of_word, str | None) and
        isinstance(end_of_word, str | None)
    ):
        return None

    prepared_word = []

    if start_of_word is not None:
        prepared_word = [start_of_word]

    for symbol in raw_word:
        prepared_word.append(symbol)

    if end_of_word is not None:
        prepared_word.append(end_of_word)

    return tuple(prepared_word)

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
    if not (isinstance(text, str) and
        isinstance(start_of_word, str | None) and
        isinstance(end_of_word, str)
    ):
        return None

    prepared_text = text.split()
    for word in prepared_text:
        if not isinstance(word, str):
            return None

    for word in prepared_text:
        if prepare_word(word, start_of_word, end_of_word) is None:
            return None

    frequencies_dict = {}
    for word in prepared_text:
        prepared_word = prepare_word(word, start_of_word, end_of_word)
        if prepared_word is None:
            return None
        if prepared_word and prepared_word not in frequencies_dict:
            frequencies_dict[prepared_word] = 1
        else:
            frequencies_dict[prepared_word] += 1

    return frequencies_dict

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
    if not (isinstance(word_frequencies, dict) and
        all(isinstance(key, tuple) and isinstance(value, int)
            for key, value in word_frequencies.items()) and
        all(isinstance(el, str) for key in word_frequencies for el in key)
    ):
        return None

    if word_frequencies is None:
        return None

    pair_frequencies = {}
    for key, value in word_frequencies.items():
        for i in range(len(key)-1):
            pair = key[i], key[i+1]
            pair_frequencies[pair] = pair_frequencies.get(pair, 0) + value


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
    if not (isinstance(word_frequencies, dict) and
        isinstance(pair, tuple) and
        all(isinstance(key, tuple) and isinstance(value, int)
            for key, value in word_frequencies.items()) and
        all(isinstance(word, str) for key in word_frequencies for word in key) and
        all(isinstance(token, str) for token in pair)
    ):
        return None

    if word_frequencies is None:
        return None

    new_word_frequencies = {}

    for key, value in word_frequencies.items():
        key_elements = list(key)
        i = 0
        while i < len(key_elements)-1:
            if key_elements[i] == pair[0] and key_elements[i+1] == pair[1]:
                key_elements[i] = pair[0] + pair[1]
                key_elements.pop(i+1)
            else:
                i += 1
        new_word_frequencies[tuple(key_elements)] = value

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

    if not (isinstance(word_frequencies, dict) and
        isinstance(num_merges, int) and
        all(isinstance(key, tuple) and isinstance(value, int)
            for key, value in word_frequencies.items()) and
        all(isinstance(word, str) for key in word_frequencies for word in key)
    ):
        return None

    while num_merges > 0:
        if count_tokens_pairs(word_frequencies) is None:
            return None

        pair_frequencies = count_tokens_pairs(word_frequencies)
        if not pair_frequencies:
            break

        if pair_frequencies is None:
            return None

        max_freq = max(pair_frequencies.values())
        popular_tokens = []

        for key, value in pair_frequencies.items():
            if value == max_freq:
                popular_tokens.append(key)

        max_len = 0
        for token_part_1, token_part_2 in popular_tokens:
            max_len = max(max_len, len(token_part_1 + token_part_2))

        longest = []
        for token_part_1, token_part_2 in popular_tokens:
            if len(token_part_1+token_part_2) == max_len:
                longest.append((token_part_1+token_part_2, (token_part_1, token_part_2)))

        popular_pair = min(longest)[1]

        word_frequencies = merge_tokens(word_frequencies, popular_pair)

        if word_frequencies is None:
            return None

        num_merges -= 1

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
    if not (isinstance(word_frequencies, dict) and
        isinstance(unknown_token, str) and
        all(isinstance(key, tuple) and isinstance(value, int)
            for key, value in word_frequencies.items()) and
        all(isinstance(word, str) for key in word_frequencies for word in key)
    ):
        return None

    vocabulary_lst = [el for key in word_frequencies.keys() for el in key]

    for token in vocabulary_lst:
        if len(token) > 1:
            vocabulary_lst.extend(list(token))
    vocabulary_lst.append(unknown_token)

    vocabulary_lst = sorted(vocabulary_lst, key = lambda token: (-len(token), token))

    vocabulary = {}
    i = 0
    for el in vocabulary_lst:
        if el not in vocabulary:
            vocabulary[el] = i
            i+=1

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
    if not (isinstance(encoded_text, list) and
        isinstance(vocabulary, dict) and
        all(isinstance(key, str) and isinstance(value, int)
            for key,value in vocabulary.items()) and
        isinstance(end_of_word_token, str | None)
    ):
        return None

    result = ""
    keys_lst = list(vocabulary.keys())
    value_lst = list(vocabulary.values())
    for ch in encoded_text:
        token_ind = value_lst.index(ch)
        token = keys_lst[token_ind]
        result += token

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

    if not (isinstance(word, tuple) and
        all(isinstance(el, str) for el in word) and
        isinstance(vocabulary, dict)
    ):
        return None

    if not(all(isinstance(token, str) and isinstance(value, int)
            for token, value in vocabulary.items()) and
        isinstance(end_of_word, str | None) and
        isinstance(unknown_token, str)
    ):
        return None

    joined_word = "".join(word)

    tokens = [key for key in vocabulary.keys() if key in joined_word]
    tokens = sorted(tokens, key = lambda token: (-len(token), token))

    number_of_cut = 0

    encoded_word: list[str | int] = [joined_word]
    tokens_in_word = []
    for token in tokens:
        parts_encoded_word = []
        for element in encoded_word:
            if isinstance(element, int) or token not in element:
                parts_encoded_word.append(element)
            else:
                piece = element.split(token)
                number_of_cut += 1
                tokens_in_word.append(token)
                for i, char in enumerate(piece):
                    if i > 0:
                        parts_encoded_word.append(vocabulary[token])
                    if char:
                        parts_encoded_word.append(char)
        encoded_word = parts_encoded_word

    result = []
    for element in encoded_word:
        if isinstance(element, int):
            result.append(element)
        else:
            result.extend([vocabulary[unknown_token]]*len(element))

    return result, number_of_cut, tokens_in_word

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

    with open(vocab_path, "r", encoding = "utf-8") as text_file:
        vocabulary = json.load(text_file)

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
    if not(
        isinstance(original_text, str) and
        isinstance(vocabulary, dict)
    ):
        return None

    if not all(
        isinstance(key, str) and isinstance(value, int)
        for key, value in vocabulary.items()
    ):
        return None

    if not (
        isinstance(start_of_word_token, str | None) and
        isinstance(end_of_word_token, str | None) and
        isinstance(unknown_token, str)
    ):
        return None

    prepared_text = original_text.split()

    freq_of_cut = {}
    encoded_text = []
    for word in prepared_text:
        prepared_word = prepare_word(word, start_of_word_token, end_of_word_token)
        if prepared_word is None:
            return None

        encoded_word, number_of_cut, tokens_in_most_cut_word = tokenize_word(prepared_word, vocabulary, end_of_word_token, unknown_token)
        freq_of_cut[word] = number_of_cut
        if encoded_word is None:
            return None

        encoded_text.extend(encoded_word)

    cut_values = list(freq_of_cut.values())
    cut_max_ind = cut_values.index(max(cut_values))
    most_cut_word = list(freq_of_cut.keys())[cut_max_ind]
    _, _, tokens_in_most_cut_word = tokenize_word (prepare_word(most_cut_word, start_of_word_token, end_of_word_token), vocabulary, end_of_word_token, unknown_token)

    sorted_most_cut = dict(sorted(freq_of_cut.items(), key=lambda item: item[1], reverse = True))


    return encoded_text, most_cut_word, list(sorted_most_cut.keys())[:4], tokens_in_most_cut_word

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
