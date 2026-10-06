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
    if(
    not isinstance(raw_word, str)
    or not isinstance(start_of_word, str | None)
    or not isinstance(end_of_word, str | None)
    ):
        return None

    tokens = []

    if start_of_word is not None:
        tokens.append(start_of_word)

    tokens.extend(raw_word)

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
    if(
    not isinstance(text,str)
    or not isinstance(start_of_word, str | None)
    or not isinstance(end_of_word, str)
    ):
        return None

    word_frequencies = {}

    for raw_word in text.split():
        prepared_word = prepare_word(raw_word, start_of_word, end_of_word)

        if prepared_word is None:
            return None

        word_frequencies[prepared_word] = word_frequencies.get(prepared_word, 0) + 1

    return word_frequencies


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
    if(
    not isinstance(word_frequencies, dict)
    or not all(isinstance(key, tuple) for key in word_frequencies)
    or not all(isinstance(j, str) for i in word_frequencies for j in i)
    or not all(isinstance(value, int) for value in word_frequencies.values())
    ):
        return None

    b_tokens_dict = {}
    for word, freq in word_frequencies.items():
        for i in range(len(word) - 1):
            b_token = (word[i],word[i+1])

            b_tokens_dict[b_token] = b_tokens_dict.get(b_token, 0) + freq

    return b_tokens_dict

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
    if(
    not isinstance(word_frequencies, dict)
    or not all(isinstance(key, tuple) for key in word_frequencies)
    or not all(isinstance(j, str) for i in word_frequencies for j in i)
    or not all(isinstance(value, int) for value in word_frequencies.values())
    ):
        return None
    if(
    not isinstance(pair, tuple)
    or len(pair) != 2
    or not all(isinstance(el, str) for el in pair)
    ):
        return None

    new_token = pair[0] + pair[1]

    new_word_frequencies = {}

    for key, value in word_frequencies.items():
        new_key = key

        for i, token in enumerate(key):
            if i + 1 < len(key):
                if token == pair[0] and key[i+1] == pair[1]:
                    new_key = key[:i] + (new_token,) + key[i+2:]

        new_word_frequencies[new_key] = value

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
    if(
    not isinstance(word_frequencies, dict)
    or not all(isinstance(key, tuple) for key in word_frequencies)
    or not all(isinstance(j, str) for i in word_frequencies for j in i)
    or not all(isinstance(value, int) for value in word_frequencies.values())
    or not isinstance(num_merges, int)
    ):
        return None

    for _ in range(num_merges):
        pairs_frequencies = count_tokens_pairs(word_frequencies)

        if pairs_frequencies is None:
            return None

        if not pairs_frequencies:
            break

        sorted_pair_frequencies = sorted(pairs_frequencies.items(),
                                        key=lambda item: (
            -item[1],
            -len(item[0][0] + item[0][1]),
            item[0][0] + item[0][1],
        ))

        new_frequencies = merge_tokens(word_frequencies, sorted_pair_frequencies[0][0])

        if new_frequencies is None:
            return None

        word_frequencies = new_frequencies

    return new_frequencies



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
    if(
    not isinstance(word_frequencies, dict)
    or not all(isinstance(key, tuple) for key in word_frequencies)
    or not all(isinstance(j, str) for i in word_frequencies for j in i)
    or not all(isinstance(value, int) for value in word_frequencies.values())
    or not isinstance(unknown_token, str)
    ):
        return None

    tokens = set()

    for key in word_frequencies:
        for token in key:
            tokens.add(token)
            for symbol in token:
                tokens.add(symbol)

    tokens.add(unknown_token)
    sorted_tokens = sorted(tokens,key=lambda x: (-len(x), x))

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
    if encoded_text is None or vocabulary is None:
        return None
    if(
    not isinstance(encoded_text, list)
    or not all(isinstance(i, int) for i in encoded_text)
    or not isinstance(end_of_word_token, str | None)
    ):
        return None
    if(
    not isinstance(vocabulary, dict)
    or not all(isinstance(key, str) for key in vocabulary)
    or not all(isinstance(value, int) for value in vocabulary.values())
    ):
        return None

    id_dict = {v: k for k, v in vocabulary.items()}

    decoded_symbols = []
    for token_id in encoded_text:
        token = id_dict[token_id]
        if end_of_word_token is not None:
         token = token.replace(end_of_word_token, " ")

        decoded_symbols.append(token)

    return "".join(decoded_symbols)


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
