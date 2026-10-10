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
    if not all (
        [
            isinstance(raw_word,
                            str),
            any([
                isinstance(start_of_word,
                                    str),
                not start_of_word
                ]),
            any([
                isinstance(end_of_word,
                                    str),
                not end_of_word
                ])
        ]
    ):
        return None

    if any (
        [
            isinstance(end_of_word, (tuple,
                                    list,
                                    dict)),
            start_of_word == 0,

            isinstance(start_of_word, (tuple,
                                        list,
                                        dict)),
        end_of_word == 0
        ]
    ):
        return None

    list_of_tokens = []

    if start_of_word:
        list_of_tokens.append(start_of_word)

    for letter in raw_word:
        list_of_tokens.append(letter)

    if end_of_word:
        list_of_tokens.append(end_of_word)

    return tuple(list_of_tokens)


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
    if not all(
            [
                isinstance(text,
                            str),
                any ([
                    isinstance(start_of_word,
                                        str),
                    not start_of_word
                    ]),
                isinstance(end_of_word,
                                    str)
            ]
    ):
        return None

    list_with_repetitions = text.split()
    text_without_repetitions = set(list_with_repetitions)

    dict_of_frequencies = {}
    for i in text_without_repetitions:
        prepared_word = prepare_word(i,
                                    start_of_word,
                                    end_of_word)
        if not isinstance(
                    prepared_word,
                    tuple):
                    return None

        dict_of_frequencies[
                    prepared_word
                         ] = list_with_repetitions.count(i)

    return dict_of_frequencies


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
    if not isinstance(word_frequencies,
                                    dict):
        return None

    unpacked_dict = []
    for key in word_frequencies:
        counter = word_frequencies[key]
        while counter != 0:
            unpacked_dict.append(key)
            counter -= 1

    list_of_tokens = []
    for key in unpacked_dict:
        tokens = [(key[(index - 1)], key[index])
                  for index in range(len(key))
                  if index > 0]
        list_of_tokens.extend(tokens)

    original_tokens = set(list_of_tokens)

    dict_of_pair_frequency = {}
    for i in original_tokens:
        dict_of_pair_frequency[i] = list_of_tokens.count(i)

    return dict_of_pair_frequency


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
    if not all(
        [
            isinstance(word_frequencies,
                                    dict),
            isinstance(pair,
                        tuple)
        ]
    ):
        return None

    if not all(
        [
                len(pair) == 2,
                all (
                    isinstance(element,
                                    str)
                    for element in pair
                    )
        ]
    ):
        return None

    for keys, values in word_frequencies.items():
        if not all(
            [
                isinstance(keys,
                            tuple),
                isinstance(values,
                                int),
                all (
                    isinstance(item,
                                str)
                    for item in keys
                    )
            ]
        ):
            return None

    list_of_keys = list(word_frequencies.keys())

    keys_as_lists = [
                list(element)
                for element
                in list_of_keys]

    for element in keys_as_lists:
        indexes = list(range(len(element) - 1))
        for index in indexes:
            if (
                element[index] == pair[0]
                and element[index + 1] == pair[1]
                ):
                element.pop(index + 1)
                indexes.pop(len(element) - 1)
                element[index] = (f'{pair[0]}{pair[1]}')

    keys_as_tuples = [
            tuple(element)
            for element
            in keys_as_lists
    ]

    list_of_frequencies = list(word_frequencies.values())

    new_dict = dict(zip(keys_as_tuples, list_of_frequencies))

    return new_dict


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
    if not all([
        isinstance(word_frequencies,
                                dict),
        isinstance(num_merges,
                            int)
    ]):
        return None

    for key, values in word_frequencies.items():
        if not all([
            isinstance(key,
                       tuple),
            isinstance(values,
                       int),
            all (
                isinstance(letter,
                                str)
                for letter in key
                )
        ]):
            return None

    if num_merges < 0:
        return None

    for _ in range(num_merges):

        pair_frequency = count_tokens_pairs(word_frequencies)
        if not pair_frequency:
            break

        unpacked_pair_frequency = list(
            pair_frequency.items()
        )

        sorted_list_of_frequencies = sorted(
            unpacked_pair_frequency, key = lambda x: (
                -x[1],
                -(len(x[0][0] + x[0][1])),
                x[0][0] + x[0][1]
            )
        )

        tokenised_text = merge_tokens(word_frequencies,
                                    sorted_list_of_frequencies[0][0])

        if not tokenised_text:
            return None

        if tokenised_text == word_frequencies:
            break

        word_frequencies = tokenised_text

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
    if not all([
        isinstance(word_frequencies,
                                dict),
        isinstance(unknown_token,
                                str)
    ]):
        return None

    for keys, value in word_frequencies.items():
        if not all(
            [
            isinstance(keys,
                        tuple),
            isinstance(value,
                            int),
            all(
                isinstance(token,
                                str)
                for token
                in keys
                )
            ]
        ):
            return None

    list_of_words = []
    list_of_letters = []
    for key in word_frequencies.keys():

        for tokens in key:
            list_of_letters.append(tokens)
            list_of_words.append(tokens)

            for letter in tokens:
                list_of_words.append(letter)

    list_of_words.append(unknown_token)

    list_of_original_words = []
    for item in list_of_words:
        if item not in list_of_original_words:
            list_of_original_words.append(item)

    sorted_list = sorted(list_of_original_words, key = lambda x: (-len(x), x))

    list_of_identification_numbers = list(
        range(len(sorted_list))
    )

    dict_of_identificators = dict(
        zip(sorted_list,
            list_of_identification_numbers)
    )
    return dict_of_identificators


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
        not isinstance(encoded_text,
                            Sequence)
        or not encoded_text
        or not isinstance(vocabulary,
                                dict)
        or not vocabulary
        or (end_of_word_token is not None
            and not isinstance(end_of_word_token,
                                                str))
        or not all(isinstance(i,
                              int)
                   for i
                   in encoded_text)
    ):
        return None

    for key, value in vocabulary.items():
        if not isinstance(value,
                                int):
            return None
        if not isinstance(key,
                            str):
            return None

    keys = list(vocabulary.keys())
    values = list(vocabulary.values())
    vocabulary = dict(zip(values, keys))

    if isinstance(encoded_text, str):
        encoded_text.split(" ")

    list_of_encoded_tokens = [
        vocabulary[token]
        for token
        in encoded_text
    ]

    sentence = "".join(list_of_encoded_tokens)

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
    if not all(
        [
            all(
                [
                    isinstance(word,
                                tuple),
                    word
                ]
            ),
            isinstance(vocabulary,
                                dict),
            isinstance(end_of_word,
                                str),
            isinstance(unknown_token,
                                    str)
        ]
    ):
        return None

    for keys, values in vocabulary.items():
        if not all(
            [
                isinstance(keys,
                                str),
                isinstance(values,
                                int),
                all(
                    isinstance(letter,
                                    str)
                        for letter in word
                    )
            ]
        ):
            return None

    full_word = "".join(word)
    word_tokenised = [i for i in full_word]
    result = []

    vocabulary_sorted = sorted(vocabulary.keys(), key = lambda x: (-len(x), x))

    for token in vocabulary_sorted:
        while token in full_word:
            start_find = 0
            first_index_word = full_word.index(token[0], start_find)
            last_index_word = full_word.index(token[(len(token)) - 1], start_find)
            while full_word[first_index_word:last_index_word + 1] != token[0:(len(token))]:
                first_index_word = full_word.index(token[0], start_find)
                last_index_word = full_word.index(token[(len(token)) - 1], start_find)
                start_find += 1
            for i in range(word_tokenised.index(token[0], start_find) + 1, word_tokenised.index(token[(len(token)) - 1], start_find) + 1):
                word_tokenised[i] = None
            word_tokenised[word_tokenised.index(token[0], start_find)] = vocabulary[token]

            full_word = "".join(element for element in word_tokenised if isinstance(element, str))

    for i in range(len(word_tokenised)):
        if word_tokenised[i] and not isinstance(word_tokenised[i], int):
            word_tokenised[i] = vocabulary[unknown_token]

    for element in word_tokenised:
        if isinstance(element, int):
            result.append(element)

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
    if not isinstance (vocab_path,
                                str):
        return None

    with open (f"{vocab_path}", "r", encoding="utf-8") as file:
        vocab = json.load(file)

    if not isinstance(vocab,
                        dict):
        return None

    for key, value in vocab.items():
        if not all(
            [
            isinstance(key,
                        str),
            isinstance(value,
                            int)
            ]
        ):
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
