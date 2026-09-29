"""
Lab 1.

Language detection
"""

import json
import os

# pylint:disable=unused-argument
import json
import re
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
    text = re.sub(r"[^\w\s]|\d", "", text)
    tokens = list(text.split())

    return tokens

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
    if not all([isinstance(tokens, (list, tuple)),
                isinstance(stop_words, (list, tuple))]):
        return None

    if not all(isinstance(i, str) for i in tokens):
        return None

    if not all(isinstance(i, str) for i in stop_words):
        return None

    cleaned_text = [word for word in tokens if word not in stop_words]

    return cleaned_text

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

    for element in tokens:
        if not isinstance(element, str):
            return None

    frequency = {}
    overall_words = len(tokens)
    for element in tokens:
        frequency[element] = frequency.get(element, 0.0) + 1.0 / overall_words

    return frequency


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

    for key, value in freq_dict.items():
        if not all([isinstance(key, str),
                isinstance(value, float)]):
            return None

    freq_tuples = list(freq_dict.items())
    sorted_freq_tuples = sorted(freq_tuples, key=lambda x: (-x[1], x[0]))
    sorted_freq_list = list(sorted_freq_tuples[:top_n])
    sorted_list = [element[0] for element in sorted_freq_list]

    return sorted_list

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
    if not all([isinstance(language, str),
                isinstance(text, str),
                isinstance(stop_words, (list, tuple))]):
        return None

    tokenized_text = tokenize(text)
    if not tokenized_text:
        return None

    tokenized_text_without_stopwords = remove_stop_words(tokenized_text, stop_words)
    if not tokenized_text_without_stopwords:
        return None

    freq_dict = calculate_frequencies(tokenized_text_without_stopwords)
    if not freq_dict:
        return None

    if not all([isinstance(tokenized_text, list),
                isinstance(tokenized_text_without_stopwords, list),
                isinstance(freq_dict, dict)]):
        return None

    for el in freq_dict:
        freq_dict[el] = freq_dict[el] / len(tokenized_text_without_stopwords)
    n_words = len(freq_dict)

    return language, freq_dict, n_words

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
    if not isinstance(profile, tuple):
        return False

    if not len(profile) == 3:
        return False

    if not all ([isinstance(profile[0], str),
              isinstance(profile[1], dict),
              isinstance(profile[2], int)]):
        return False

    for keys, values in profile[1].items():
        if not (isinstance(keys, str) and isinstance(values, float)):
            return False

    return True

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
    if not all([check_profile(unknown_profile),
                check_profile (profile_to_compare)]):
        return None

    if not isinstance(top_n, int):
        return None

    if top_n <= 0:
        return None

    freq_dict_unk = unknown_profile[1]
    freq_dict_sec = profile_to_compare[1]
    top_words_unk = get_top_n_words(freq_dict_unk, top_n)
    top_words_sec = get_top_n_words(freq_dict_sec, top_n)

    if not (isinstance(top_words_unk, (list, tuple))
            and isinstance(top_words_sec, (list, tuple))):
        return None

    list_of_common_words = [word for word in top_words_unk if word in top_words_sec]

    num_of_common_words = len(list_of_common_words)

    num_of_unk_words = len(top_words_unk)
    result = num_of_common_words / num_of_unk_words

    return result

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
    if not isinstance(top_n, int):
        return None

    if not (check_profile(unknown_profile)
            and check_profile(profile_1)
            and check_profile(profile_2)
            and top_n>0):
        return None

    compared_unk_n_1 = compare_profiles_by_top_n(unknown_profile, profile_1, top_n)
    compared_unk_n_2 = compare_profiles_by_top_n(unknown_profile, profile_2, top_n)

    if (compared_unk_n_1 is None
        or compared_unk_n_2 is None):
        return None

    if compared_unk_n_1 > compared_unk_n_2:
        return profile_1[0]

    if compared_unk_n_1 < compared_unk_n_2:
        return profile_2[0]

    list_of_langs = [profile_1[0], profile_2[0]]
    sorted_list = sorted(list_of_langs)

    return sorted_list[0]

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
    if not all([isinstance(predicted, (tuple, list)),
                    isinstance(actual, (list, tuple))]):
        return None

    if len(predicted) != len(actual):
        return None

    if not (predicted
            and actual):
        return 0.0

    for element in predicted:
        if not isinstance(element, float):
            return None

    for el in actual:
        if not isinstance(el, float):
            return None

    list_of_values = zip(actual, predicted)
    diffs = []

    for elem in list_of_values:
        diff = (elem[0] - elem[1])**2
        diffs.append(diff)

    return sum(diffs) / len(actual)

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
    if not all([check_profile(unknown_profile),
              check_profile (profile_to_compare)]):
        return None

    list_of_unk = []
    list_of_second = []
    list_of_tokens = []

    for element in unknown_profile[1]:
        list_of_tokens.append(element)
        list_of_unk.append(element)

    for el in profile_to_compare[1]:
        list_of_second.append(el)
        if el not in list_of_tokens:
            list_of_tokens.append(el)

    list_of_mse_unk = [
        unknown_profile[1][i]
        if i in list_of_unk
        else 0.0
        for i in list_of_tokens
        ]

    list_of_mse_sec = [
        profile_to_compare[1][i]
        if i in list_of_second
        else 0.0
        for i in list_of_tokens
        ]

    return calculate_mse(list_of_mse_unk, list_of_mse_sec)

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
    if not all([check_profile(unknown_profile),
                check_profile(profile_1),
                check_profile(profile_2)]):
        return None

    compared_1 = compare_profiles_by_mse(unknown_profile, profile_1)
    compared_2 = compare_profiles_by_mse(unknown_profile, profile_2)

    if (compared_1 is None
        or compared_2 is None):
        return None

    if compared_1 > compared_2:
        return profile_2[0]

    if compared_1 < compared_2:
        return profile_1[0]

    list_of_langs = [profile_1[0], profile_2[0]]
    sorted_list = sorted(list_of_langs)

    return sorted_list[0]

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

    with open(path_to_file, "r", encoding="utf-8") as file:
        file_with_lang_profile = json.load(file)

    if not isinstance(file_with_lang_profile, dict):
        return None

    profile = tuple(file_with_lang_profile.values())

    if not check_profile(profile):
        return None

    return profile

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
