"""
Checks the fourth lab SentencePreprocessor abstraction
"""

# pylint: disable=protected-access, duplicate-code
import string

import pytest

from lab_4_summarization_textrank.main import IncorrectArgumentError, Sentence, SentencePreprocessor
from lab_4_summarization_textrank.tests.conftest import InvalidInput

TEXT = (
    "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor "
    "incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud "
    "exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure "
    "dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. "
    "Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit "
    "anim id est laborum."
)

SENTENCES = [
    "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor "
    "incididunt ut labore et dolore magna aliqua.",
    "Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea "
    "commodo consequat.",
    "Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat "
    "nulla pariatur.",
    "Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit "
    "anim id est laborum.",
]

PREPROCESSED_SENTENCES = [
    (
        "lorem",
        "ipsum",
        "dolor",
        "sit",
        "amet",
        "consectetur",
        "adipiscing",
        "elit",
        "eiusmod",
        "tempor",
        "incididunt",
        "labore",
        "dolore",
        "magna",
        "aliqua",
    ),
    (
        "enim",
        "ad",
        "minim",
        "veniam",
        "quis",
        "nostrud",
        "exercitation",
        "ullamco",
        "laboris",
        "nisi",
        "aliquip",
        "commodo",
        "consequat",
    ),
    (
        "duis",
        "aute",
        "irure",
        "dolor",
        "reprehenderit",
        "voluptate",
        "velit",
        "cillum",
        "dolore",
        "eu",
        "fugiat",
        "nulla",
        "pariatur",
    ),
    (
        "excepteur",
        "sint",
        "occaecat",
        "cupidatat",
        "proident",
        "sunt",
        "culpa",
        "officia",
        "deserunt",
        "mollit",
        "anim",
        "id",
        "laborum",
    ),
]


@pytest.mark.lab_4_summarization_textrank
@pytest.mark.mark6
@pytest.mark.mark8
@pytest.mark.mark10
def test_sentence_preprocessor_initialization_ideal() -> None:
    """
    Checks SentencePreprocessor initialization and its attributes
    """
    stop_words = ("and", "of", "the")
    punctuation = (",", "!", "?")
    preprocessor = SentencePreprocessor(stop_words, punctuation)

    for attribute in ["_stop_words", "_punctuation"]:
        assert hasattr(
            preprocessor, attribute
        ), f"Sentence preprocessor misses {attribute} attribute"


@pytest.mark.lab_4_summarization_textrank
@pytest.mark.mark6
@pytest.mark.mark8
@pytest.mark.mark10
def test_sentence_preprocessor_str_ideal() -> None:
    """
    Checks the __str__ method of SentencePreprocessor
    """
    stop_words = ("and", "of", "the")
    punctuation = (",", "!", "?")
    preprocessor = SentencePreprocessor(stop_words, punctuation)
    assert str(preprocessor) == "SentencePreprocessor(stop_words=3, punctuation=3)"


@pytest.mark.lab_4_summarization_textrank
@pytest.mark.mark6
@pytest.mark.mark8
@pytest.mark.mark10
def test_sentence_preprocessor_initialization_incorrect_argument_error(
    invalid_inputs: list[InvalidInput],
) -> None:
    """
    Checks that invalid initialization arguments raise IncorrectArgumentError

    Args:
        invalid_inputs (list[InvalidInput]): Invalid inputs
    """
    wrong_inputs = [item for item in invalid_inputs if not isinstance(item, str)]
    for wrong_input in wrong_inputs:
        with pytest.raises(IncorrectArgumentError):
            SentencePreprocessor(wrong_input, ("1", "2", "3"))
        with pytest.raises(IncorrectArgumentError):
            SentencePreprocessor(("1", "2", "3"), wrong_input)
        with pytest.raises(IncorrectArgumentError):
            SentencePreprocessor(wrong_input, wrong_input)


@pytest.mark.lab_4_summarization_textrank
@pytest.mark.mark6
@pytest.mark.mark8
@pytest.mark.mark10
def test_split_by_sentence_ideal() -> None:
    """
    Checks splitting text into sentences
    """
    preprocessor = SentencePreprocessor((), tuple(string.punctuation))
    output = preprocessor._split_by_sentence(TEXT)
    assert isinstance(output, tuple)
    for index, sentence in enumerate(output):
        assert SENTENCES[index] == sentence.get_text()


@pytest.mark.lab_4_summarization_textrank
@pytest.mark.mark6
@pytest.mark.mark8
@pytest.mark.mark10
def test_split_by_sentence_incorrect_argument_error(invalid_inputs: list[InvalidInput]) -> None:
    """
    Checks that invalid input to _split_by_sentence raises IncorrectArgumentError

    Args:
        invalid_inputs (list[InvalidInput]): Invalid inputs
    """
    preprocessor = SentencePreprocessor((), tuple(string.punctuation))
    wrong_inputs = [item for item in invalid_inputs if not isinstance(item, str)]
    for wrong_input in wrong_inputs:
        with pytest.raises(IncorrectArgumentError):
            preprocessor._split_by_sentence(wrong_input)


@pytest.mark.lab_4_summarization_textrank
@pytest.mark.mark6
@pytest.mark.mark8
@pytest.mark.mark10
def test_get_sentences_incorrect_argument_error(invalid_inputs: list[InvalidInput]) -> None:
    """
    Checks that invalid input to get_sentences raises IncorrectArgumentError

    Args:
        invalid_inputs (list[InvalidInput]): Invalid inputs
    """
    stop_words = ("sed", "ex", "ut", "est", "non", "in", "qui", "esse", "ea", "et", "do")
    preprocessor = SentencePreprocessor(stop_words, tuple(string.punctuation))
    wrong_inputs = [item for item in invalid_inputs if not isinstance(item, str)]
    for wrong_input in wrong_inputs:
        with pytest.raises(IncorrectArgumentError):
            preprocessor.get_sentences(wrong_input)


@pytest.mark.lab_4_summarization_textrank
@pytest.mark.mark6
@pytest.mark.mark8
@pytest.mark.mark10
def test_preprocess_sentences_incorrect_argument_error(invalid_inputs: list[InvalidInput]) -> None:
    """
    Checks that invalid input to _preprocess_sentences raises IncorrectArgumentError

    Args:
        invalid_inputs (list[InvalidInput]): Invalid inputs
    """
    stop_words = ("sed", "ex", "ut", "est", "non", "in", "qui", "esse", "ea", "et", "do")
    preprocessor = SentencePreprocessor(stop_words, tuple(string.punctuation))
    for invalid_input in invalid_inputs + [SENTENCES]:
        with pytest.raises(IncorrectArgumentError):
            preprocessor._preprocess_sentences(invalid_input)


@pytest.mark.lab_4_summarization_textrank
@pytest.mark.mark6
@pytest.mark.mark8
@pytest.mark.mark10
def test_get_sentences_ideal() -> None:
    """
    Checks sentence extraction and preprocessing
    """
    stop_words = ("sed", "ex", "ut", "est", "non", "in", "qui", "esse", "ea", "et", "do")
    preprocessor = SentencePreprocessor(
        stop_words,
        tuple(string.punctuation)
        + tuple(
            "”",
        ),
    )
    output = preprocessor.get_sentences(TEXT)
    assert isinstance(output, tuple)
    for index, sentence in enumerate(output):
        assert PREPROCESSED_SENTENCES[index] == sentence.get_preprocessed()


@pytest.mark.lab_4_summarization_textrank
@pytest.mark.mark6
@pytest.mark.mark8
@pytest.mark.mark10
def test_preprocess_sentences_ideal() -> None:
    """
    Checks preprocessing of a sequence of sentences
    """
    stop_words = ("sed", "ex", "ut", "est", "non", "in", "qui", "esse", "ea", "et", "do")
    preprocessor = SentencePreprocessor(
        stop_words,
        tuple(string.punctuation)
        + tuple(
            "”",
        ),
    )
    sentences = tuple(Sentence(sentence, position) for position, sentence in enumerate(SENTENCES))
    preprocessor._preprocess_sentences(sentences)
    for index, sentence in enumerate(sentences):
        assert PREPROCESSED_SENTENCES[index] == sentence.get_preprocessed()


@pytest.mark.lab_4_summarization_textrank
@pytest.mark.mark6
@pytest.mark.mark8
@pytest.mark.mark10
def test_preprocess_text_ideal() -> None:
    """
    Checks preprocessing raw text
    """
    text = "Во времена, Советского Союза."
    preprocessor = SentencePreprocessor(stop_words=("во",), punctuation=(",", ".", "/"))
    preprocessed = preprocessor.preprocess_text(text)
    assert isinstance(preprocessed, tuple)
    assert preprocessed == ("времена", "советского", "союза")


@pytest.mark.lab_4_summarization_textrank
@pytest.mark.mark6
@pytest.mark.mark8
@pytest.mark.mark10
def test_preprocess_text_no_punctuation() -> None:
    """
    Checks preprocessing text without punctuation removal
    """
    text = "Во времена, Советского Союза."
    preprocessor = SentencePreprocessor(stop_words=("во",), punctuation=())
    preprocessed = preprocessor.preprocess_text(text)
    assert isinstance(preprocessed, tuple)
    assert preprocessed == ("времена,", "советского", "союза.")


@pytest.mark.lab_4_summarization_textrank
@pytest.mark.mark6
@pytest.mark.mark8
@pytest.mark.mark10
def test_clean_and_tokenize_ideal() -> None:
    """
    Checks cleaning and tokenizing text
    """
    preprocessor = SentencePreprocessor((), (",", "."))
    tokens = preprocessor._clean_and_tokenize("Мама, мыла раму.")
    assert isinstance(tokens, tuple)
    assert tokens == ("мама", "мыла", "раму")


@pytest.mark.lab_4_summarization_textrank
@pytest.mark.mark6
@pytest.mark.mark8
@pytest.mark.mark10
def test_clean_and_tokenize_invalid_input(invalid_inputs: list[InvalidInput]) -> None:
    """
    Checks that invalid text input in _clean_and_tokenize raises IncorrectArgumentError

    Args:
        invalid_inputs (list[InvalidInput]): Invalid inputs
    """
    preprocessor = SentencePreprocessor((), ())
    wrong_inputs = [item for item in invalid_inputs if not isinstance(item, str)]
    for invalid_input in wrong_inputs:
        with pytest.raises(IncorrectArgumentError):
            preprocessor._clean_and_tokenize(invalid_input)


@pytest.mark.lab_4_summarization_textrank
@pytest.mark.mark6
@pytest.mark.mark8
@pytest.mark.mark10
def test_remove_stop_words_ideal() -> None:
    """
    Checks removing stop words from tokens
    """
    preprocessor = SentencePreprocessor(("a", "the"), ())
    tokens = ("a", "quick", "brown", "fox", "the")
    filtered = preprocessor._remove_stop_words(tokens)
    assert isinstance(filtered, tuple)
    assert filtered == ("quick", "brown", "fox")


@pytest.mark.lab_4_summarization_textrank
@pytest.mark.mark6
@pytest.mark.mark8
@pytest.mark.mark10
def test_remove_stop_words_invalid_input(invalid_inputs: list[InvalidInput]) -> None:
    """
    Checks that invalid tokens input in _remove_stop_words raises IncorrectArgumentError

    Args:
        invalid_inputs (list[InvalidInput]): Invalid inputs
    """
    preprocessor = SentencePreprocessor((), ())
    wrong_inputs = [item for item in invalid_inputs if not isinstance(item, str)]
    for invalid_input in wrong_inputs:
        with pytest.raises(IncorrectArgumentError):
            preprocessor._remove_stop_words(invalid_input)


@pytest.mark.lab_4_summarization_textrank
@pytest.mark.mark6
@pytest.mark.mark8
@pytest.mark.mark10
def test_preprocess_text_invalid_input(invalid_inputs: list[InvalidInput]) -> None:
    """
    Checks that invalid text input in preprocess_text raises IncorrectArgumentError

    Args:
        invalid_inputs (list[InvalidInput]): Invalid inputs
    """
    preprocessor = SentencePreprocessor((), ())
    wrong_inputs = [item for item in invalid_inputs if not isinstance(item, str)]
    for invalid_input in wrong_inputs:
        with pytest.raises(IncorrectArgumentError):
            preprocessor.preprocess_text(invalid_input)


@pytest.mark.lab_4_summarization_textrank
@pytest.mark.mark6
@pytest.mark.mark8
@pytest.mark.mark10
def test_preprocess_text_empty_input() -> None:
    """
    Checks preprocessing empty text
    """
    preprocessor = SentencePreprocessor(stop_words=(), punctuation=(",", "."))
    empty_result = preprocessor.preprocess_text("")
    assert isinstance(empty_result, tuple)
    assert not empty_result


@pytest.mark.lab_4_summarization_textrank
@pytest.mark.mark6
@pytest.mark.mark8
@pytest.mark.mark10
def test_remove_stop_words_empty_input() -> None:
    """
    Checks removing stop words from empty tokens
    """
    preprocessor = SentencePreprocessor(stop_words=(), punctuation=())
    empty_result = preprocessor._remove_stop_words(())
    assert isinstance(empty_result, tuple)
    assert not empty_result
