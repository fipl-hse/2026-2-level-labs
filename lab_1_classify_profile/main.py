"""
Lab 1.

Language detection
"""

# pylint:disable=unused-argument
from typing import Sequence
import json

FreqDictType = dict[str, float]
"Frequency dictionary. Contains pairs of token and its frequency."
ProfileType = tuple[str, FreqDictType, int]
"Language profile of a text. Contains language name, frequency dictionary and number of tokens."
# Mark 4.

def tokenize(text: str) -> Sequence[str] | None:
    """
    Splits a text into tokens, converts the tokens into lowercase,
    removes punctuation and other symbols from words

    Args:
       text (str): Text

    Returns:
        Sequence[str] | None: Sequence of lower-cased tokens without punctuation.
        Returns None if input text is not a string.
    """

    if not isinstance(text, str):
        return None


    tokenized_text = []

    for word in text.lower().split():
        clean_word = ''
        for char in word:
            if char.isalpha():
                clean_word += char

        if clean_word:
            tokenized_text.append(clean_word)

    return tokenized_text

def remove_stop_words(tokens: Sequence[str], stop_words: Sequence[str]) -> Sequence[str] | None:
    """
    Removes stop words

    Args:
        tokens (Sequence[str]): Sequence of tokens
        stop_words (Sequence[str]): Sequence of stop words (can be empty)
    Returns:
        Sequence[str] | None: Sequence of tokens without stop words.
        Returns None in case of incorrect input types.
    """
    if not isinstance(tokens, (list, tuple)) or not isinstance(stop_words, (list, tuple)):
        return None

    if not all(isinstance(word, str) for word in tokens):
        return None

    if not all(isinstance(word, str) and word.isalpha() for word in stop_words):
        return None

    stop_words_set =set(stop_words) # for optimization

    filtered_tokens = []

    for token in tokens:
        if token not in stop_words_set:
            filtered_tokens.append(token)

    return filtered_tokens

def calculate_frequencies(tokens: Sequence[str]) -> dict[str, float] | None:
    """
    Calculates frequencies of given tokens

    Args:
        tokens (Sequence[str]): Sequence of tokens
    Returns:
        dict[str, float] | None: Dictionary with frequencies.
        Returns None in case of incorrect input types.
    """
    if not isinstance(tokens, Sequence):
        return None

    if tokens is None or not all(isinstance(word, str) for word in tokens):
        return None

    total_n = len(tokens)
    if total_n == 0:
        return {}

    tokens_set = set(tokens)
    tokens_freq = {}

    for token in tokens_set:
        n = tokens.count(token)
        tokens_freq[token] = n / total_n

    return tokens_freq


def get_top_n_words(freq_dict: dict[str, float], top_n: int) -> Sequence[str] | None:
    """
    Finds the most common words

    Args:
        freq_dict (dict[str, float]): Dictionary with frequencies
        top_n (int): Number of the most common words

    Returns:
        Sequence[str] | None: Sequence of the most common words.
        Returns None in case of incorrect input types or non-positive top_n.
    """
    if not isinstance(freq_dict, dict) or not isinstance(top_n, int):
        return None

    if top_n <= 0:
        return None

    sorted_freq_dict = sorted(freq_dict.items(), key = lambda item: (-item[1],item))


    return [word for word, freq in sorted_freq_dict[:top_n]]



# Mark 6.


def create_language_profile(
    language: str, text: str, stop_words: Sequence[str]
) -> ProfileType | None:
    """
    Creates a language profile

    Args:
        language (str): Language name
        text (str): Text
        stop_words (Sequence[str]): Sequence of stop words (can be empty)

    Returns:
        ProfileType | None: Language profile.
        Returns None in case of incorrect input types.
    """
    if not isinstance(language, str):
        return None

    tokenized_text = tokenize(text)
    if tokenized_text is None:
        return None
    filtered_tokens = remove_stop_words(tokenized_text, stop_words)
    if filtered_tokens is None:
        return None
    tokens_freq = calculate_frequencies(filtered_tokens)
    if tokens_freq is None:
        return None

    return (language, tokens_freq, len(tokens_freq))

def check_profile(profile: ProfileType) -> bool:
    """
    Checks profile structure

    Args:
        profile (ProfileType): Profile to check

    Returns:
        bool: Returns True if the profile has right structure and types,
        otherwise returns False.
    """

    if not isinstance(profile, tuple) or len(profile) != 3:
        return False

    language, freq_dict, n = profile

    if not isinstance(language, str):
        return False

    if not isinstance(freq_dict, dict):
        return False

    for key, value in freq_dict.items():
        if not isinstance(key, str):
            return False
        if not isinstance(value, (int, float)):
            return False

    if not isinstance(n, (int, float)):
        return False

    return True


def compare_profiles_by_top_n(
    unknown_profile: ProfileType, profile_to_compare: ProfileType, top_n: int
) -> float | None:
    """
    Compares profiles and calculates the distance using top n words

    Args:
        unknown_profile (ProfileType): Unknown profile
        profile_to_compare (ProfileType): Profile of a known language
        top_n (int): Number of the most common words
    Returns:
        float | None: The distance between profiles.
        Returns None in case of incorrect input types.
    """

    if not check_profile(unknown_profile) or not check_profile(profile_to_compare) or top_n == 0:
        return None

    top_n_unk_profile = get_top_n_words(unknown_profile[1], top_n)
    if top_n_unk_profile is None:
        return None

    top_n_profile_to_compare = get_top_n_words(profile_to_compare[1], top_n)
    if top_n_profile_to_compare is None:
        return None

    common_words = len(set(top_n_unk_profile) & set(top_n_profile_to_compare))

    return common_words / len(top_n_unk_profile)

def detect_language_by_top_n(
    unknown_profile: ProfileType, profile_1: ProfileType, profile_2: ProfileType, top_n: int
) -> str | None:
    """
    Detects the language of an unknown profile

    Args:
        unknown_profile (ProfileType): Unknown profile
        profile_1 (ProfileType): Profile for comparison
        profile_2 (ProfileType): Another profile for comparison
        top_n (int): Number of the most common words


    Returns:
        str | None: Unknown profile language.
        Returns None in case of incorrect input types.
    """

    compare_unk_to_1 = compare_profiles_by_top_n(unknown_profile, profile_1, top_n)
    if compare_unk_to_1 is None:
        return None
    compare_unk_to_2 = compare_profiles_by_top_n(unknown_profile, profile_2, top_n)
    if compare_unk_to_2 is None:
        return None

    if compare_unk_to_1 > compare_unk_to_2:
        return profile_1[0]
    if compare_unk_to_1 < compare_unk_to_2:
        return profile_2[0]

    return min(profile_1[0], profile_2[0])


# Mark 8


def calculate_mse(predicted: Sequence[float], actual: Sequence[float]) -> float | None:
    """
    Calculates mean squared error between predicted and actual values.

    Args:
        predicted (Sequence[float]): Sequence of predicted values
        actual (Sequence[float]): Sequence of actual values

    Returns:
        float | None: The score
        Returns None in case of incorrect input types or mismatched length.
        In case of empty inputs, returns 0.0.
    """

    if not isinstance(predicted, (tuple, list)) or not isinstance(actual, (tuple, list)):
        return None
    if len(actual) != len(predicted):
        return None
    if not actual:
        return 0.0
    if (
        not all(
            isinstance(num, (int,float))
            and not isinstance(num, bool)
            for num in actual
            )
        or not all(
            isinstance(num, (int, float))
            and not isinstance(num, bool)
            for num in predicted
            )
        ):
        return None

    squares = [(a - p) ** 2 for a, p in zip(actual, predicted)]

    return float(sum(squares) / len(actual))

def compare_profiles_by_mse(
    unknown_profile: ProfileType, profile_to_compare: ProfileType
) -> float | None:
    """
    Compares two language profiles using the MSE metric.

    Args:
        unknown_profile (ProfileType): Unknown profile
        profile_to_compare (ProfileType): Profile
            to compare the unknown profile with

    Returns:
        float | None: The distance between the profiles.
        In case of corrupt input arguments or invalid profile structure, None is returned.
    """
    if not check_profile(unknown_profile) or not check_profile(profile_to_compare):
        return None

    freq_unk = unknown_profile[1]
    freq_profile_to_compare = profile_to_compare[1]

    all_words = set(freq_unk.keys()) | set(freq_profile_to_compare.keys())

    actual = []
    predicted = []

    for word in all_words:
        actual.append(freq_unk.get(word, 0.0))
        predicted.append(freq_profile_to_compare.get(word, 0.0))

    return calculate_mse(predicted, actual)

def detect_language_by_mse(
    unknown_profile: ProfileType, profile_1: ProfileType, profile_2: ProfileType
) -> str | None:
    """
    Detects the language of an unknown profile.

    Args:
        unknown_profile (ProfileType): Profile
            to determine the language of
        profile_1 (ProfileType): Known profile
        profile_2 (ProfileType): Another known profile

    Returns:
        str | None: Unknown profile language.
        Returns None in case of incorrect input types.
    """
    if (
        not check_profile(unknown_profile)
        or not check_profile(profile_1)
        or not check_profile(profile_2)
    ):
        return None

    unk_1_mse = compare_profiles_by_mse(unknown_profile, profile_1)
    if unk_1_mse is None:
        return None
    unk_2_mse = compare_profiles_by_mse(unknown_profile, profile_2)
    if unk_2_mse is None:
        return None

    if unk_1_mse < unk_2_mse:
        return profile_1[0]
    if unk_1_mse > unk_2_mse:
        return profile_2[0]

    return min(profile_1[0], profile_2[0])


# Mark 10


def save_profile(profile: ProfileType, save_path: str) -> bool:
    """
    Saves a language profile

    Args:
        profile (ProfileType): Profile
        save_path (str): Path to the folder to save profile

    Returns:
        bool: False in case of incorrect input types or if the profile
        is missing obligatory keys. True if the profile is saved.
    """
    if not check_profile(profile) or not isinstance(save_path, str):
        return False

    profile_dict = {
        "name": profile[0],
        "freq": profile[1],
        "n_words": profile[2]
    }

    with open(f"{save_path}/{profile[0]}.json", "w", encoding="utf-8") as file:
        file.write(json.dumps(profile_dict, indent=4, ensure_ascii=False))

    return True

def load_profile(path_to_file: str) -> ProfileType | None:
    """
    Loads a language profile.

    Args:
        path_to_file (str): Path to the language profile

    Returns:
        ProfileType | None: Loaded profile.
        Returns None in case of incorrect input types.
    """


def collect_profiles(paths_to_profiles: Sequence[str]) -> Sequence[ProfileType] | None:
    """
    Collects profiles for a given path.

    Args:
        paths_to_profiles (Sequence[str]): Sequence of paths to the profiles

    Returns:
        Sequence[ProfileType] | None: Sequence of loaded profiles.
        Returns None in case of incorrect input types.
    """


def detect_language_advanced(
    unknown_profile: ProfileType, known_profiles: Sequence[ProfileType], top_n: int
) -> Sequence[tuple[str, dict[str, float]]] | None:
    """
    Detects the language of an unknown profile.

    Args:
        unknown_profile (ProfileType): Profile
            to determine the language of
        known_profiles (Sequence[ProfileType]): Known profiles
        top_n (int): Number of popular words

    Returns:
        Sequence[tuple[str, dict[str, float]]] | None: Sorted sequence of tuples
        containing a language and a distance via both metrics.
        The sequence is sorted by best MSE value, then by best Top-N value.
        Returns None in case of incorrect input types.
    """


def print_report(
    unknown_profile: ProfileType, metrics_stats: Sequence[tuple[str, dict[str, float]]], top_n: int
) -> None:
    """
    Prints report for detection of language.

    Args:
        unknown_profile (ProfileType): Profile
        metrics_stats (Sequence[tuple[str, dict[str, float]]]): Sequence with distances for
            available language comparison and metrics
        top_n (int): Number of popular words

    In case of incorrect type inputs, does not print anything.
    """
