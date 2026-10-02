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
    if not(
        isinstance(raw_word, str)
        and (isinstance(start_of_word, str) or start_of_word is None)
        and (isinstance(end_of_word, str) or end_of_word is None)
        ):
        return None

    preprocessed_word = list(raw_word)

    if start_of_word is not None:
        preprocessed_word.insert(0, start_of_word)
    if end_of_word is not None:
        preprocessed_word.append(end_of_word)

    return tuple(preprocessed_word)


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
    if not(
        isinstance(text, str)
        and (isinstance(start_of_word, str) or start_of_word is None)
        and isinstance(end_of_word, str)
        ):
        return None

    word_tokens = text.strip().split()
    freq_dict = {}

    for word in word_tokens:
        prep_word = prepare_word(word, start_of_word, end_of_word)
        if prep_word is None:
            return None

        if prep_word in freq_dict:
            freq_dict[prep_word] += 1
        else:
            freq_dict[prep_word] = 1

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
        if not isinstance(value, int) or isinstance(value, bool):
            return None
        if not all(isinstance(s, str) for s in key):
            return None

    pairs_freq = {}
    for key in word_frequencies:
        for pair in zip(key, key[1:]):
            if pair in pairs_freq:
                pairs_freq[pair] += word_frequencies[key]
            else:
                pairs_freq[pair] = word_frequencies[key]

    return pairs_freq


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
    if (
        not isinstance(word_frequencies, dict)
        or not isinstance(pair, tuple)
        or not len(pair) == 2
        or not all(isinstance(s, str) for s in pair)
        ):
        return None

    for key, value in word_frequencies.items():
        if not isinstance(key, tuple):
            return None
        if not isinstance(value, int) or isinstance(value, bool):
            return None
        if not all(isinstance(s, str) for s in key):
            return None

    upd_dict = {}

    for key in word_frequencies:
        i = 0
        new_key = []
        while i < len(key):
            if i < len(key) - 1 and (key[i], key[i+1]) == pair:
                new_key.append(f'{pair[0]}{pair[1]}')
                i += 2
            else:
                new_key.append(key[i])
                i += 1

        upd_dict[tuple(new_key)] = word_frequencies[key]

    return upd_dict


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
    if (
    not isinstance(num_merges, int)
    or isinstance(num_merges, bool)
    or not isinstance(word_frequencies, dict)
    ):
        return None
    for key, value in word_frequencies.items():
        if not isinstance(key, tuple):
            return None
        if not isinstance(value, int) or isinstance(value, bool):
            return None
        if not all(isinstance(s, str) for s in key):
            return None

    tokenized_text = word_frequencies

    for _ in range(num_merges):
        pairs_dict = count_tokens_pairs(tokenized_text)
        if not pairs_dict:
            break
        if pairs_dict is None:
            return None

        sorted_pairs = sorted(
            pairs_dict.items(),
            key=lambda item: (
                -item[1],
                -len(item[0][0] + item[0][1]),
                item[0][0] + item[0][1]
            )
            )

        merge_pair = sorted_pairs[0][0]

        new_tokenized_text = merge_tokens(tokenized_text, merge_pair)
        if new_tokenized_text is None:
            return None
        if new_tokenized_text == tokenized_text:
            break
        tokenized_text = new_tokenized_text

    return tokenized_text

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
        not isinstance(unknown_token, str)
        or not isinstance(word_frequencies, dict)
    ):
        return None
    for key, value in word_frequencies.items():
        if not isinstance(key, tuple):
            return None
        if not isinstance(value, int) or isinstance(value, bool):
            return None
        if not all(isinstance(s, str) for s in key):
            return None

    unique_tokens = set()
    for word in word_frequencies:
        for token in word:
            unique_tokens.add(token)
            unique_tokens.update(token)

    unique_tokens.add(unknown_token)
    sorted_uniq_tokens = sorted(unique_tokens, key=lambda token: (-len(token), token))

    tokens_id_dict = {token: i for i, token in enumerate(sorted_uniq_tokens)}

    return tokens_id_dict


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
        not isinstance(encoded_text, Sequence)
        or not encoded_text
        or not isinstance(vocabulary, dict)
        or (end_of_word_token is not None and not isinstance(end_of_word_token,str))
        or not all(isinstance(i, int) for i in encoded_text)
    ):
        return None
    for key, value in vocabulary.items():
        if not isinstance(value, int) or isinstance(value, bool):
            return None
        if not isinstance(key, str):
            return None

    id_to_token = {v: k for k, v in vocabulary.items()}
    decoded_text =''.join(id_to_token[t] for t in encoded_text)

    if end_of_word_token is not None:
        decoded_text = decoded_text.replace(end_of_word_token, ' ')

    return decoded_text.strip()

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
