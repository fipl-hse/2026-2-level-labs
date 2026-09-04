"""
Checks the first lab stop words removal functions
"""

import pytest

from lab_1_classify_profile.main import remove_stop_words

STOP_WORDS = ["the", "a", "is"]


@pytest.mark.lab_1_classify_profile
@pytest.mark.mark4
@pytest.mark.mark6
@pytest.mark.mark8
@pytest.mark.mark10
def test_remove_stop_words_ideal() -> None:
    """
    Ideal removing stop words scenario
    """
    expected = ["weather", "sunny", "man", "happy"]
    actual = remove_stop_words(
        ["the", "weather", "is", "sunny", "the", "man", "is", "happy"],
        STOP_WORDS,
    )
    assert expected == actual


@pytest.mark.lab_1_classify_profile
@pytest.mark.mark4
@pytest.mark.mark6
@pytest.mark.mark8
@pytest.mark.mark10
def test_remove_stop_words_bad_input() -> None:
    """
    Remove stop words bad input scenario
    """
    bad_inputs = [{"a": "b"}, [-1, 2], None, 9, 9.34, True]
    expected = None
    for bad_input in range(0, 6):
        actual = remove_stop_words(["word"], bad_inputs[bad_input])
        assert expected == actual
        actual = remove_stop_words(bad_inputs[bad_input], ["and"])
        assert expected == actual


@pytest.mark.lab_1_classify_profile
@pytest.mark.mark4
@pytest.mark.mark6
@pytest.mark.mark8
@pytest.mark.mark10
def test_remove_stop_words_no_stop_words() -> None:
    """
    Remove stop words without stop words scenario
    """
    expected = ["token1", "token2"]
    actual = remove_stop_words(["token1", "token2"], [])
    assert expected == actual


def test_remove_stop_words_all_words() -> None:
    """
    Remove stop words as the whole text scenario
    """
    expected = []
    actual = remove_stop_words(["the", "a", "is"], STOP_WORDS)
    assert expected == actual
