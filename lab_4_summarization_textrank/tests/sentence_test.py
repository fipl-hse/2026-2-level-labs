"""
Checks the fourth lab Sentence abstraction
"""

import pytest

from lab_4_summarization_textrank.main import IncorrectArgumentError, Sentence
from lab_4_summarization_textrank.tests.conftest import InvalidInput


@pytest.mark.lab_4_summarization_textrank
@pytest.mark.mark6
@pytest.mark.mark8
@pytest.mark.mark10
def test_sentence_initialization_ideal(sentence: Sentence) -> None:
    """
    Checks Sentence initialization and its attributes

    Args:
        sentence (Sentence): An instance of Sentence
    """
    for attribute in ["_text", "_preprocessed", "_encoded", "_position"]:
        assert hasattr(sentence, attribute), f"Sentence misses {attribute} attribute"


@pytest.mark.lab_4_summarization_textrank
@pytest.mark.mark6
@pytest.mark.mark8
@pytest.mark.mark10
def test_sentence_str_ideal(sentence: Sentence) -> None:
    """
    Checks the __str__ method of Sentence

    Args:
        sentence (Sentence): An instance of Sentence
    """
    assert str(sentence) == "Sentence(text='Мама мыла раму', position=0)"


@pytest.mark.lab_4_summarization_textrank
@pytest.mark.mark8
@pytest.mark.mark10
def test_sentence_eq_ideal(sentence: Sentence) -> None:
    """
    Checks the __eq__ method of Sentence

    Args:
        sentence (Sentence): An instance of Sentence
    """
    assert sentence == Sentence("Мама мыла раму", 0)
    assert sentence != Sentence("Другая строка", 0)
    assert sentence != Sentence("Мама мыла раму", 1)


@pytest.mark.lab_4_summarization_textrank
@pytest.mark.mark8
@pytest.mark.mark10
def test_sentence_eq_incorrect_argument_error(
    sentence: Sentence, invalid_inputs: list[InvalidInput]
) -> None:
    """
    Checks that comparing Sentence with non-Sentence raises IncorrectArgumentError

    Args:
        sentence (Sentence): An instance of Sentence
        invalid_inputs (list[InvalidInput]): Invalid inputs
    """
    for invalid_input in invalid_inputs:
        with pytest.raises(IncorrectArgumentError):
            sentence == invalid_input  # pylint: disable=pointless-statement


@pytest.mark.lab_4_summarization_textrank
@pytest.mark.mark8
@pytest.mark.mark10
def test_sentence_hash_ideal(sentence: Sentence) -> None:
    """
    Checks the __hash__ method of Sentence

    Args:
        sentence (Sentence): An instance of Sentence
    """
    assert hash(sentence) == hash(Sentence("Мама мыла раму", 0))
    assert hash(sentence) != hash(Sentence("Мама мыла раму", 1))


@pytest.mark.lab_4_summarization_textrank
@pytest.mark.mark6
@pytest.mark.mark8
@pytest.mark.mark10
def test_sentence_initialization_incorrect_argument_error(
    invalid_inputs: list[InvalidInput],
) -> None:
    """
    Checks that invalid initialization arguments raise IncorrectArgumentError

    Args:
        invalid_inputs (list[InvalidInput]): Invalid inputs
    """
    text_inputs = [item for item in invalid_inputs if not isinstance(item, str)]
    position_inputs = [item for item in invalid_inputs if not isinstance(item, int)]
    for wrong_input in text_inputs:
        with pytest.raises(IncorrectArgumentError):
            Sentence(wrong_input, 0)
    for wrong_input in position_inputs:
        with pytest.raises(IncorrectArgumentError):
            Sentence("Мама мыла раму", wrong_input)
    for wrong_text, wrong_position in zip(text_inputs, position_inputs):
        with pytest.raises(IncorrectArgumentError):
            Sentence(wrong_text, wrong_position)


@pytest.mark.lab_4_summarization_textrank
@pytest.mark.mark6
@pytest.mark.mark8
@pytest.mark.mark10
def test_sentence_setting_getting_attributes(sentence: Sentence) -> None:
    """
    Checks setting and getting Sentence attributes

    Args:
        sentence (Sentence): An instance of Sentence
    """
    text1 = "Мама мыла раму"
    preprocessed = ("мама", "мыла", "раму")
    encoded = (1, 2, 3)

    assert sentence.get_text() == text1
    assert sentence.get_position() == 0

    sentence.set_preprocessed(preprocessed)
    assert isinstance(sentence.get_preprocessed(), tuple)
    assert sentence.get_preprocessed() == preprocessed

    sentence.set_encoded(encoded)
    assert isinstance(sentence.get_encoded(), tuple)
    assert sentence.get_encoded() == encoded


@pytest.mark.lab_4_summarization_textrank
@pytest.mark.mark6
@pytest.mark.mark8
@pytest.mark.mark10
def test_sentence_setting_attributes_incorrect_argument_error(
    sentence: Sentence, invalid_inputs: list[InvalidInput]
) -> None:
    """
    Checks that invalid attribute values raise IncorrectArgumentError

    Args:
        sentence (Sentence): An instance of Sentence
        invalid_inputs (list[InvalidInput]): Invalid inputs
    """
    preprocessed_wrong_inputs = [item for item in invalid_inputs if not isinstance(item, str)]
    encoded_wrong_inputs = [item for item in invalid_inputs if not isinstance(item, (list, tuple))]

    for preprocessed_wrong_input in preprocessed_wrong_inputs:
        with pytest.raises(IncorrectArgumentError):
            sentence.set_preprocessed(preprocessed_wrong_input)

    for encoded_wrong_input in encoded_wrong_inputs:
        with pytest.raises(IncorrectArgumentError):
            sentence.set_encoded(encoded_wrong_input)
