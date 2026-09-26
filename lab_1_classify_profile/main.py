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

    words = text.lower().split()
    tokens = []

    for word in words:
        token = ''
        for char in word:
            if char.isalpha():
                token += char
        if token:
            tokens.append(token)

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
    if not isinstance(tokens, Sequence) or isinstance(tokens, str):
        return None

    if not all(isinstance(token, str) for token in tokens):
        return None

    if not isinstance(stop_words, Sequence) or isinstance(stop_words, str):
        return None

    if not all(isinstance(word, str) for word in stop_words):
        return None

    tokens_without_stop_words = []

    for token in tokens:
        if token not in stop_words:
            tokens_without_stop_words.append(token)

    return tokens_without_stop_words


def calculate_frequencies(tokens: Sequence[str]) -> dict[str, float] | None:
    """
    Calculates frequencies of given tokens

    Args:
        tokens (Sequence[str]): Sequence of tokens
    Returns:
        dict[str, float] | None: Dictionary with frequencies.
        Returns None in case of incorrect input types.
    """
    if not isinstance(tokens, Sequence) or isinstance(tokens, str):
        return None

    if not all(isinstance(token, str) for token in tokens):
        return None

    length = len(tokens)

    if length == 0:
        return {}

    freq = {}

    for token in tokens:
        if token not in freq:
            freq[token] = 0.0
        freq[token] += 1.0 / length

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
    if not isinstance(top_n, int) or top_n <= 0:
        return None

    if not isinstance(freq_dict, dict):
        return None

    if not all(isinstance(key, str) for key in freq_dict):
        return None
    if not all(isinstance(value, float) for value in freq_dict.values()):
        return None

    sorted_words = sorted(freq_dict.keys(), key=lambda x: (-freq_dict[x], x))

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
    if not all([
        isinstance(language, str),
        isinstance(text, str),
        isinstance(stop_words, Sequence),
        not isinstance(stop_words, str)
    ]):
        return None

    if not all(isinstance(word, str) for word in stop_words):
        return None

    tokens = tokenize(text)
    if tokens is None:
        return None

    tokens = remove_stop_words(tokens, stop_words)
    if tokens is None:
        return None

    freq = calculate_frequencies(tokens)
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

    if (not isinstance(profile[0], str)
        or not isinstance(profile[1], dict)
        or not isinstance(profile[2], int)):
        return False

    freq = profile[1]

    for key, value in freq.items():
        if not all([isinstance(key, str), isinstance(value, float)]):
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


    if not all([check_profile(unknown_profile), check_profile(profile_to_compare)]):
        return None

    if not isinstance(top_n, int) or top_n <= 0:
        return None

    unknown_profile_top_n = get_top_n_words(unknown_profile[1], top_n)
    profile_to_compare_top_n = get_top_n_words(profile_to_compare[1], top_n)

    if unknown_profile_top_n is None or profile_to_compare_top_n is None:
        return None

    unknown_set = set(unknown_profile_top_n)
    language_set = set(profile_to_compare_top_n)
    intersaction = unknown_set & language_set

    return len(intersaction) / len(unknown_profile_top_n)


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
    if not all([check_profile(unknown_profile),
                       check_profile(profile_1),
                       check_profile(profile_2)]):
        return None

    if not isinstance(top_n, int) or top_n <= 0:
        return None

    lang_name_1 = profile_1[0]
    lang_name_2 = profile_2[0]

    score_1 = compare_profiles_by_top_n(unknown_profile,
                                        profile_1, top_n)
    score_2 = compare_profiles_by_top_n(unknown_profile,
                                        profile_2, top_n)

    if score_1 is None or score_2 is None:
        return None

    if score_1 > score_2:
        return lang_name_1
    if score_2 > score_1:
        return lang_name_2

    return sorted([lang_name_1, lang_name_2])[0]

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
    if not isinstance(predicted, Sequence) or not isinstance(actual, Sequence):
        return None
    if not all(isinstance(element, float) for element in predicted):
        return None
    if not all(isinstance(element, float) for element in actual):
        return None
    if len(predicted) != len(actual):
        return None
    if not predicted or not actual:
        return 0.0

    sum_squared = [(a - p) ** 2 for a, p in zip(actual, predicted)]

    return sum(sum_squared) / len(actual)


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

    lang_1 = unknown_profile[1]
    lang_2 = profile_to_compare[1]

    unknown_set = set(lang_1.keys())
    set_to_compare = set(lang_2.keys())
    conjunction = unknown_set | set_to_compare

    actual_list = []
    predicted_list = []

    for word in conjunction:
        val1 = lang_1.get(word, 0.0)
        val2 = lang_2.get(word, 0.0)

        actual_list.append(val1)
        predicted_list.append(val2)

    return calculate_mse(predicted_list, actual_list)

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
    if not all([check_profile(unknown_profile),
                    check_profile(profile_1),
                    check_profile(profile_2)]):
        return None

    lang_name_1 = profile_1[0]
    lang_name_2 = profile_2[0]

    score_1 = compare_profiles_by_mse(unknown_profile,
                                            profile_1)
    score_2 = compare_profiles_by_mse(unknown_profile,
                                            profile_2)

    if score_1 is None or score_2 is None:
        return None

    if score_1 > score_2:
        return lang_name_2
    if score_2 > score_1:
        return lang_name_1

    return sorted([lang_name_1, lang_name_2])[0]

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
