"""
Lab 1.

Language detection
"""

# pylint:disable=unused-argument
from json import dumps, loads
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

    wordlst = text.lower().split()
    wordlst_cleaned = []
    for word in wordlst:
        word_cleaned = ""
        for symbol in word:
            if symbol.isalpha():
                word_cleaned += symbol
        if word_cleaned:
            wordlst_cleaned.append(word_cleaned)
    return wordlst_cleaned


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
    if not (
        isinstance(tokens, Sequence)
        and isinstance(stop_words, Sequence)
        and all((isinstance(token, str) for token in tokens))
        and all((isinstance(word, str) for word in stop_words))
    ):
        return None

    return [word for word in tokens if word not in stop_words]


def calculate_frequencies(tokens: Sequence[str]) -> dict[str, float] | None:
    """
    Calculates frequencies of given tokens

    Args:
        tokens (Sequence[str]): Sequence of tokens
    Returns:
        dict[str, float] | None: Dictionary with frequencies.
        Returns None in case of incorrect input types.
    """
    if not (
        isinstance(tokens, Sequence)
        and all((isinstance(token, str) for token in tokens))
    ):
        return None

    return {token: tokens.count(token) / len(tokens) for token in tokens}


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
    if not (
        isinstance(freq_dict, dict)
        and all((isinstance(key, str) for key in freq_dict))
        and all((isinstance(value, float) for value in freq_dict.values()))
        and isinstance(top_n, int)
        and top_n > 0
    ):
        return None

    sorted_freq_dict = dict(sorted(freq_dict.items(), key=lambda item: (-item[1], item[0])))
    return list(sorted_freq_dict)[:top_n]


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
    if not (
        isinstance(language, str)
        and isinstance(text, str)
        and isinstance(stop_words, Sequence)
        and all((isinstance(word, str) for word in stop_words))
    ):
        return None

    tokens = tokenize(text)
    cleaned_tokens = remove_stop_words(tokens, stop_words) if tokens is not None else None
    dict_freqs = calculate_frequencies(cleaned_tokens) if cleaned_tokens is not None else None
    unique_words = len(set(cleaned_tokens)) if cleaned_tokens is not None else None
    if not(dict_freqs is None or unique_words is None):
        return language, dict_freqs, unique_words
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
    if (
        isinstance(profile, tuple)
        and len(profile) == 3
        and isinstance(profile[0], str)
        and isinstance(profile[1], dict)
        and all((isinstance(key, str) for key in profile[1]))
        and all((isinstance(value, float) for value in profile[1].values()))
        and isinstance(profile[2], int)
    ):
        return True
    return False


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
    if not (
        check_profile(unknown_profile)
        and check_profile(profile_to_compare)
        and isinstance(top_n, int)
        and top_n > 0
    ):
        return None

    unk_top_n = get_top_n_words(unknown_profile[1], top_n)
    com_top_n = get_top_n_words(profile_to_compare[1], top_n)
    if not(unk_top_n is None or com_top_n is None):
        return len(set(unk_top_n).intersection(set(com_top_n))) / len(unk_top_n)
    return None


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
        check_profile(unknown_profile)
        and check_profile(profile_1)
        and check_profile(profile_2)
        and isinstance(top_n, int)
        and top_n > 0
    ):
        return None

    dist_1 = compare_profiles_by_top_n(unknown_profile, profile_1, top_n)
    dist_2 = compare_profiles_by_top_n(unknown_profile, profile_2, top_n)
    if not (isinstance(dist_1, float) and isinstance(dist_2, float)):
        return None

    if dist_1 > dist_2:
        return profile_1[0]
    if dist_1 < dist_2:
        return profile_2[0]
    return sorted([profile_1[0], profile_2[0]])[0]


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
    if not (
        isinstance(predicted, Sequence)
        and isinstance(actual, Sequence)
        and all((isinstance(el, float) for el in predicted))
        and all((isinstance(el, float) for el in actual))
        and len(predicted) == len(actual)
    ):
        return None

    if len(predicted) == 0 or len(actual) == 0:
        return 0.0

    differences = [(actual[i] - predicted[i])**2 for i in range(len(actual))]
    return sum(differences) / len(actual)


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
    if not (
        check_profile(unknown_profile)
        and check_profile(profile_to_compare)
    ):
        return None

    tokens = list(set(unknown_profile[1]).union(set(profile_to_compare[1])))
    unk_freqs = [
        unknown_profile[1].get(token)
        if token in unknown_profile[1]
        else 0.0
        for token in tokens
    ]
    com_freqs = [
        profile_to_compare[1].get(token)
        if token in profile_to_compare[1]
        else 0.0
        for token in tokens
    ]
    return calculate_mse(com_freqs, unk_freqs)


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
    if not (
        check_profile(unknown_profile)
        and check_profile(profile_1)
        and check_profile(profile_2)
    ):
        return None

    mse_1 = compare_profiles_by_mse(unknown_profile, profile_1)
    mse_2 = compare_profiles_by_mse(unknown_profile, profile_2)
    if not (isinstance(mse_1, float) and isinstance(mse_2, float)):
        return None

    if mse_1 > mse_2:
        return profile_2[0]
    if mse_1 < mse_2:
        return profile_1[0]
    return sorted([profile_1[0], profile_2[0]])[0]


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
    if not(check_profile(profile) and isinstance(save_path, str)):
        return False

    profile_to_dict = {"name": profile[0], "freq": profile[1], "n_words": profile[2]}
    with open(f"{save_path}/{profile[0]}.json", "w", encoding="utf-8") as file:
        file.write(dumps(profile_to_dict, indent=4, ensure_ascii=False))
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

    with open(path_to_file, "r", encoding="utf-8") as file:
        dict_profile = loads(file.read())
    profile = tuple(dict_profile.values()) if dict_profile is not None else None
    if check_profile(profile):
        return profile
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
    if not(
        isinstance(paths_to_profiles, Sequence)
        and all((isinstance(path, str) for path in paths_to_profiles))
    ):
        return None

    profiles = [
        load_profile(path)
        for path in paths_to_profiles
        if load_profile(path) is not None
    ]
    if all((check_profile(profile) for profile in profiles)):
        return profiles
    return None


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
    if not(
        check_profile(unknown_profile)
        and isinstance(known_profiles, Sequence)
        and all((check_profile(profile) for profile in known_profiles))
        and isinstance(top_n, int)
        and top_n > 0
    ):
        return None

    metrics_stats = [
        (
            known_profile[0],
            {
                "MSE": compare_profiles_by_mse(unknown_profile, known_profile),
                "Top-N": compare_profiles_by_top_n(unknown_profile, known_profile, top_n)
            }
        )
        for known_profile in known_profiles
    ]
    return sorted(
        metrics_stats,
        key=lambda x: (-x[1].get("MSE"), -x[1].get("Top-N"), x[0])
    )


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
        check_profile(unknown_profile)
        and isinstance(metrics_stats, Sequence)
        and all((isinstance(lang, tuple) for lang in metrics_stats))
        and all((isinstance(lang[0], str) for lang in metrics_stats))
        and all((isinstance(lang[1], dict) for lang in metrics_stats))
        and all((isinstance(list(lang[1].keys())[0], str) for lang in metrics_stats))
        and all((isinstance(list(lang[1].keys())[1], str) for lang in metrics_stats))
        and all((isinstance(list(lang[1].values())[0], float) for lang in metrics_stats))
        and all((isinstance(list(lang[1].values())[1], float) for lang in metrics_stats))
    ):
        popular_words = get_top_n_words(unknown_profile[1], top_n)
        max_len_word = max(set(unknown_profile[1]), key=len)
        min_len_word = min(set(unknown_profile[1]), key=len)
        average_len = sum(
            (len(token) for token in set(unknown_profile[1]))
        ) / len(set(unknown_profile[1]))
        print(
            f"""
            Unknown language stats
            ======================
            Popular words: {popular_words}
            Max length word: {max_len_word}
            Min length word: {min_len_word}
            Average token length: {average_len:.5f}

            Language scores
            ---------------
            """
        )
        for lang in metrics_stats:
            print(
                f"{lang[0]}:",
                f"MSE {list(lang[1].values())[0]:.5f}",
                f"Top-N Score {list(lang[1].values())[1]:.5f}"
            )
