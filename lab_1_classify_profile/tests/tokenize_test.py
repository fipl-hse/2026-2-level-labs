"""
Checks the first lab text preprocessing functions
"""

import pytest

from lab_1_classify_profile.main import tokenize


@pytest.mark.lab_1_classify_profile
@pytest.mark.mark4
@pytest.mark.mark6
@pytest.mark.mark8
@pytest.mark.mark10
def test_tokenize_ideal() -> None:
    """
    Ideal tokenize scenario
    """
    expected = ["the", "weather", "is", "sunny"]
    actual = tokenize("The weather is sunny.")
    assert expected == actual


@pytest.mark.lab_1_classify_profile
@pytest.mark.mark4
@pytest.mark.mark6
@pytest.mark.mark8
@pytest.mark.mark10
def test_tokenize_several_sentences() -> None:
    """
    Tokenize text with several sentences
    """
    expected = ["the", "first", "sentence", "the", "second", "sentence"]
    actual = tokenize("The first sentence. The second sentence.")
    assert expected == actual


@pytest.mark.lab_1_classify_profile
@pytest.mark.mark4
@pytest.mark.mark6
@pytest.mark.mark8
@pytest.mark.mark10
def test_tokenize_punctuation_marks() -> None:
    """
    Tokenize text with different punctuation marks
    """
    expected = ["the", "first", "sentence", "nice"]
    actual = tokenize("The, first sentence - nice!")
    assert expected == actual


@pytest.mark.lab_1_classify_profile
@pytest.mark.mark4
@pytest.mark.mark6
@pytest.mark.mark8
@pytest.mark.mark10
def test_tokenize_german_ideal() -> None:
    """
    Tokenize german text
    """
    expected = [
        "ich",
        "weiß",
        "nicht",
        "was",
        "ich",
        "machen",
        "möchte",
        "vielleicht",
        "ich",
        "muss",
        "das",
        "überlegen",
    ]
    actual = tokenize("Ich weiß nicht was ich machen möchte. Vielleicht ich muss das überlegen")
    assert expected == actual


@pytest.mark.lab_1_classify_profile
@pytest.mark.mark4
@pytest.mark.mark6
@pytest.mark.mark8
@pytest.mark.mark10
def test_tokenize_dirty_text() -> None:
    """
    Tokenize dirty text
    """
    expected = ["the", "first", "sentence", "the", "second", "sentence"]
    actual = tokenize("The first% sentence><. The sec&*ond sent@ence #.")
    assert expected == actual


@pytest.mark.lab_1_classify_profile
@pytest.mark.mark4
@pytest.mark.mark6
@pytest.mark.mark8
@pytest.mark.mark10
def test_tokenize_bad_input() -> None:
    """
    Tokenize bad input argument scenario
    """
    bad_inputs = [[], {}, (), None, 9, 9.34, True]
    expected = None
    for bad_input in bad_inputs:
        actual = tokenize(bad_input)
        assert expected == actual
