"""
Lab 1.

Language detection
"""

# pylint:disable=unused-argument, too-many-return-statements
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

    tokens = []
    for raw_word in text.split():
        word = ''
        for sym in raw_word:
            if sym.isalpha():
                word += sym
        if word != '':
            tokens.append(word)

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
    for token in tokens:
        if not isinstance(token, str):
            return None

    if not isinstance(stop_words, (list, tuple)):
        return None
    for word in stop_words:
        if not isinstance(word, str):
            return None

    result = [token for token in tokens if token not in stop_words]
    return result



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

    for token in tokens:
        if not isinstance(token, str):
            return None

    if len(tokens) == 0:
        return {}

    counts = {}
    for token in tokens:
        counts[token] = counts.get(token, 0) + 1

    total = len(tokens)
    frequencies = {}
    for token, count in counts.items():
        frequencies[token] = count / total

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
    if not all([isinstance(freq_dict, dict),
                isinstance(top_n, int)]):
        return None

    if top_n <= 0:
        return None

    if not isinstance(freq_dict, dict):
        return None

    if not isinstance(top_n, int) or isinstance(top_n, bool) or top_n <= 0:
        return None

    for word, freq in freq_dict.items():
        if not isinstance(word, str):
            return None
        if not isinstance(freq, (int, float)) or isinstance(freq, bool):
            return None

    items = list(freq_dict.items())
    items.sort(key=lambda pair: (-pair[1], pair[0]))

    result = [word for word, _ in items[:top_n]]
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
    for word in stop_words:
        if not isinstance(word, str):
            return None

    tokens = tokenize(text)
    if tokens is None:
        return None

    filtered_tokens = remove_stop_words(tokens, stop_words)
    if filtered_tokens is None:
        return None

    freq_dict = calculate_frequencies(filtered_tokens)
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

    name, freq_dict, n_words = profile

    if not isinstance(name, str):
        return False

    if not isinstance(freq_dict, dict):
        return False
    for key, value in freq_dict.items():
        if not isinstance(key, str):
            return False
        if not isinstance(value, (int, float)) or isinstance(value, bool):
            return False

    if not isinstance(n_words, int) or isinstance(n_words, bool):
        return False

    if n_words != len(freq_dict):
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
    if not isinstance(top_n, int) or isinstance(top_n, bool) or top_n <= 0:
        return None

    if not check_profile(unknown_profile):
        return None
    if not check_profile(profile_to_compare):
        return None

    unknown_top = get_top_n_words(unknown_profile[1], top_n)
    language_top = get_top_n_words(profile_to_compare[1], top_n)

    if unknown_top is None or language_top is None:
        return None

    if len(unknown_top) == 0:
        return None

    unknown_set = set(unknown_top)
    common = 0
    for word in language_top:
        if word in unknown_set:
            common += 1

    return common / len(unknown_top)

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
    if not isinstance(top_n, int) or isinstance(top_n, bool) or top_n <= 0:
        return None

    if not check_profile(unknown_profile):
        return None
    if not check_profile(profile_1):
        return None
    if not check_profile(profile_2):
        return None

    score_1 = compare_profiles_by_top_n(unknown_profile, profile_1, top_n)
    score_2 = compare_profiles_by_top_n(unknown_profile, profile_2, top_n)

    if score_1 is None or score_2 is None:
        return None

    name_1 = profile_1[0]
    name_2 = profile_2[0]

    if score_1 > score_2:
        return name_1
    if score_2 > score_1:
        return name_2

    return min(name_1, name_2)

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

    if len(predicted) == 0:
        return 0.0

    for val in predicted:
        if not isinstance(val, (int, float)) or isinstance(val, bool):
            return None

    for val in actual:
        if not isinstance(val, (int, float)) or isinstance(val, bool):
            return None

    mse_sum = 0.0

    for pred, act in zip(predicted, actual):
        mse_sum += (pred - act) ** 2

    return mse_sum / len(predicted)


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

    freq_unknown = unknown_profile[1]
    freq_compare = profile_to_compare[1]

    all_tokens = set(freq_unknown.keys()).union(set(freq_compare.keys()))

    actual_values = []
    predicted_values = []

    for token in all_tokens:
        actual_values.append(freq_unknown.get(token, 0.0))
        predicted_values.append(freq_compare.get(token, 0.0))

    return calculate_mse(predicted_values, actual_values)


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
    if (not check_profile(unknown_profile)
        or not check_profile(profile_1)
        or not check_profile(profile_2)):
        return None

    mse_1 = compare_profiles_by_mse(unknown_profile, profile_1)
    mse_2 = compare_profiles_by_mse(unknown_profile, profile_2)

    if mse_1 is None or mse_2 is None:
        return None

    name_1 = profile_1[0]
    name_2 = profile_2[0]

    if mse_1 < mse_2:
        return name_1
    if mse_2 < mse_1:
        return name_2

    return min(name_1, name_2)

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

    file_name = f"{profile[0]}.json"
    path = f"{save_path}/{file_name}"
    lang_profile = {
        "name": profile[0],
        "freq": profile[1],
        "n_words": profile[2]
    }
    with open(path, "w", encoding="utf-8") as file:
        json.dump(lang_profile, file, indent=4, ensure_ascii=False)

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
        file_with_lang_profile = json.load(file)

    if not isinstance(file_with_lang_profile, dict):
        return None

    profile = tuple(file_with_lang_profile.values())

    if not check_profile(profile):
        return None

    return profile


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

    for element in paths_to_profiles:
        if not isinstance(element, str):
            return None

    list_of_profs = []
    for element in paths_to_profiles:
        prof = load_profile(element)
        if prof is not None:
            list_of_profs.append(prof)

    for item in list_of_profs:
        if not check_profile(item):
            return None

    return list_of_profs


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
    if not all([isinstance(unknown_profile, tuple),
            isinstance(known_profiles, (list, tuple)),
            isinstance(top_n, int),
            check_profile(unknown_profile)]):
        return None

    if top_n <= 0:
        return None

    full_list = []
    for profile in known_profiles:
        if not check_profile(profile):
            return None

        compared_by_mse = compare_profiles_by_mse(unknown_profile, profile)
        compared_by_top_n = compare_profiles_by_top_n(unknown_profile, profile, top_n)
        if not (isinstance(compared_by_top_n, float)
                and isinstance(compared_by_mse, float)):
            return None

        dicts = {
            "MSE": compared_by_mse,
            "Top-N": compared_by_top_n
            }
        prof = (profile[0], dicts)
        full_list.append(prof)

    sorted_list = sorted(full_list, key=lambda x:
                        (x[1]["MSE"], -x[1]["Top-N"]))

    return sorted_list


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
    if not all([check_profile(unknown_profile),
              isinstance(metrics_stats, (list, tuple)),
              isinstance(top_n, int),
              ]):
        return None

    if not top_n > 0:
        return None

    for item in metrics_stats:
        if not isinstance(item, tuple):
            return None

        for first_element in item[0]:
            if not isinstance(first_element, str):
                return None

        for second_element in item[1]:
            if not (isinstance(second_element, str)
                    and isinstance(item[1][second_element], float)):
                return None

    pop_words = get_top_n_words(unknown_profile[1], top_n)
    list_of_tokens = []
    for element in unknown_profile[1]:
        list_of_tokens.append(element)

    list_of_nums = []
    for el in list_of_tokens:
        list_of_nums.append(len(el))

    word_of_max_len = list_of_tokens[list_of_nums.index(max(list_of_nums))]
    word_of_min_len = list_of_tokens[list_of_nums.index(min(list_of_nums))]
    av_len = round(sum(list_of_nums) / len(list_of_tokens), 5)

    print("Unknown language stats")
    print("======================")
    print(f"Popular words: {pop_words}")
    print(f"Max length word: '{word_of_max_len}'")
    print(f"Min length word: '{word_of_min_len}'")
    print(f"Average token length: {av_len:.5f}")
    print()
    print("Language scores")
    print("---------------")
    for ele in metrics_stats:
        print(f"{ele[0]}: MSE {ele[1]["MSE"]:.5f}  Top-N Score {ele[1]["Top-N"]:.5f}")

    return None
