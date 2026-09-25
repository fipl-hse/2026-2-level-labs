"""
Lab 1.

Language detection
"""

# pylint:disable=unused-argument

import string
from typing import Sequence

FreqDictType = dict[str, float]
"Frequency dictionary. Contains pairs of token and its frequency."
ProfileType = tuple[str, FreqDictType, int]
"Language profile of a text. Contains language name, frequency dictionary and number of tokens."
# Mark 4.


def tokenize(text: str) -> Sequence[str] | None:
    if not isinstance(text, str):
        return None
    punctuation = string.punctuation
    text = text.lower()
    for sym in punctuation:
        text = text.replace(sym, '')
    return [token for token in text.split() if token]

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
    if not isinstance(stop_words, list) or not isinstance(tokens, list):
        return None
    if not all(isinstance(token, str) for token in tokens):
        return None

    if not all(isinstance(word, str) for word in stop_words):
        return None

    for stop_word in stop_words:
        while stop_word in tokens:
            tokens.remove(stop_word)
    return tokens

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
    if not isinstance(tokens,list):
        return None
    for token in tokens:
        if not isinstance(token, str):
            return None
    freq_dict = {}
    for token in set(tokens):
        freq_dict[token] = tokens.count(token) / len(tokens)
    return freq_dict
    """
    Calculates frequencies of given tokens

    Args:
        tokens (Sequence[str]): Sequence of tokens
    Returns:
        dict[str, float] | None: Dictionary with frequencies.
        Returns None in case of incorrect input types.
    """


def get_top_n_words(freq_dict: dict[str, float], top_n: int) -> Sequence[str] | None:
    if not isinstance(freq_dict,dict) or not isinstance(top_n,int):
        return None
    if top_n <= 0:
        return None

    sort_tokens = sorted(freq_dict)
    sort_tokens = sorted(sort_tokens, key = freq_dict.get, reverse = True)
    return sort_tokens[:top_n]

    """
    Finds the most common words

    Args:
        freq_dict (dict[str, float]): Dictionary with frequencies
        top_n (int): Number of the most common words

    Returns:
        Sequence[str] | None: Sequence of the most common words.
        Returns None in case of incorrect input types or non-positive top_n.
    """


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

    tokens = tokenize(text)
    cl_tokens = remove_stop_words(tokens, stop_words)
    freq_dict = calculate_frequencies(cl_tokens)

    if not isinstance(stop_words, list) or not isinstance(text, str) or not isinstance(language,str):
        return None

    for word in stop_words:
        if not isinstance(word, str):
            return None

    if freq_dict is None:
        return None

    if cl_tokens is None:
        return None

    language_profile = (language, freq_dict, len(freq_dict))
    return language_profile


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
    if not isinstance(profile, tuple) or len(profile) != 3:
        return False


    if not isinstance(profile[0], str):
        return False
    if not isinstance(profile[1], dict):
        return False
    if not isinstance(profile[2], int) :
        return False
    for key, value in profile[1].items():
        if not isinstance(key, str):
            return False
        if not isinstance(value, float):
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
    if not check_profile(unknown_profile)  or not check_profile(profile_to_compare) or not isinstance(top_n,int) :
        return None
    unknown_profile_top_n = get_top_n_words(unknown_profile[1], top_n)
    if unknown_profile_top_n is None:
        return None

    compare_profile_top_n = get_top_n_words(profile_to_compare[1], top_n)
    if compare_profile_top_n is None:
        return None

    intersect = 0
    for word in unknown_profile_top_n:
        if word in compare_profile_top_n :
            intersect += 1
    intersection = intersect/ top_n

    return intersection


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
    if not check_profile(unknown_profile)  or not check_profile(profile_1) or not check_profile(profile_2) or not isinstance(top_n,int):
            return None
    sim1 = compare_profiles_by_top_n(unknown_profile, profile_1, top_n)
    sim2 = compare_profiles_by_top_n(unknown_profile, profile_2, top_n)
    if sim1 is None or sim2 is None:
        return None
    if sim1>sim2:
        return profile_1[0]
    if sim2>sim1:
        return profile_2[0]
    if sim1==sim2:
        return min(profile_1[0], profile_2[0])
    else:
        return None


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
