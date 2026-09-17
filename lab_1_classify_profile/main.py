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
    words = text.split()
    for word in words:
        right_word = ''
        for a in word:
            if a.isalpha():
                right_word += a.lower()
        if right_word != "":
            tokens.append(right_word)
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
    if not isinstance(stop_words, (list, tuple)):
        return None
    without_stopwords = []
    for token in tokens:
        if token not in stop_words:
            without_stopwords.append(token)
    return without_stopwords

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
    counting = {}
    for token in tokens:
        if token in counting:
            counting[token] += 1
        else:
            counting[token] = 1
    total = len(tokens)
    freq_dict = {}
    for token in counting:
        freq_dict[token] = counting[token]/total
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
    items = list(freq_dict.items())
    for b in range(len(items)):
        for c in range(len(items)-1-b):
            word1, freq1 = items[c]
            word2, freq2 = items[c+1]
            place = False
            if freq1 < freq2:
                place = True
            elif freq1 == freq2 and word1 > word2:
                place = True
            if place:
                items[c], items[c + 1] = items[c + 1], items[c]
    topwords = []
    for d in range(len(items)):
        if d >= top_n:
            break
        topwords.append(items[d][0])
    return topwords

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
    if not isinstance(stop_words, (list,tuple)):
        return None
    tokens = tokenize(text)
    clean_tokens = remove_stop_words(tokens, stop_words)
    freq = calculate_frequencies(clean_tokens)
    n_words = len(freq)
    return (language, freq, n_words)

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
    name, freq, n_words = profile
    if not isinstance(name, str):
        return False
    if not isinstance(freq, dict):
        return False
    for key, value in freq.items():
        if not isinstance(key, str):
            return False
        if not isinstance(value, (int, float)):
            return False
    if not isinstance(n_words, int):
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
    if not check_profile(unknown_profile):
        return None
    if not check_profile(profile_to_compare):
        return None
    unknown_freq = unknown_profile[1]
    language_freq = profile_to_compare[1]
    unknown_topwords = get_top_n_words(unknown_freq, top_n)
    language_topwords = get_top_n_words(language_freq, top_n)
    general = 0
    for word in unknown_topwords:
        if word in language_topwords:
            general += 1
    return general/len(unknown_topwords)

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
    number_1 = compare_profiles_by_top_n(unknown_profile, profile_1, top_n)
    number_2 = compare_profiles_by_top_n(unknown_profile, profile_2, top_n)
    name_1 = profile_1[0]
    name_2 = profile_2[0]
    if number_1 == number_2:
        if name_1 <= name_2:
            return name_1
        else:
            return name_2
    if number_1 > number_2:
        return name_1
    else:
        return name_2

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
