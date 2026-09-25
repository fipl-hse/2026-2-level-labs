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

    if isinstance(text,str) is False:
        return None

    text = text.lower()

    for word in text:
        if not word.isalpha() and not word.isspace():
            text = text.replace(word, "")

    tokens = text.split()

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

    if isinstance(tokens,list) is False or isinstance(stop_words,list) is False:
        return None

    for check in tokens:
        if isinstance(check,str) is False:
            return None

    for check in stop_words:
        if isinstance(check,str) is False:
            return None

    checked_tokens = [token for token in tokens if token not in stop_words]

    return checked_tokens

def calculate_frequencies(tokens: Sequence[str]) -> dict[str, float] | None:
    """
    Calculates frequencies of given tokens

    Args:
        tokens (Sequence[str]): Sequence of tokens
    Returns:
        dict[str, float] | None: Dictionary with frequencies.
        Returns None in case of incorrect input types.
    """

    if isinstance(tokens, list) is False:
        return None

    for token in tokens:
        if isinstance(token, str) is False:
            return None

    freq_dict = {}

    for token in tokens:
        if token in freq_dict:
            freq_dict[token] += 1 / len(tokens)
        else:
            freq_dict[token] = 1 / len(tokens)

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
    if isinstance(freq_dict, dict) is False or isinstance(top_n, int) is False or top_n <= 0:
        return None

    for key, value in freq_dict.items():
        if isinstance(key, str) is False or isinstance(value, float) is False:
            return None

    items_sorted = (sorted(freq_dict.items(), key=lambda x: (-x[1],x[0])))

    top_words = [word for word, _ in items_sorted[:top_n]]

    return top_words

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
    if not all(
        [
            isinstance(language, str),
            isinstance(text, str),
            isinstance(stop_words, list)
        ]
    ):
        return None

    for word in stop_words:
        if isinstance(word, str) is False:
            return None

    profile = tuple()

    profile_tokens = tokenize(text)
    if profile_tokens is None:
        return None

    profile_tokens_without_stopwords = remove_stop_words(profile_tokens, stop_words)
    if profile_tokens_without_stopwords is None:
        return None

    profile_freq_dict = calculate_frequencies(profile_tokens_without_stopwords)
    if profile_freq_dict is None:
        return None

    profile = (language, profile_freq_dict, len(profile_freq_dict))

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
    if isinstance(profile, tuple) is False or len(profile) != 3:
        return False

    language, freq_dict, word_count = profile

    if not all(
        [
            isinstance(language, str),
            isinstance(freq_dict, dict),
            isinstance(word_count, int),
        ]
    ):
        return False

    for key, value in freq_dict.items():
        if all([isinstance(key, str),isinstance(value, float)]) is False:
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

    if isinstance(top_n, int) is False or top_n <= 0:
        return None

    top_n_words_unknown = get_top_n_words(unknown_profile[1], top_n)
    if top_n_words_unknown is None:
        return None

    top_n_words_compare = get_top_n_words(profile_to_compare[1], top_n)
    if top_n_words_compare is None:
        return None

    common_words = [word for word in top_n_words_unknown if word in top_n_words_compare]

    count_common = len(common_words) if common_words is not None else 0

    count_unknown = len(top_n_words_unknown) if top_n_words_unknown is not None else 0

    result =count_common / count_unknown

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

    if not all([check_profile(profile_1), check_profile(profile_2)]):
        return None

    if check_profile(unknown_profile) is False:
        return None

    if isinstance(top_n, int) is False or top_n <= 0:
        return None

    result = None

    count_1 = compare_profiles_by_top_n(unknown_profile, profile_1, top_n)

    count_2 = compare_profiles_by_top_n(unknown_profile, profile_2, top_n)

    if count_1 is None or count_2 is None:
        return None

    if count_1 > count_2:
        result = profile_1[0]
    elif count_2 > count_1:
        result = profile_2[0]
    elif count_1 == count_2:
        sorted_profiles = sorted([profile_1[0], profile_2[0]])
        result = sorted_profiles[0]

    return result



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

    for x in predicted:
        if not isinstance(x,float):
            return None

    for x in actual:
        if not isinstance(x,float):
            return None

    if len(predicted) != len(actual):
        return None

    if len(predicted) == 0 or len(actual) == 0:
        return 0.0

    difference: list[float] = [(p - a) ** 2 for p in predicted for a in actual]

    mse = 0.0

    mse = sum(difference) / len(difference)

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
    if not all([check_profile(unknown_profile), check_profile(profile_to_compare)]):
        return None

    predicted = [unknown_profile[1].get(word, 0.0) for word in profile_to_compare[1].keys()]
    actual = [profile_to_compare[1][word] for word in profile_to_compare[1].keys()]

    calculated_mse = calculate_mse(predicted, actual)

    return calculated_mse

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
    if not all(
        [
            check_profile(unknown_profile),
            check_profile(profile_1),
            check_profile(profile_2)
        ]
    ):
        return None

    result = None

    mse_1 = compare_profiles_by_mse(unknown_profile, profile_1)
    mse_2 = compare_profiles_by_mse(unknown_profile, profile_2)

    if mse_1 is None or mse_2 is None:
        return None

    if mse_1 < mse_2:
        result = profile_1[0]
    if mse_2 < mse_1:
        result = profile_2[0]
    if mse_1 == mse_2:
        sorted_profiles = sorted([profile_1[0], profile_2[0]])
        result =  sorted_profiles[0]

    return result


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
