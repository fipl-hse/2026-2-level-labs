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
    if not isinstance(text, str):
        return None
    import re
    words = text.split()
    word_list = []
    for word in words:
        delete_non_letters = re.sub(r"[^a-zA-Zа-яА-ЯёЁßäöüÄÖÜ]", '', word)
        if delete_non_letters:
            word_list.append(delete_non_letters.lower())
    return word_list
    """
    Splits a text into tokens, converts the tokens into lowercase,
    removes punctuation and other symbols from words

    Args:
       text (str): Text

    Returns:
        Sequence[str] | None: Sequence of lower-cased tokens without punctuation.
        Returns None if input text is not a string.
    """


def remove_stop_words(tokens: Sequence[str], stop_words: Sequence[str]) -> Sequence[str] | None:
    if not isinstance(tokens, (list, tuple)):
        return None
    for token in tokens:
        if not isinstance(token, str):
            return None
    if not isinstance(stop_words, (list, tuple)):
        return None
    for word in stop_words:
        if not isinstance(word, str):
            return None
    if not stop_words:
        return tokens
    stop_set = set(stop_words)
    return [token for token in tokens if token not in stop_set]
    """
    Removes stop words

    Args:
        tokens (Sequence[str]): Sequence of tokens
        stop_words (Sequence[str]): Sequence of stop words (can be empty)
    Returns:
        Sequence[str] | None: Sequence of tokens without stop words.
        Returns None in case of incorrect input types.
    """


def calculate_frequencies(tokens: Sequence[str]) -> dict[str, float] | None:
    """
    Calculates frequencies of given tokens

    Args:
        tokens (Sequence[str]): Sequence of tokens
    Returns:
        dict[str, float] | None: Dictionary with frequencies.
        Returns None in case of incorrect input types.
    """
    if not isinstance(tokens, (list, tuple)):
        return None
    if len(tokens) == 0:
        return {}
    for token in tokens:
        if not isinstance(token, str):
            return None

    total = len(tokens)
    freq_dict: dict[str, float] = {}
    for token in tokens:
        freq_dict[token] = freq_dict.get(token, 0) + 1

    for token in freq_dict:
        freq_dict[token] /= total
    return freq_dict


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
    if not isinstance(freq_dict, dict):
        return None
    if not isinstance(top_n, int) or isinstance(top_n, bool):
        return None
    if top_n <= 0:
        return None
    for key, value in freq_dict.items():
        if not isinstance(key, str) or not isinstance(value, (int, float)):
            return None
    sorted_words = sorted(freq_dict, key=lambda word: (-freq_dict[word], word))
    return sorted_words[:top_n]


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
    if not isinstance(text, str):
        return None
    if not isinstance(stop_words, (list, tuple)):
        return None
    for word in stop_words:
        if not isinstance(word, str):
            return None

    tokens = tokenize(text)
    if tokens is None:
        return None

    clean_tokens = remove_stop_words(tokens, stop_words)
    if clean_tokens is None:
        return None

    frequencies = calculate_frequencies(clean_tokens)
    if frequencies is None:
        return None

    n_words = len(frequencies)
    return (language, frequencies, n_words)



def check_profile(profile: ProfileType) -> bool:
    """
    Checks profile structure

    Args:
        profile (ProfileType): Profile to check

    Returns:
        bool: Returns True if the profile has right structure and types,
        otherwise returns False.
    """

    if not isinstance(profile, tuple):
        return False
    if len(profile) != 3:
        return False

    language, frequencies, n_words = profile

    if not isinstance(language, str):
        return False
    if not isinstance(frequencies, dict):
        return False
    for key, value in frequencies.items():
        if not isinstance(key, str):
            return False
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            return False

    if isinstance(n_words, bool) or not isinstance(n_words, int):
        return False
    if n_words < 0:
        return False
    if n_words != len(frequencies):
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
    if isinstance(top_n, bool) or not isinstance(top_n, int):
        return None
    if top_n <= 0:
        return None

    if not check_profile(unknown_profile):
        return None
    if not check_profile(profile_to_compare):
        return None

    unknown_freq = unknown_profile[1]
    compare_freq = profile_to_compare[1]
    unknown_top = get_top_n_words(unknown_freq, top_n)
    compare_top = get_top_n_words(compare_freq, top_n)

    if unknown_top is None or compare_top is None:
        return None
    if len(unknown_top) == 0:
        return None

    intersection = set(unknown_top) & set(compare_top)
    return len(intersection) / len(unknown_top)


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
    if not check_profile(unknown_profile):
        return None
    if not check_profile(profile_1):
        return None
    if not check_profile(profile_2):
        return None

    distance_1 = compare_profiles_by_top_n(unknown_profile, profile_1, top_n)
    distance_2 = compare_profiles_by_top_n(unknown_profile, profile_2, top_n)

    if distance_1 is None or distance_2 is None:
        return None

    language_1 = profile_1[0]
    language_2 = profile_2[0]

    if distance_1 > distance_2:
        return language_1
    if distance_2 > distance_1:
        return language_2
    return min(language_1, language_2)

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
