"""
Lab 1.

Language detection
"""

# pylint:disable=unused-argument
from typing import Sequence

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
    tokens = []
    for word in text.split():
        clean_word = "".join(letter for letter in word if letter.isalpha())
        if clean_word:
            tokens.append(clean_word.lower())
    return tokens


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
    if tokens is None or not isinstance(tokens, (list, tuple, str)):
        return None
    if not isinstance(stop_words, (list, tuple, str)):
        return None
    if not all(isinstance(token, str) for token in tokens):
        return None
    if not all(isinstance(word, str) for word in stop_words):
        return None
    if not stop_words:
        return tokens
    result = []
    for token in tokens:
        if token not in stop_words:
            result.append(token)
    return result


def calculate_frequencies(tokens: Sequence[str]) -> dict[str, float] | None:
    """
    Calculates frequencies of given tokens

    Args:
        tokens (Sequence[str]): Sequence of tokens
    Returns:
        dict[str, float] | None: Dictionary with frequencies.
        Returns None in case of incorrect input types.
    """
    if tokens is None or not isinstance(tokens, (list, tuple, str)):
        return None
    if not all(isinstance(token, str) for token in tokens):
        return None
    if not tokens:
        return {}
    total = len(tokens)
    freq: dict [str, float] = {}
    for token in tokens:
        if token not in freq:
            freq[token] = 0.0
        freq[token] += 1.0
    for token in freq:
        freq[token] = freq[token] / total
    return freq


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
    if (
        not isinstance(freq_dict, dict)
        or not all(isinstance(key, str) for key in freq_dict)
        or not all(isinstance(value, (int, float)) for value in freq_dict.values())
        or not isinstance(top_n, int)
        or top_n <= 0
    ):
        return None
    if not freq_dict:
        return []
    words = list(freq_dict.keys())
    words.sort(key=lambda w: (-freq_dict[w], w))
    return words[:top_n]

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
    if (
        not isinstance(language, str)
        or not isinstance(text, str)
        or not isinstance(stop_words, (list, tuple, str))
        or not all(isinstance(word, str) for word in stop_words)
    ):
        return None

    tokens = tokenize(text)
    if tokens is None:
        return None
    clean_tokens = remove_stop_words(tokens, stop_words)
    if clean_tokens is None:
        return None
    freq = calculate_frequencies(clean_tokens)
    if freq is None:
        return None
    return language, freq, len(freq)


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
    name, freq, n_words = profile
    return (
        isinstance(name, str)
        and isinstance(freq, dict)
        and not isinstance(n_words, bool)
        and isinstance(n_words, int)
        and all(isinstance(key, str) for key in freq)
        and all(isinstance(value, float) for value in freq.values())
    )


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
    if not check_profile(unknown_profile) or not check_profile(profile_to_compare):
        return None
    if not isinstance(top_n, int) or top_n <= 0:
        return None
    unknown_top = get_top_n_words(unknown_profile[1], top_n)
    compare_top = get_top_n_words(profile_to_compare[1], top_n)
    if unknown_top is None or compare_top is None:
        return None
    if not unknown_top:
        return 0.0

    common = len(set(unknown_top) & set(compare_top))
    return common / len(unknown_top)


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
    if (
        not check_profile(unknown_profile)
        or not check_profile(profile_1)
        or not check_profile(profile_2)
    ):
        return None

    score_1 = compare_profiles_by_top_n(unknown_profile, profile_1, top_n)
    score_2 = compare_profiles_by_top_n(unknown_profile, profile_2, top_n)

    if score_1 is None or score_2 is None:
        return None

    if score_1 > score_2:
        return profile_1[0]
    if score_2 > score_1:
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
    if (
        not isinstance(predicted, (list, tuple))
        or not isinstance(actual, (list, tuple))
        or len(predicted) != len(actual)
    ):
        return None
    if not predicted and not actual:
        return 0.0

    total = 0.0
    for p, y in zip(predicted, actual):
        if not isinstance(p, (int, float)) or isinstance(p, bool):
            return None
        if not isinstance(y, (int, float)) or isinstance(y, bool):
            return None
        total += (y - p) ** 2

    return total / len(predicted)


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

    freq_1 = unknown_profile[1]
    freq_2 = profile_to_compare[1]

    tokens_1 = list(freq_1.keys())
    tokens_2 = list(freq_2.keys())

    all_tokens = list(set(tokens_1 + tokens_2))

    predicted = []
    actual = []

    for token in all_tokens:
        predicted.append(freq_1.get(token, 0.0))
        actual.append(freq_2.get(token, 0.0))
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

    mse_1 = compare_profiles_by_mse(unknown_profile, profile_1)
    mse_2 = compare_profiles_by_mse(unknown_profile, profile_2)

    if mse_1 is None or mse_2 is None:
        return None

    if mse_1 < mse_2:
        return profile_1[0]
    if mse_2 < mse_1:
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
    return False


def load_profile(path_to_file: str) -> ProfileType | None:
    """
    Loads a language profile.

    Args:
        path_to_file (str): Path to the language profile

    Returns:
        ProfileType | None: Loaded profile.
        Returns None in case of incorrect input types.
    """
    return ("", {}, 0)


def collect_profiles(paths_to_profiles: Sequence[str]) -> Sequence[ProfileType] | None:
    """
    Collects profiles for a given path.

    Args:
        paths_to_profiles (Sequence[str]): Sequence of paths to the profiles

    Returns:
        Sequence[ProfileType] | None: Sequence of loaded profiles.
        Returns None in case of incorrect input types.
    """
    return []


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
    return []


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
