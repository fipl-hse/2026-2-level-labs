"""
Lab 1.

Language detection
"""

import json
import os

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
        elif char.isspace() and current_token:
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

    if not isinstance(tokens, (list, tuple)) or not all(
        isinstance(token, str) for token in tokens
    ):
        return None
    if not isinstance(stop_words, (list, tuple)) or not all(
        isinstance(word, str) for word in stop_words
    ):
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
        freq_dict[token] = freq_dict.get(token, 0) + 1 / total

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

    if (
        not isinstance(language, str)
        or not isinstance(text, str)
        or not isinstance(stop_words, (list, tuple))
    ):
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

    if not isinstance(top_n, int) or top_n <= 0:
        return None
    if not check_profile(unknown_profile) or not check_profile(profile_to_compare):
        return None

    unknown_top = get_top_n_words(unknown_profile[1], top_n)
    compare_top = get_top_n_words(profile_to_compare[1], top_n)
    if unknown_top is None or compare_top is None:
        return None

    unknown_set = set(unknown_top)
    compare_set = set(compare_top)
    intersection = unknown_set & compare_set
    return len(intersection) / len(unknown_set) if unknown_set else 0.0


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
    if not isinstance(top_n, int) or top_n <= 0:
        return None

    score_1 = compare_profiles_by_top_n(unknown_profile, profile_1, top_n)
    score_2 = compare_profiles_by_top_n(unknown_profile, profile_2, top_n)
    if score_1 is None or score_2 is None:
        return None

    return sorted(
        [(score_1, profile_1[0]), (score_2, profile_2[0])],
        key=lambda item: (-item[0], item[1]),
    )[0][1]

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

    if not check_profile(unknown_profile) or not check_profile(profile_to_compare):
        return None

    unknown_freq = unknown_profile[1]
    compare_freq = profile_to_compare[1]
    all_tokens = set(unknown_freq) | set(compare_freq)

    unknown_values = [unknown_freq.get(token, 0.0) for token in all_tokens]
    compare_values = [compare_freq.get(token, 0.0) for token in all_tokens]

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

    lang_1, lang_2 = profile_1[0], profile_2[0]
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

    if not check_profile(profile):
        return False
    if not isinstance(save_path, str):
        return False

    language = profile[0]
    freq_dict = profile[1]
    n_words = profile[2]

    profile_dict = {
        "name": language,
        "freq": freq_dict,
        "n_words": n_words,
    }

    try:
        os.makedirs(save_path, exist_ok=True)
        file_path = os.path.join(save_path, f"{language}.json")
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(profile_dict, file, ensure_ascii=False, indent=4)
    except (OSError, TypeError, ValueError):
        return False

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

    if not isinstance(path_to_file, str):
        return None

    try:
        with open(path_to_file, "r", encoding="utf-8") as file:
            data = json.load(file)
    except (OSError, ValueError):
        return None

    if not isinstance(data, dict) or set(data.keys()) != {"name", "freq", "n_words"}:
        return None

    name = data["name"]
    freq = data["freq"]
    n_words = data["n_words"]

    if not isinstance(name, str) or not isinstance(freq, dict):
        return None
    if not isinstance(n_words, int):
        return None

    profile = (name, freq, n_words)
    return profile if check_profile(profile) else None


def collect_profiles(paths_to_profiles: Sequence[str]) -> Sequence[ProfileType] | None:
    """
    Collects profiles for a given path.

    Args:
        paths_to_profiles (Sequence[str]): Sequence of paths to the profiles

    Returns:
        Sequence[ProfileType] | None: Sequence of loaded profiles.
        Returns None in case of incorrect input types.
    """

    if not isinstance(paths_to_profiles, (list, tuple)):
        return None

    profiles = []
    for path in paths_to_profiles:
        if not isinstance(path, str):
            return None
        profile = load_profile(path)
        if profile is not None:
            profiles.append(profile)

    return profiles


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

    if (
        not check_profile(unknown_profile)
        or not isinstance(known_profiles, (list, tuple))
        or not isinstance(top_n, int)
        or top_n <= 0
    ):
        return None

    results = []
    for profile in known_profiles:
        if not check_profile(profile):
            return None

        mse = compare_profiles_by_mse(unknown_profile, profile)
        top_n_score = compare_profiles_by_top_n(unknown_profile, profile, top_n)
        if mse is None or top_n_score is None:
            return None

        results.append((profile[0], {"MSE": mse, "Top-N": top_n_score}))

    results.sort(key=lambda item: (item[1]["MSE"], -item[1]["Top-N"], item[0]))
    return results


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

    if not check_profile(unknown_profile) or not isinstance(metrics_stats, (list, tuple)):
        return
    if not isinstance(top_n, int) or top_n <= 0:
        return

    for item in metrics_stats:
        if not isinstance(item, tuple) or len(item) != 2:
            return
        if not isinstance(item[0], str) or not isinstance(item[1], dict):
            return
        if "MSE" not in item[1] or "Top-N" not in item[1]:
            return

    freq_dict = unknown_profile[1]
    top_words = get_top_n_words(freq_dict, top_n)
    if top_words is None:
        return

    tokens = list(freq_dict.keys())
    if tokens:
        max_word = max(tokens, key=len)
        min_word = min(tokens, key=len)
        avg_length = sum(len(token) for token in tokens) / len(tokens)
    else:
        max_word = ""
        min_word = ""
        avg_length = 0.0

    print("Unknown language stats")
    print("======================")
    print(f"Popular words: {sorted(top_words)}")
    print(f"Max length word: '{max_word}'")
    print(f"Min length word: '{min_word}'")
    print(f"Average token length: {avg_length:.5f}")
    print()
    print("Language scores")
    print("---------------")

    for language, scores in sorted(
        metrics_stats, key=lambda item: (item[1]["MSE"], -item[1]["Top-N"], item[0])
    ):
        print(f"{language}: MSE {scores['MSE']:.5f}  Top-N Score {scores['Top-N']:.5f}")
