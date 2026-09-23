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
    tokens = [symbol for symbol in text if symbol.isalpha() or symbol.isspace()]
    tokens = "".join(tokens).split()
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
    if not isinstance (tokens, list):
        return None
    for token in tokens:
        if not isinstance (token, str):
            return None

    if not isinstance(stop_words, list):
        return None
    for word in stop_words:
        if not isinstance(word, str):
            return None

    tokens = [token for token in tokens if token not in stop_words]
    return tokens


def calculate_frequencies(tokens: Sequence[str]) -> dict[str, float] | None:
    """
    Calculates frequencies of given tokens

    Args:
        tokens (Sequence[str]): Sequence of tokens
    Returns:
        dict[str, float] | None: Dictionary with frequencies.
        Returns None in case of incorrect input types.
    """
    if not isinstance (tokens, list):
        return None
    for token in tokens:
        if not isinstance (token, str):
            return None

    freq_dict = {}
    for token in tokens:
        if token in freq_dict:
            freq_dict[token] += 1
        else:
            freq_dict[token] = 1

    for token in freq_dict:
        freq_dict[token] = freq_dict[token]/len(tokens)

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
    for key, value in freq_dict.items():
        if not (isinstance (key, str) and isinstance (value, float)):
            return None

    sort_freq_dct = sorted(freq_dict.items(), key = lambda freqs: freqs[0])
    sort_freq_dct = sorted(sort_freq_dct, key = lambda freqs: freqs[1], reverse = True)
    top_n_words = []

    top_n_words = [item[0] for item in sort_freq_dct]


    top_n_words = top_n_words[:top_n]

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
    if not (isinstance(language, str) and isinstance(text, str) and isinstance(stop_words, list)):
        return None

    for word in stop_words:
        if not isinstance(word, str):
            return None

    tokens = tokenize(text)
    if tokens is None:
        return None

    cleaned_tokens = remove_stop_words(tokens, stop_words)
    if cleaned_tokens is None:
        return None

    freq = calculate_frequencies(cleaned_tokens)
    if freq is None:
        return None

    profile = (language, freq, len(freq))

    return profile

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

    if not (isinstance(profile[0], str) and
    isinstance(profile[1], dict) and
    isinstance(profile[2], int)):
        return False

    for key, value in profile[1].items():
        if not (isinstance (key, str) and isinstance (value, float)):
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
    check_unknown = check_profile(unknown_profile)
    check_compare = check_profile(profile_to_compare)

    if not (check_unknown and check_compare):
        return None

    if not isinstance(top_n, int):
        return None

    top_n_unknown = get_top_n_words(unknown_profile[1], top_n)
    if top_n_unknown is None:
        return None
    top_n_compare = get_top_n_words(profile_to_compare[1], top_n)
    if top_n_compare is None:
        return None


    similarity = 0
    for word in top_n_unknown:
        for item in top_n_compare:
            if word == item:
                similarity +=1

    result = similarity/top_n
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
    if not (
        check_profile(unknown_profile) and
        check_profile(profile_1) and
        check_profile(profile_2) and
        isinstance(top_n, int)):
        return None

    compare_unknown_1 = compare_profiles_by_top_n(unknown_profile, profile_1, top_n)
    compare_unknown_2 = compare_profiles_by_top_n(unknown_profile, profile_2, top_n)

    if (compare_unknown_1 is None) or (compare_unknown_2 is None):
        return None

    if compare_unknown_1 == compare_unknown_2:
        return min(profile_2[0], profile_1[0])
    if compare_unknown_1 < compare_unknown_2:
        return profile_2[0]
    return profile_1[0]


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

    if not (isinstance(predicted, list) and
    isinstance(actual, list) and
    len(predicted) == len(actual)):
        return None


    if not (len(predicted) != 0 and len(actual) !=0):
        return 0.0

    for item in actual:
        if not isinstance(item, float):
            return None

    for item in predicted:
        if not isinstance(item, float):
            return None


    mse_summa = 0
    for i, value in enumerate(actual):
        mse_summa += ((value - predicted[i])**2)

    mse = mse_summa/len(actual)
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
    if not (check_profile(unknown_profile) and
    check_profile(profile_to_compare)
    ):
        return None

    all_words = list(unknown_profile[1].keys())[:]
    all_words = [word for word in list(profile_to_compare[1].keys()) if word not in all_words]

    values_unknown = []
    values_to_compare = []
    for word in all_words:
        if word not in list(unknown_profile[1].keys()):
            values_unknown.append(0.0)
            values_to_compare.append(profile_to_compare[1].get(word))
        elif word not in list(profile_to_compare[1].keys()):
            values_to_compare.append(0.0)
            values_unknown.append(unknown_profile[1].get(word))
        else:
            values_to_compare.append(profile_to_compare[1].get(word))
            values_unknown.append(unknown_profile[1].get(word))


    if calculate_mse(values_unknown, values_to_compare) is None:
        return None

    mse_compared = round(calculate_mse(values_unknown, values_to_compare), 3)
    return mse_compared


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
    if not (check_profile(unknown_profile)
    and check_profile(profile_1)
    and check_profile(profile_2)):
        return None

    mse_1 = compare_profiles_by_mse(unknown_profile, profile_1)
    mse_2 = compare_profiles_by_mse(unknown_profile, profile_2)

    if mse_1 == mse_2:
        return max(profile_1[0], profile_2[0])

    if mse_1 < mse_2:
        return profile_1[0]
    return profile_2[0]



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
