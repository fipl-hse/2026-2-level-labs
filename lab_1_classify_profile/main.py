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

    processed_tokens = []
    unprocessed_tokens = text.split()
    for word in unprocessed_tokens:
        alpha_symbols = []
        for symbol in word:
            if symbol.isalpha():
                alpha_symbols.append(symbol)
        joined_word = "".join(alpha_symbols).lower()
        if joined_word:
            processed_tokens.append(joined_word)
    return processed_tokens


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
    if (not isinstance(tokens, list)
    or not isinstance(stop_words, list)
    or not all(isinstance(token, str) for token in tokens)
    or not all(isinstance(word, str) for word in stop_words)
    ):
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
    if ( not isinstance(tokens, list)
    or not all(isinstance(token, str) for token in tokens)
    ):
        return None

    tokens_quantity = {}
    tokens_frequency = {}
    for token in tokens:
        if token not in tokens_quantity:
            tokens_quantity[token] = 1
        else:
            tokens_quantity[token] += 1
    if not tokens:
        return tokens_frequency
    for token, quantity in tokens_quantity.items():
        frequency = quantity / len(tokens)
        tokens_frequency[token] = frequency
    return tokens_frequency


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
    or not all(isinstance(value, float) for value in freq_dict.values())
    or not isinstance(top_n, int)
    ):
        return None

    if top_n <= 0:
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
    if (
    not isinstance(language, str)
    or not isinstance(text, str)
    or not isinstance (stop_words, list)
    or not all(isinstance(word, str) for word in stop_words)
    ):
        return None

    processed_tokens = tokenize(text)
    if processed_tokens is None:
        return None
    tokens = remove_stop_words(processed_tokens, stop_words)
    if tokens is None:
        return None
    freq_dict = calculate_frequencies(tokens)
    if freq_dict is None:
        return None

    return (language, freq_dict, len(freq_dict))


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

    if not isinstance(profile[0], str):
        return False

    if (not isinstance(profile[1], dict)
    or not all(isinstance(key, str) for key in profile[1])
    or not all(isinstance(value, float) for value in profile[1].values())
    ):
        return False
    if not isinstance(profile[2], int):
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
    checked_unknown_profile = check_profile(unknown_profile)
    checked_profile_to_compare = check_profile(profile_to_compare)

    if (not isinstance(top_n, int)
    or top_n <= 0
    or not checked_unknown_profile
    or not checked_profile_to_compare
    ):
        return None

    top_unknown_profile = get_top_n_words(unknown_profile[1], top_n)
    top_profile_to_compare = get_top_n_words(profile_to_compare[1], top_n)
    if (
        top_unknown_profile is None
        or top_profile_to_compare is None
    ):
        return None

    intersecting_top_words = []
    for top_word in top_unknown_profile:
        if top_word in top_profile_to_compare:
            intersecting_top_words.append(top_word)
    profile_comparison = len(intersecting_top_words) / len(top_unknown_profile)
    return profile_comparison


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
    checked_unknown_profile = check_profile(unknown_profile)
    checked_profile_1 = check_profile(profile_1)
    checked_profile_2 = check_profile(profile_2)

    if (not isinstance(top_n, int)
        or top_n <= 0
        or not checked_unknown_profile
        or not checked_profile_1
        or not checked_profile_2
        ):
        return None

    comparison_with_profile_1 = compare_profiles_by_top_n(unknown_profile, profile_1, top_n)
    comparison_with_profile_2 = compare_profiles_by_top_n(unknown_profile, profile_2, top_n)

    if(comparison_with_profile_1 is None
    or comparison_with_profile_2 is None
    ):
        return None

    if comparison_with_profile_1 > comparison_with_profile_2:
        return profile_1[0]
    if comparison_with_profile_1 < comparison_with_profile_2:
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
    not isinstance(predicted, list)
    or not all(isinstance(predicted_num, float) for predicted_num in predicted)
     or not isinstance(actual, list)
     or not all(isinstance(actual_num, float) for actual_num in actual)
    ):
        return None

    if len(predicted) != len(actual):
        return None

    if len(predicted) == 0:
        return 0.0

    squared_difference_sum = 0.0
    for i, predicted_value in enumerate(predicted):
        actual_value = actual[i]
        squared_difference_sum += (predicted_value - actual_value) ** 2
    mse = squared_difference_sum / len(predicted)
    return mse


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
    checked_unknown_profile = check_profile(unknown_profile)
    checked_profile_to_compare = check_profile(profile_to_compare)
    if (not checked_unknown_profile
    or not checked_profile_to_compare
    ):
        return None

    freq_dict_unknown = unknown_profile[1]
    freq_dict_to_compare = profile_to_compare[1]

    all_tokens = []
    for token in freq_dict_unknown:
        all_tokens.append(token)
    for token in freq_dict_to_compare:
        if token not in all_tokens:
            all_tokens.append(token)

    predicted = []
    actual = []
    for token in all_tokens:
        predicted.append(freq_dict_unknown.get(token, 0.0))
        actual.append(freq_dict_to_compare.get(token, 0.0))

    mse = calculate_mse(predicted, actual)
    return mse

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
    checked_unknown_profile = check_profile(unknown_profile)
    checked_profile_1 = check_profile(profile_1)
    checked_profile_2 = check_profile(profile_2)

    if (not checked_unknown_profile
    or not checked_profile_1
    or not checked_profile_2
    ):
        return None

    mse_1 = compare_profiles_by_mse(unknown_profile, profile_1)
    mse_2 = compare_profiles_by_mse(unknown_profile, profile_2)

    if mse_1 is None or mse_2 is None:
        return None

    if mse_1 < mse_2:
        return profile_1[0]
    if mse_1 > mse_2:
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
