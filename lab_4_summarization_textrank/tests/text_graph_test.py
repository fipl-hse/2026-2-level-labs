# pylint: disable=protected-access
"""
Checks the fourth lab TextGraph abstraction
"""

from collections import Counter

import pytest

from lab_4_summarization_textrank.main import (
    IncorrectArgumentError,
    Sentence,
    TextGraph,
    TextGraphError,
)
from lab_4_summarization_textrank.tests.conftest import InvalidInput


@pytest.mark.lab_4_summarization_textrank
@pytest.mark.mark8
@pytest.mark.mark10
def test_similarity_graph_initialization() -> None:
    """
    Checks TextGraph initialization and its attributes
    """
    matrix = TextGraph()
    assert hasattr(matrix, "_matrix")
    assert isinstance(matrix._matrix, list)


@pytest.mark.lab_4_summarization_textrank
@pytest.mark.mark8
@pytest.mark.mark10
def test_text_graph_str_ideal() -> None:
    """
    Checks the __str__ method of TextGraph
    """
    matrix = TextGraph()
    assert str(matrix) == "TextGraph(vertices=0)"


@pytest.mark.lab_4_summarization_textrank
@pytest.mark.mark8
@pytest.mark.mark10
def test_fill_from_single_sentence() -> None:
    """Checks that a sentence without graph edges is still included as a vertex."""
    sentence = Sentence("only sentence", 0)
    sentence.set_encoded((1000,))
    graph = TextGraph()

    graph.build([sentence])

    assert graph.get_vertices() == (sentence,)


@pytest.mark.lab_4_summarization_textrank
@pytest.mark.mark8
@pytest.mark.mark10
def test_fill_from_duplicate_sentences() -> None:
    """Checks that identical sentences remain distinct positional vertices."""
    first = Sentence("same", 0)
    second = Sentence("same", 1)
    first.set_encoded((1000,))
    second.set_encoded((1000,))
    graph = TextGraph()

    graph.build([first, second])

    assert graph.get_vertices() == (first, second)


@pytest.mark.lab_4_summarization_textrank
@pytest.mark.mark8
@pytest.mark.mark10
def test_build_invalid_input(invalid_inputs: list[InvalidInput]) -> None:
    """
    Checks that invalid input to build raises IncorrectArgumentError

    Args:
        invalid_inputs (list[InvalidInput]): Invalid inputs
    """
    matrix = TextGraph()
    for invalid_input in invalid_inputs:
        with pytest.raises(IncorrectArgumentError):
            matrix.build(invalid_input)


@pytest.mark.lab_4_summarization_textrank
@pytest.mark.mark8
@pytest.mark.mark10
def test_add_edge_ideal(matrix_sentences: list[Sentence]) -> None:
    """
    Checks adding edges between valid sentence vertices

    Args:
        matrix_sentences (list[Sentence]): Preprocessed and encoded sentences
    """
    matrix = TextGraph()
    matrix._add_edge(matrix_sentences[0], matrix_sentences[1])
    matrix._add_edge(matrix_sentences[0], matrix_sentences[2])
    matrix._add_edge(matrix_sentences[1], matrix_sentences[2])
    matrix._add_edge(matrix_sentences[3], matrix_sentences[0])
    assert len(matrix._matrix) == 4


@pytest.mark.lab_4_summarization_textrank
@pytest.mark.mark8
@pytest.mark.mark10
def test_add_edge_incorrect_argument_error(
    matrix_sentences: list[Sentence], invalid_inputs: list[InvalidInput]
) -> None:
    """
    Checks that invalid vertices raise IncorrectArgumentError when adding an edge

    Args:
        matrix_sentences (list[Sentence]): Preprocessed and encoded sentences
        invalid_inputs (list[InvalidInput]): Invalid inputs
    """
    matrix = TextGraph()
    valid_vertex = matrix_sentences[0]
    for invalid_input in invalid_inputs:
        with pytest.raises(IncorrectArgumentError):
            matrix._add_edge(invalid_input, valid_vertex)
        with pytest.raises(IncorrectArgumentError):
            matrix._add_edge(valid_vertex, invalid_input)
        with pytest.raises(IncorrectArgumentError):
            matrix._add_edge(invalid_input, invalid_input)


@pytest.mark.lab_4_summarization_textrank
@pytest.mark.mark8
@pytest.mark.mark10
def test_get_similarity_score_ideal(matrix_sentences: list[Sentence]) -> None:
    """
    Checks similarity scores between sentence vertices

    Args:
        matrix_sentences (list[Sentence]): Preprocessed and encoded sentences
    """
    matrix = TextGraph()
    matrix.build(matrix_sentences)

    expected_scores = (
        (matrix_sentences[0], matrix_sentences[1], 0.5),
        (matrix_sentences[1], matrix_sentences[2], 0.2),
        (matrix_sentences[3], matrix_sentences[0], 1 / 6),
        (matrix_sentences[1], matrix_sentences[3], 0.4),
        (matrix_sentences[0], matrix_sentences[2], 0.0),
    )
    for first_sentence, second_sentence, expected in expected_scores:
        assert matrix.get_similarity_score(first_sentence, second_sentence) == pytest.approx(
            expected
        )


@pytest.mark.lab_4_summarization_textrank
@pytest.mark.mark8
@pytest.mark.mark10
def test_get_similarity_score_incorrect_argument_error(
    matrix_sentences: list[Sentence], invalid_inputs: list[InvalidInput]
) -> None:
    """
    Checks that invalid vertices raise IncorrectArgumentError when getting a similarity score

    Args:
        matrix_sentences (list[Sentence]): Preprocessed and encoded sentences
        invalid_inputs (list[InvalidInput]): Invalid inputs
    """
    matrix = TextGraph()
    matrix.build(matrix_sentences)
    valid_vertex = matrix_sentences[0]
    for invalid_input in invalid_inputs:
        with pytest.raises(IncorrectArgumentError):
            matrix.get_similarity_score(invalid_input, valid_vertex)
        with pytest.raises(IncorrectArgumentError):
            matrix.get_similarity_score(valid_vertex, invalid_input)
        with pytest.raises(IncorrectArgumentError):
            matrix.get_similarity_score(invalid_input, invalid_input)


@pytest.mark.lab_4_summarization_textrank
@pytest.mark.mark8
@pytest.mark.mark10
def test_get_similarity_score_nonexistent_vertex(matrix_sentences: list[Sentence]) -> None:
    """
    Checks that a nonexistent vertex raises TextGraphError when getting a similarity score

    Args:
        matrix_sentences (list[Sentence]): Preprocessed and encoded sentences
    """
    matrix = TextGraph()
    with pytest.raises(TextGraphError):
        matrix.get_similarity_score(matrix_sentences[0], matrix_sentences[2])
    matrix._add_vertex(matrix_sentences[0])
    with pytest.raises(TextGraphError):
        matrix.get_similarity_score(matrix_sentences[0], matrix_sentences[2])
    with pytest.raises(TextGraphError):
        matrix.get_similarity_score(matrix_sentences[2], matrix_sentences[0])


@pytest.mark.lab_4_summarization_textrank
@pytest.mark.mark8
@pytest.mark.mark10
def test_add_edge_cannot_add_loops(matrix_sentences: list[Sentence]) -> None:
    """
    Checks that adding an edge from a vertex to itself raises TextGraphError

    Args:
        matrix_sentences (list[Sentence]): Preprocessed and encoded sentences
    """
    matrix = TextGraph()
    with pytest.raises(TextGraphError):
        matrix._add_edge(matrix_sentences[0], matrix_sentences[0])


@pytest.mark.lab_4_summarization_textrank
@pytest.mark.mark8
@pytest.mark.mark10
def test_get_vertices(matrix_sentences: list[Sentence]) -> None:
    """
    Checks retrieval of all vertices from the similarity graph

    Args:
        matrix_sentences (list[Sentence]): Preprocessed and encoded sentences
    """
    matrix = TextGraph()
    matrix.build(matrix_sentences)
    assert isinstance(matrix.get_vertices(), tuple)
    assert Counter(matrix_sentences) == Counter(matrix.get_vertices())


@pytest.mark.lab_4_summarization_textrank
@pytest.mark.mark10
def test_fill_from_sentences(matrix_sentences: list[Sentence]) -> None:
    """
    Checks filling the similarity graph from a sequence of sentences

    Args:
        matrix_sentences (list[Sentence]): Preprocessed and encoded sentences
    """
    matrix = TextGraph()
    matrix.build(matrix_sentences)
    assert len(matrix.get_vertices()) == 4


@pytest.mark.lab_4_summarization_textrank
@pytest.mark.mark8
@pytest.mark.mark10
def test_get_top_n_sentences(matrix_sentences: list[Sentence]) -> None:
    """
    Checks retrieval of top n sentences from TextGraph

    Args:
        matrix_sentences (list[Sentence]): Preprocessed and encoded sentences
    """
    matrix = TextGraph()
    matrix.build(matrix_sentences)
    top = matrix.get_top_n_sentences(2)
    expected = (matrix_sentences[1], matrix_sentences[3])
    assert isinstance(top, tuple)
    assert len(top) == 2
    assert top == expected


@pytest.mark.lab_4_summarization_textrank
@pytest.mark.mark8
@pytest.mark.mark10
def test_get_top_n_sentences_invalid_input(
    matrix_sentences: list[Sentence], invalid_inputs: list[InvalidInput]
) -> None:
    """
    Checks that invalid n raises IncorrectArgumentError in get_top_n_sentences

    Args:
        matrix_sentences (list[Sentence]): Preprocessed and encoded sentences
        invalid_inputs (list[InvalidInput]): Invalid inputs
    """
    matrix = TextGraph()
    matrix.build(matrix_sentences)
    wrong_inputs = [item for item in invalid_inputs if not isinstance(item, int)] + [0, -1]
    for invalid_input in wrong_inputs:
        with pytest.raises(IncorrectArgumentError):
            matrix.get_top_n_sentences(invalid_input)


@pytest.mark.lab_4_summarization_textrank
@pytest.mark.mark8
@pytest.mark.mark10
def test_get_top_n_sentences_empty_graph() -> None:
    """
    Checks that get_top_n_sentences on an empty graph raises TextGraphError
    """
    matrix = TextGraph()
    with pytest.raises(TextGraphError):
        matrix.get_top_n_sentences(1)


@pytest.mark.lab_4_summarization_textrank
@pytest.mark.mark8
@pytest.mark.mark10
def test_add_vertex_incorrect_argument_error(invalid_inputs: list[InvalidInput]) -> None:
    """
    Checks that invalid input to _add_vertex raises IncorrectArgumentError

    Args:
        invalid_inputs (list[InvalidInput]): Invalid inputs
    """
    matrix = TextGraph()
    for invalid_input in invalid_inputs:
        with pytest.raises(IncorrectArgumentError):
            matrix._add_vertex(invalid_input)


@pytest.mark.lab_4_summarization_textrank
@pytest.mark.mark8
@pytest.mark.mark10
def test_add_vertex_duplicate_ideal(matrix_sentences: list[Sentence]) -> None:
    """
    Checks that adding a duplicate vertex does not duplicate it in the graph

    Args:
        matrix_sentences (list[Sentence]): Preprocessed and encoded sentences
    """
    matrix = TextGraph()
    matrix._add_vertex(matrix_sentences[0])
    matrix._add_vertex(matrix_sentences[0])
    assert len(matrix.get_vertices()) == 1


@pytest.mark.lab_4_summarization_textrank
@pytest.mark.mark8
@pytest.mark.mark10
def test_text_graph_len_ideal(matrix_sentences: list[Sentence]) -> None:
    """
    Checks the __len__ method of TextGraph

    Args:
        matrix_sentences (list[Sentence]): Preprocessed and encoded sentences
    """
    matrix = TextGraph()
    assert len(matrix) == 0
    matrix.build(matrix_sentences)
    assert len(matrix) == len(matrix_sentences)


@pytest.mark.lab_4_summarization_textrank
@pytest.mark.mark10
def test_calculate_inout_score(matrix_sentences: list[Sentence]) -> None:
    """
    Checks calculation of the number of similar vertices

    Args:
        matrix_sentences (list[Sentence]): Preprocessed and encoded sentences
    """
    matrix = TextGraph()
    matrix.build(matrix_sentences)
    expected = (2, 3, 2, 3)
    for sentence, score in zip(matrix_sentences, expected):
        assert matrix.calculate_inout_score(sentence) == score


@pytest.mark.lab_4_summarization_textrank
@pytest.mark.mark10
def test_calculate_inout_score_isolated_vertex() -> None:
    """
    Checks score calculation for a single vertex
    """
    sentence = Sentence("only sentence", 0)
    sentence.set_encoded((1000,))
    graph = TextGraph()
    graph.build([sentence])
    assert graph.calculate_inout_score(sentence) == 0


@pytest.mark.lab_4_summarization_textrank
@pytest.mark.mark10
def test_calculate_inout_score_nonexistent_vertex(matrix_sentences: list[Sentence]) -> None:
    """
    Checks that a nonexistent vertex raises TextGraphError when calculating its score

    Args:
        matrix_sentences (list[Sentence]): Preprocessed and encoded sentences
    """
    matrix = TextGraph()
    with pytest.raises(TextGraphError):
        matrix.calculate_inout_score(matrix_sentences[0])


@pytest.mark.lab_4_summarization_textrank
@pytest.mark.mark10
def test_calculate_inout_score_invalid_input(
    matrix_sentences: list[Sentence], invalid_inputs: list[InvalidInput]
) -> None:
    """
    Checks that invalid vertices raise IncorrectArgumentError when calculating their score

    Args:
        matrix_sentences (list[Sentence]): Preprocessed and encoded sentences
        invalid_inputs (list[InvalidInput]): Invalid inputs
    """
    matrix = TextGraph()
    matrix.build(matrix_sentences)
    for invalid_input in invalid_inputs:
        with pytest.raises(IncorrectArgumentError):
            matrix.calculate_inout_score(invalid_input)
