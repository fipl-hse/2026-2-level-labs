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
    current_word = ""

    for char in text:
        if char.isalpha():
            current_word += char.lower()
        elif char.isspace():
            if current_word:
                tokens.append(current_word)
                current_word = ""

    if current_word:
        tokens.append(current_word)

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

    stop_words_set = set(stop_words)
    return [token for token in tokens if token not in stop_words_set]





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

    if not tokens:
        return {}

    counts = {}
    for token in tokens:
        counts[token] = counts.get(token, 0) + 1

    total_count = len(tokens)
    frequencies = {}
    for token, count in counts.items():
        frequencies[token] = count / total_count

    return frequencies


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
    if not isinstance(freq_dict, dict) or not isinstance(top_n, int) or isinstance(top_n, bool):
        return None

    if not all(isinstance(k, str) and isinstance(v, (int, float)) for k, v in freq_dict.items()):
        return None

    if top_n <= 0:
        return None

    sorted_words = sorted(freq_dict.keys(), key=lambda w: (-freq_dict[w], w))

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
    if (not isinstance(language, str) or not isinstance(text, str) or
            not isinstance(stop_words, Sequence) or isinstance(stop_words, str) or
            not all(isinstance(w, str) for w in stop_words)):
        return None

    tokens = tokenize(text)
    if tokens is not None:
        clean_tokens = remove_stop_words(tokens, stop_words)
        if clean_tokens is not None:
            frequencies = calculate_frequencies(clean_tokens)
            if frequencies is not None:
                return (language, frequencies, len(frequencies))
    return None




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

    lang, freqs, length = profile

    if not isinstance(lang, str):
        return False

    if not isinstance(freqs, dict):
        return False

    if not all(isinstance(k, str) and isinstance(v, float) for k, v in freqs.items()):
        return False

    if not isinstance(length, int) or isinstance(length, bool):
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
    if not isinstance(unknown_profile, tuple) or not isinstance(profile_to_compare, tuple):
        return None
    if not isinstance(top_n, int) or isinstance(top_n, bool) or top_n <= 0:
        return None
    if not check_profile(unknown_profile) or not check_profile(profile_to_compare):
        return None

    un_top = get_top_n_words(unknown_profile[1], top_n)
    comp_top = get_top_n_words(profile_to_compare[1], top_n)

    if un_top is None or comp_top is None:
        return None

    if len(un_top) == 0:
        return 0.0

    common_words_count = 0
    for word in un_top:
        if word in comp_top:
            common_words_count += 1

    return float(common_words_count / len(un_top))



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
    if (not isinstance(unknown_profile, tuple) or
            not isinstance(profile_1, tuple) or
            not isinstance(profile_2, tuple)):
        return None

    if (not isinstance(top_n, int) or
            isinstance(top_n, bool) or
            top_n <= 0):
        return None

    if (not check_profile(unknown_profile) or not check_profile(profile_1) or
            not check_profile(profile_2)):
        return None

    score_1 = compare_profiles_by_top_n(unknown_profile, profile_1, top_n)
    score_2 = compare_profiles_by_top_n(unknown_profile, profile_2, top_n)
    result = None

    if score_1 is not None and score_2 is not None:
        if score_1 > score_2:
            result = profile_1[0]
        elif score_2 > score_1:
            result = profile_2[0]
        elif profile_1[0] < profile_2[0]:
            result = profile_1[0]
        else:
            result = profile_2[0]

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
    if (not isinstance(predicted, (list, tuple)) or
            not isinstance(actual, (list, tuple)) or
            len(predicted) != len(actual)):
        return None

    if len(predicted) == 0:
        return 0.0

    for p_value in predicted:
        if not isinstance(p_value, (int, float)) or isinstance(p_value, bool):
            return None

    for a_value in actual:
        if not isinstance(a_value, (int, float)) or isinstance(a_value, bool):
            return None

    error_sum = 0.0
    for i, pred_val in enumerate(predicted):
        difference = pred_val - actual[i]
        error_sum += difference ** 2

    return float(error_sum / len(predicted))


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
    if not isinstance(unknown_profile, tuple) or not isinstance(profile_to_compare, tuple):
        return None
    if not check_profile(unknown_profile) or not check_profile(profile_to_compare):
        return None

    un_freqs = unknown_profile[1]
    comp_freqs = profile_to_compare[1]

    all_words = []
    for word in un_freqs:
        if word not in all_words:
            all_words.append(word)
    for word in comp_freqs:
        if word not in all_words:
            all_words.append(word)

    predicted = []
    actual = []

    for word in all_words:
        if word in un_freqs:
            predicted.append(un_freqs[word])
        else:
            predicted.append(0.0)

        if word in comp_freqs:
            actual.append(comp_freqs[word])
        else:
            actual.append(0.0)

    return calculate_mse(predicted, actual)


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
    if (not isinstance(unknown_profile, tuple) or
            not isinstance(profile_1, tuple) or
            not isinstance(profile_2, tuple)):
        return None

    if (not check_profile(unknown_profile) or
            not check_profile(profile_1) or
            not check_profile(profile_2)):
        return None

    mse_1 = compare_profiles_by_mse(unknown_profile, profile_1)
    mse_2 = compare_profiles_by_mse(unknown_profile, profile_2)
    result = None

    if mse_1 is not None and mse_2 is not None:
        if mse_1 < mse_2:
            result = profile_1[0]
        elif mse_2 < mse_1:
            result = profile_2[0]
        elif profile_1[0] < profile_2[0]:
            result = profile_1[0]
        else:
            result = profile_2[0]

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
