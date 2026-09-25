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
    if type(text) != str:
        return None
    tokens = []
    for word in text.split():
<<<<<<< HEAD
        clean_word = ''
        for letter in word:
            if letter.isalpha():
                clean_word += letter.lower()
    if len(clean_word) > 0:
        tokens.append(clean_word)
    return tokens

=======
        clean_word = ""
        for letter in word:
            if letter.isalpha():
                clean_word +=
    letter.lower()
    if len(clean_word) > 0:
        tokens.append(clean_word)
    return tokens
>>>>>>> 85ebe6eb751346f1e03c0c8a1fd09d5a1969bb9d

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
<<<<<<< HEAD
    if type(tokens) != list or  type (stop_words) != list:
=======
    if type(tokens) != list or type (stop_words) != list:
>>>>>>> 85ebe6eb751346f1e03c0c8a1fd09d5a1969bb9d
        return None
    result = []
    for word in tokens:
        if word not in stop_words:
<<<<<<< HEAD
            result.append
    return result
=======
            result.append(word)
    return result

>>>>>>> 85ebe6eb751346f1e03c0c8a1fd09d5a1969bb9d


def calculate_frequencies(tokens: Sequence[str]) -> dict[str, float] | None:
    """
    Calculates frequencies of given tokens

    Args:
        tokens (Sequence[str]): Sequence of tokens
    Returns:
        dict[str, float] | None: Dictionary with frequencies.
        Returns None in case of incorrect input types.
    """
<<<<<<< HEAD
    if not isinstance(tokens, (list, tuple)):
        return None
    for token in tokens:
        if not isinstance(token, str):
            return None

    total = len(tokens)
    if total == 0:
        return {}

    freq_dict = {}
    for token in tokens:
        freq_dict[token] = freq_dict.get(token, 0) + 1

    return {word: count / total for word, count in freq_dict.items()}
=======
    if type(tokens) not in (list, tuple):
        return None
    if not tokens:
        return {}
    freq_dictionary = {}
    for token in tokens:
        if token in freq_dictionary:
            freq_dictionary[token] += 1
        else:
            freq_dictionary[token] = 1
    return freq_dictionary
>>>>>>> 85ebe6eb751346f1e03c0c8a1fd09d5a1969bb9d



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
    if not isinstance(top_n, int) or top_n <=0:
        return None

    return sorted(freq_dict, key=freq_dict.get, reverse=True)[:top_n]


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
    if not isinstance(language, str) or not isinstance(text, str) or not isinstance(stop_words, (list, tuple)):
            return None
    for word in stop_words:
            if not isinstance(word, str):
                return None

    tokens = text.lower().split()
    filtered = [t for t in tokens if t not in stop_words]

    if not filtered:
        return {"language": language, "frequencies": {}}

    freq = {}
    for t in filtered:
        freq[t] = freq.get(t, 0) + 1

    total = len(filtered)
    for k in freq:
        freq[k] = freq[k] / total

    return {"language": language, "frequencies": freq}


def check_profile(profile: ProfileType) -> bool:
    """
    Checks profile structure

    Args:
        profile (ProfileType): Profile to check

    Returns:
        bool: Returns True if the profile has right structure and types,
        otherwise returns False.
    """
    if not isinstance(profile, dict):
        return False
    if "language" not in profile or "frequencies" not in profile:
        return False
    if not isinstance(profile["frequencies"], dict):
        return False

    for word, freq in profile["frequencies"].items():
        if not isinstance(word, str) or not isinstance(freq, (int, float)):
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
    if not isinstance(unknown_profile, dict) or not isinstance(profile_to_compare, dict):
        return None
    if "frequencies" not in unknown_profile or "frequencies" not in profile_to_compare:
        return None
    if not isinstance(top_n, int) or top_n <= 0:
        return None

    freq_unknown = unknown_profile["frequencies"]
    freq_ref = profile_to_compare["frequencies"]

    top_words = sorted(freq_unknown, key=freq_unknown.get, reverse=True)[:top_n]

    distance = 0.0
    for word in top_words:
        distance += abs(freq_unknown.get(word, 0) - freq_ref.get(word, 0))

        return distance


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
    if not isinstance(unknown_profile, dict) or not isinstance(profile_1, dict) or not isinstance(profile_2, dict):
        return None
    if "language" not in profile_1 or "language" not in profile_2:
        return None
    if not isinstance(top_n, int) or top_n <= 0:
        return None

    distance_1 = compare_profiles_by_top_n(unknown_profile, profile_1, top_n)
    distance_2 = compare_profiles_by_top_n(unknown_profile, profile_2, top_n)

    if distance_1 is None or distance_2 is None:
        return None

    if distance_1 <= distance_2:
        return profile_1["language"]
    else:
        return profile_2["language"]



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
