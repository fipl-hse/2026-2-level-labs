"""
Checks the first lab get top words function
"""

import pytest

from lab_1_classify_profile.main import get_top_n_words


@pytest.mark.lab_1_classify_profile
@pytest.mark.mark4
@pytest.mark.mark6
@pytest.mark.mark8
@pytest.mark.mark10
def test_get_top_n_words_ideal() -> None:
    """
    Ideal get top number of words scenario
    """
    expected = ["man"]
    actual = get_top_n_words({"happy": 0.2, "man": 0.3}, 1)
    assert expected == actual


@pytest.mark.lab_1_classify_profile
@pytest.mark.mark4
@pytest.mark.mark6
@pytest.mark.mark8
@pytest.mark.mark10
def test_get_top_n_words_same_frequency() -> None:
    """
    Get top number of words with the same frequency check
    """
    expected = ["happy", "hello", "man"]
    actual = get_top_n_words({"happy": 0.2, "man": 0.2, "hello": 0.2}, 3)
    assert expected == actual
    expected = ["happy"]
    actual = get_top_n_words({"man": 0.2, "happy": 0.2, "hello": 0.2}, 1)
    assert expected == actual


@pytest.mark.lab_1_classify_profile
@pytest.mark.mark4
@pytest.mark.mark6
@pytest.mark.mark8
@pytest.mark.mark10
def test_get_top_n_words_more_number() -> None:
    """
    Get top number of words with bigger number of words than in dictionary
    """
    expected = ["man", "happy"]
    actual = get_top_n_words({"happy": 0.2, "man": 0.3}, 10)
    assert expected == actual


@pytest.mark.lab_1_classify_profile
@pytest.mark.mark4
@pytest.mark.mark6
@pytest.mark.mark8
@pytest.mark.mark10
def test_get_top_n_words_bad_inputs() -> None:
    """
    Get top number of words with bad argument inputs
    """
    bad_inputs = ["string", (), None, 9, 9.34, True, [None], []]
    expected = None
    for bad_input in bad_inputs:
        actual = get_top_n_words(bad_input, 2)
        assert expected == actual


@pytest.mark.lab_1_classify_profile
@pytest.mark.mark4
@pytest.mark.mark6
@pytest.mark.mark8
@pytest.mark.mark10
def test_get_top_n_words_empty() -> None:
    """
    Get top number of words with empty arguments
    """
    expected = []
    actual = get_top_n_words({}, 10)
    assert expected == actual


@pytest.mark.lab_1_classify_profile
@pytest.mark.mark4
@pytest.mark.mark6
@pytest.mark.mark8
@pytest.mark.mark10
def test_get_top_n_words_incorrect_numbers() -> None:
    """
    Get top number of words using incorrect number of words parameter
    """
    actual = get_top_n_words({}, -1)
    assert actual is None
    actual = get_top_n_words({"happy": 0.2}, 0)
    assert actual is None
