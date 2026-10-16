"""
Lab 2.

BPE and machine translation evaluation
"""

# pylint:disable=unused-argument
from json import load
from math import e, exp, log
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
        (isinstance(raw_word, str) and raw_word)
        and (isinstance(start_of_word, str) or start_of_word is None)
        and (isinstance(end_of_word, str) or end_of_word is None)
    ):
        return None

    word_by_sym = list(raw_word.strip())
    if start_of_word is not None:
        word_by_sym.insert(0, start_of_word)
    if end_of_word is not None:
        word_by_sym.append(end_of_word)
    return tuple(word_by_sym)


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
        (isinstance(text, str) and text)
        and (isinstance(start_of_word, str) or start_of_word is None)
        and isinstance(end_of_word, str)
    ):
        return None

    list_of_words = text.split()
    word_frequencies = {}
    for word in list_of_words:
        word_by_sym = prepare_word(word, start_of_word, end_of_word)
        if word_by_sym is None:
            return None
        word_frequencies[word_by_sym] = list_of_words.count(word)
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
    if not(
        isinstance(word_frequencies, dict)
        and all(((
            isinstance(word_by_sym, tuple)
            and all((isinstance(sym, str) for sym in word_by_sym))
        ) for word_by_sym in word_frequencies))
        and all((isinstance(frequency, int) for frequency in word_frequencies.values()))
    ):
        return None

    pairs = []
    for word, frequency in word_frequencies.items():
        for ind in range(len(word) - 1):
            pair = word[ind], word[ind + 1]
            for _ in range(frequency):
                pairs.append(pair)
    return {pair: pairs.count(pair) for pair in pairs}


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
    if not(
        isinstance(word_frequencies, dict)
        and all(((
            isinstance(word_by_sym, tuple)
            and all((isinstance(sym, str) for sym in word_by_sym))
        ) for word_by_sym in word_frequencies))
        and all((isinstance(frequency, int) for frequency in word_frequencies.values()))
        and (isinstance(pair, tuple) and len(pair) == 2)
        and all((isinstance(sym, str) for sym in pair))
    ):
        return None

    new_token = "".join(pair)
    upd_word_frequencies = {}
    for word in word_frequencies:
        word_to_upd_dict = []
        ind = 0
        while ind < len(word):
            if ind < len(word) - 1 and (word[ind], word[ind + 1]) == pair:
                word_to_upd_dict.append(new_token)
                ind += 2
            else:
                word_to_upd_dict.append(word[ind])
                ind += 1
        upd_word_frequencies[tuple(word_to_upd_dict)] = word_frequencies.get(word)
    return upd_word_frequencies


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
    if not(
        ((
            isinstance(word_frequencies, dict)
            and all(((
                isinstance(word_by_sym, tuple)
                and all((isinstance(sym, str) for sym in word_by_sym))
            ) for word_by_sym in word_frequencies))
            and all((isinstance(frequency, int) for frequency in word_frequencies.values()))
        ) and word_frequencies)
        and isinstance(num_merges, int)
    ):
        return None

    for _ in range(num_merges):
        pairs = count_tokens_pairs(word_frequencies)
        if pairs is None:
            return None
        if not pairs:
            break
        sorted_pairs = sorted(
            pairs.items(),
            key=lambda item: (-item[1], -len("".join(item[0])), "".join(item[0]))
        ) if pairs is not None else None
        word_frequencies = (
            merge_tokens(word_frequencies, sorted_pairs[0][0])
            if sorted_pairs is not None
            else None
        )
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
    if not(
        isinstance(word_frequencies, dict)
        and all(((
            isinstance(word_by_sym, tuple)
            and all((isinstance(sym, str) for sym in word_by_sym))
        ) for word_by_sym in word_frequencies))
        and all((isinstance(frequency, int) for frequency in word_frequencies.values()))
        and isinstance(unknown_token, str)
    ):
        return None

    vocabulary = {unknown_token}
    for word in word_frequencies:
        for token in word:
            vocabulary.add(token)
            vocabulary.update(token)
    sorted_vocabulary = sorted(vocabulary, key=lambda token: (-len(token), token))
    return {token: ident for ident, token in enumerate(sorted_vocabulary)}


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
    if not(
        ((
            isinstance(encoded_text, Sequence)
            and all((isinstance(num, int) for num in encoded_text))
        ) and encoded_text)
        and ((
            isinstance(vocabulary, dict)
            and all((
                isinstance(item[0], str) and isinstance(item[1], int)
                for item in vocabulary.items()
            ))
        ) and vocabulary)
        and (isinstance(end_of_word_token, str) or end_of_word_token is None)
    ):
        return None

    reversed_vocabulary = {ident: token for token, ident in vocabulary.items()}
    decoded_tokens = [reversed_vocabulary.get(ident) for ident in encoded_text]
    decoded_text = "".join(decoded_tokens)
    if end_of_word_token is not None:
        decoded_text = decoded_text.replace(end_of_word_token, " ")
    return decoded_text


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
    if not(
        (isinstance(word, tuple) and all((isinstance(sym, str) for sym in word)))
        and (
            isinstance(vocabulary, dict)
            and all((
                isinstance(item[0], str) and isinstance(item[1], int)
                for item in vocabulary.items()
            ))
        )
        and (isinstance(end_of_word, str) or end_of_word is None)
        and isinstance(unknown_token, str)
    ):
        return None

    sorted_tokens = sorted(vocabulary, key=lambda token: (-len(token), token))
    word_to_str = "".join(word)
    covered = [False] * len(word_to_str)
    word_fragments = []

    for token in sorted_tokens:
        current_start_ind = 0
        while True:
            start_of_token = word_to_str.find(token, current_start_ind)
            if start_of_token == -1:
                break
            end_of_token = start_of_token + len(token)

            if any(covered[start_of_token:end_of_token]):
                current_start_ind = start_of_token + 1
            else:
                for i in range(start_of_token, end_of_token):
                    covered[i] = True
                word_fragments.append((
                    start_of_token,
                    end_of_token,
                    vocabulary[token]
                ))
                current_start_ind = end_of_token

    for ind, iscovered in enumerate(covered):
        if not iscovered:
            word_fragments.append((ind, ind + 1, vocabulary[unknown_token]))
    sorted_word_fragments = sorted(word_fragments, key=lambda item: item[0])
    return [item[2] for item in sorted_word_fragments]


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

    with open(vocab_path, "r", encoding="utf-8") as file:
        vocab = load(file)

    if not(
        isinstance(vocab, dict)
        and all((
            isinstance(item[0], str) and isinstance(item[1], int)
            for item in vocab.items()
        ))
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
    if not(
        isinstance(original_text, str)
        and (
            isinstance(vocabulary, dict)
            and all((
                isinstance(item[0], str) and isinstance(item[1], int)
                for item in vocabulary.items()
            ))
        )
        and (isinstance(start_of_word_token, str) or start_of_word_token is None)
        and (isinstance(end_of_word_token, str) or end_of_word_token is None)
        and isinstance(unknown_token, str)
    ):
        return None

    wordlist = original_text.split()
    encoded_text = []
    for word in wordlist:
        prepared_word = prepare_word(word, start_of_word_token, end_of_word_token)
        if prepared_word is None:
            return None
        tokenized_word = tokenize_word(
            prepared_word,
            vocabulary,
            end_of_word_token,
            unknown_token
        )
        if tokenized_word is None:
            return None
        encoded_text.extend(tokenized_word)
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
    if not(isinstance(text, str) and isinstance(order, int)):
        return None

    ngrams = []
    for ind in range(len(text) - order + 1):
        text_fragment = text[ind:ind+order]
        ngrams.append(tuple(text_fragment))
    return ngrams



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
    if not(
        isinstance(actual, Sequence)
        and isinstance(reference, Sequence)
        and all((
            isinstance(ngram, tuple)
            and all((isinstance(sym, str) for sym in ngram))
        ) for ngram in actual)
        and all((
            isinstance(ngram, tuple)
            and all((isinstance(sym, str) for sym in ngram))
        ) for ngram in reference)
    ):
        return None

    if not actual or not reference:
        return 0.0

    coincidence = set(actual) & set(reference)
    return len(coincidence) / len(set(reference))


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
    if not(
        (isinstance(precisions, Sequence) and precisions)
        and all(isinstance(precision, (float, int)) for precision in precisions)
        and (isinstance(max_order, int) and max_order > 0)
    ):
        return None

    if any(precision <= 0 for precision in precisions):
        return 0.0

    precision_sum = sum(log(precision, e) for precision in precisions)
    return exp(max_order**(-1) * precision_sum)


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
    if not(
        (isinstance(actual, str) and actual)
        and isinstance(reference, str)
        and isinstance(max_order, int)
    ):
        return None

    precisions = []
    for i in range(1, max_order + 1):
        actual_ngrams = collect_ngrams(actual, i)
        reference_ngrams = collect_ngrams(reference, i)
        if actual_ngrams is None or reference_ngrams is None:
            return None
        precision = calculate_precision(actual_ngrams, reference_ngrams)
        if precision is None:
            return None
        precisions.append(precision)
    geo_mean = calculate_geo_mean(precisions, max_order)
    if geo_mean is None:
        return None
    return geo_mean * 100
