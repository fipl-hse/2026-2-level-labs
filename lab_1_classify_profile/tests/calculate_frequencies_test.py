"""
Checks the first lab calculate frequencies function
"""

import pytest

from lab_1_classify_profile.main import calculate_frequencies


@pytest.mark.lab_1_classify_profile
@pytest.mark.mark4
@pytest.mark.mark6
@pytest.mark.mark8
@pytest.mark.mark10
def test_calculate_frequencies_ideal() -> None:
    """
    Ideal calculate frequencies scenario
    """
    expected = {"happy": 0.25, "man": 0.25, "sunny": 0.25, "weather": 0.25}
    actual = calculate_frequencies(["weather", "sunny", "man", "happy"])
    assert expected == actual


@pytest.mark.lab_1_classify_profile
@pytest.mark.mark4
@pytest.mark.mark6
@pytest.mark.mark8
@pytest.mark.mark10
def test_calculate_frequencies_complex() -> None:
    """
    Calculate frequencies with several same tokens
    """
    expected = {"weather": 0.4, "sunny": 0.2, "man": 0.2, "happy": 0.2}
    actual = calculate_frequencies(["weather", "sunny", "man", "happy", "weather"])
    assert expected == actual


@pytest.mark.lab_1_classify_profile
@pytest.mark.mark4
@pytest.mark.mark6
@pytest.mark.mark8
@pytest.mark.mark10
def test_calculate_frequencies_bad_input() -> None:
    """
    Calculate frequencies invalid input tokens check
    """
    bad_inputs = [None, 9, 9.34, True, [None], {1: 0}]
    for bad_input in bad_inputs:
        assert calculate_frequencies(bad_input) is None


@pytest.mark.lab_1_classify_profile
@pytest.mark.mark4
@pytest.mark.mark6
@pytest.mark.mark8
@pytest.mark.mark10
def test_calculate_frequencies_return_value() -> None:
    """
    Calculate frequencies return values check
    """
    tokens = ["token1", "token2"]
    expected = 2
    actual = calculate_frequencies(tokens)
    assert expected == len(actual)
    for token in tokens:
        assert actual[token]
    assert isinstance(actual[tokens[0]], float)
