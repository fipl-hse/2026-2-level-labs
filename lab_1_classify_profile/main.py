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

    text = text.lower()
    tokens = []
    current_token = ""

    for char in text:
        if char.isalpha():
            current_token += char
        elif char.isspace():
            if current_token:
                tokens.append(current_token)
                current_token = ""

    if current_token:
        tokens.append(current_token)

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

    if not isinstance(tokens, (list, tuple)):
        return None

    if not all(isinstance(token, str) for token in tokens):
        return None

    if not isinstance(stop_words, (list, tuple)):
        return None

    if not all(isinstance(word, str) for word in stop_words):
        return None

    return [token for token in tokens if token not in stop_words]


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

    if not all(isinstance(token, str) for token in tokens):
        return None

    if not tokens:
        return {}

    freq_dict = {}
    total = len(tokens)

    for token in tokens:
        freq_dict[token] = freq_dict.get(token, 0) + 1

    for key in freq_dict:
        freq_dict[key] = freq_dict[key] / total

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
    if not isinstance(top_n, int) or top_n <= 0:
        return None

    sorted_words = sorted(freq_dict.items(), key=lambda x: (-x[1], x[0]))
    result = [word for word, _ in sorted_words[:top_n]]

    return result


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

    tokens = tokenize(text)
    if tokens is None:
        return None

    tokens_no_stop = remove_stop_words(tokens, stop_words)
    if tokens_no_stop is None:
        return None

    freq_dict = calculate_frequencies(tokens_no_stop)
    if freq_dict is None:
        return None

    n_words = len(freq_dict)
    return (language, freq_dict, n_words)

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

    language, freq_dict, n_words = profile

    if not isinstance(language, str) or not isinstance(freq_dict, dict):
        return False

    if not isinstance(n_words, int) or isinstance(n_words, bool) or n_words < 0:
        return False

    for key, value in freq_dict.items():
        if not isinstance(key, str):
            return False
        if not isinstance(value, (int, float)) or isinstance(value, bool):
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

    if not check_profile(unknown_profile) or not check_profile(profile_to_compare):
        return None
    if not isinstance(top_n, int) or top_n <= 0:
        return None

    unknown_freq = unknown_profile[1]
    compare_freq = profile_to_compare[1]

    unknown_top = get_top_n_words(unknown_freq, top_n)
    compare_top = get_top_n_words(compare_freq, top_n)

    if unknown_top is None or compare_top is None:
        return None

    unknown_set = set(unknown_top)
    compare_set = set(compare_top)

    intersection = unknown_set & compare_set
    result = len(intersection) / len(unknown_set) if unknown_set else 0.0

    return result

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
    if not isinstance(top_n, int) or top_n <= 0:
        return None

    score_1 = compare_profiles_by_top_n(unknown_profile, profile_1, top_n)
    score_2 = compare_profiles_by_top_n(unknown_profile, profile_2, top_n)

    if score_1 is None or score_2 is None:
        return None

    lang_1 = profile_1[0]
    lang_2 = profile_2[0]

    if score_1 > score_2:
        return lang_1
    if score_2 > score_1:
        return lang_2
    return min(lang_1, lang_2)

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

    if not isinstance(predicted, (list, tuple)) or not isinstance(actual, (list, tuple)):
        return None
    if len(predicted) != len(actual):
        return None
    if not all(isinstance(value, (int, float)) for value in predicted):
        return None
    if not all(isinstance(value, (int, float)) for value in actual):
        return None
    if not predicted:
        return 0.0

    squared_sum = 0.0
    for predicted_value, actual_value in zip(predicted, actual):
        squared_sum += (predicted_value - actual_value) ** 2

    return squared_sum / len(predicted)


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

    if not check_profile(unknown_profile):
        return None
    if not check_profile(profile_to_compare):
        return None

    unknown_freq = unknown_profile[1]
    compare_freq = profile_to_compare[1]

    all_tokens = set(unknown_freq.keys()) | set(compare_freq.keys())

    unknown_values = []
    compare_values = []
    for token in all_tokens:
        unknown_values.append(unknown_freq.get(token, 0.0))
        compare_values.append(compare_freq.get(token, 0.0))

    return calculate_mse(unknown_values, compare_values)


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

    if not check_profile(unknown_profile):
        return None
    if not check_profile(profile_1):
        return None
    if not check_profile(profile_2):
        return None

    mse_1 = compare_profiles_by_mse(unknown_profile, profile_1)
    mse_2 = compare_profiles_by_mse(unknown_profile, profile_2)

    if mse_1 is None or mse_2 is None:
        return None

    lang_1 = profile_1[0]
    lang_2 = profile_2[0]

    if mse_1 < mse_2:
        return lang_1
    if mse_2 < mse_1:
        return lang_2
    return min(lang_1, lang_2)

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
