"""
Lab 1.

Language detection
"""

# pylint:disable=unused-argument
import json
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

    for char in text:
        if not (char.isalpha()) and char != " ":
            text = text.replace(char, "")

    return text.split()


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
    if not isinstance(tokens, Sequence) or not isinstance(stop_words, Sequence):
        return None

    if not all(isinstance(token, str) for token in tokens):
        return None

    if not all(isinstance(stop_word, str) for stop_word in stop_words):
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

    if not isinstance(tokens, Sequence):
        return None

    if not all(isinstance(token, str) for token in tokens):
        return None

    freq_dict = {}
    for token in set(tokens):
        freq_dict[token] = tokens.count(token) / len(tokens)

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

    if not isinstance(freq_dict, dict) or not isinstance(top_n, int) or top_n <= 0:
        return None

    if not all(isinstance(k, str) and isinstance(v, float) for k, v in freq_dict.items()):
        return None

    sorted_dict = dict(
        sorted(freq_dict.items(), key=lambda item: (-item[1], item[0])))

    top_n_words = list(sorted_dict.keys())[:top_n]

    return top_n_words
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
        or not isinstance(stop_words, Sequence)
    ):
        return None

    if not all(isinstance(stop_word, str) for stop_word in stop_words):
        return None

    tokens = tokenize(text)
    if not tokens:
        return None

    cleared_tokens = remove_stop_words(tokens, stop_words)
    if not cleared_tokens:
        return None

    freq_dict = calculate_frequencies(cleared_tokens)
    if not freq_dict:
        return None

    return language, freq_dict, len(freq_dict)


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

    language, freq_dict, length = profile

    if (
        not isinstance(language, str)
        or not isinstance(freq_dict, dict)
        or not isinstance(length, int)
    ):
        return False

    if not all(isinstance(k, str) and isinstance(v, float) for k, v in freq_dict.items()):
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

    if (
        not check_profile(unknown_profile)
        or not check_profile(profile_to_compare)
        or not isinstance(top_n, int)
    ):
        return None

    unknown_top_most_common = get_top_n_words(unknown_profile[1], top_n)
    to_compare_top_most_common = get_top_n_words(profile_to_compare[1], top_n)

    if not to_compare_top_most_common or not unknown_top_most_common:
        return None

    return len(set(unknown_top_most_common) & set(to_compare_top_most_common)) / top_n


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
        not isinstance(top_n, int)
        or not check_profile(unknown_profile)
        or not check_profile(profile_1)
        or not check_profile(profile_2)
    ):
        return None

    lang_1_probability = compare_profiles_by_top_n(
        unknown_profile, profile_1, top_n)
    if lang_1_probability is None:
        return None

    lang_2_probability = compare_profiles_by_top_n(
        unknown_profile, profile_2, top_n)
    if lang_2_probability is None:
        return None

    if lang_1_probability > lang_2_probability:
        return profile_1[0]
    if lang_1_probability < lang_2_probability:
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

    if not isinstance(predicted, Sequence) or not isinstance(actual, Sequence):
        return None
    if (not all(isinstance(el, float) for el in predicted)
            or not all(isinstance(el,  float) for el in actual)):
        return None
    if not predicted or not actual:
        return 0.0
    if len(predicted) != len(actual):
        return None

    return sum(
        (predicted[i] - actual[i]) ** 2 for i in range(len(predicted))
    ) / len(predicted)


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

    union_tokens = (set(unknown_profile[1].keys()) |
                    set(profile_to_compare[1].keys()))
    tokens_freq_unknown = []
    tokens_freq_to_compare = []

    for token in union_tokens:
        tokens_freq_unknown.append(unknown_profile[1].get(token, 0.0))
        tokens_freq_to_compare.append(profile_to_compare[1].get(token, 0.0))

    return calculate_mse(tokens_freq_unknown, tokens_freq_to_compare)


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

    if not check_profile(profile) or not isinstance(save_path, str):
        return False

    to_write = {
        "name": profile[0],
        "freq": profile[1],
        "n_words": profile[2]
    }
    path = f"{save_path}/{profile[0]}.json"
    with open(path, 'w', encoding='utf-8') as file:
        file.write(json.dumps(to_write, ensure_ascii=False, indent=4))

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

    with open(path_to_file, encoding="utf-8") as file:
        read_data = json.load(file)

    if not isinstance(read_data, dict):
        return None

    if list(read_data.keys()) != ["name", "freq", "n_words"]:
        return None

    if check_profile((read_data["name"], read_data["freq"], read_data["n_words"])):
        return read_data["name"], read_data["freq"], read_data["n_words"]

    return None


def collect_profiles(paths_to_profiles: Sequence[str]) -> Sequence[ProfileType] | None:
    """
    Collects profiles for a given path.

    Args:
        paths_to_profiles (Sequence[str]): Sequence of paths to the profiles

    Returns:
        Sequence[ProfileType] | None: Sequence of loaded profiles.
        Returns None in case of incorrect input types.
    """
    if not isinstance(paths_to_profiles, Sequence):
        return None

    if not all(isinstance(path, str) for path in paths_to_profiles):
        return None

    profiles = []
    for path in paths_to_profiles:
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
        or not isinstance(known_profiles, Sequence)
        or not isinstance(top_n, int)
        or top_n <= 0
    ):
        return None

    if not all(check_profile(profile) for profile in known_profiles):
        return None

    res = []
    for known_profile in known_profiles:
        mse_compare = compare_profiles_by_mse(unknown_profile, known_profile)
        top_n_compare = compare_profiles_by_top_n(
            unknown_profile, known_profile, top_n)

        if mse_compare is None or top_n_compare is None:
            return None

        metrics = {
            "MSE": mse_compare,
            "Top-N": top_n_compare
        }
        res.append((known_profile[0], metrics))

    return sorted(res, key=lambda el: (el[1]["MSE"], -el[1]["Top-N"]))


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

    if (
        not check_profile(unknown_profile)
        or not isinstance(metrics_stats, Sequence)
        or not isinstance(top_n, int)
    ):
        return

    if not all(isinstance(el, tuple)
               and len(el) == 2
               and isinstance(el[0], str)
               and isinstance(el[1], dict)
               and all(
            isinstance(k, str) and isinstance(v, float)
            for k, v in el[1].items()
    )
        for el in metrics_stats
    ):
        return

    print("Unknown language stats")
    print("======================")
    print(f"Popular words: {get_top_n_words(unknown_profile[1], top_n)}")
    print(f"Max length word: '{max(unknown_profile[1].keys(), key=len)}'")
    print(f"Min length word: '{min(unknown_profile[1].keys(), key=len)}'")
    print(f"Average token length: {sum(len(s) for s in unknown_profile[1].keys())
                                   / len(unknown_profile[1].keys())
                                   if unknown_profile[1].keys() else 0:.5f}")
    print()
    print("Language scores")
    print("---------------")
    for el in metrics_stats:
        print(
            f'{el[0]}: MSE {el[1]["MSE"]:.5f}  Top-N Score {el[1]["Top-N"]:.5f}')
