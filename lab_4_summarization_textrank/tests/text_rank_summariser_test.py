# pylint: disable=protected-access
"""
Checks the fourth lab TextRankSummarizer abstraction
"""

import pytest

from lab_4_summarization_textrank.main import (
    IncorrectArgumentError,
    NaiveSummarizer,
    Sentence,
    TextGraph,
    TextRankSummarizer,
)
from lab_4_summarization_textrank.tests.conftest import InvalidInput

EXTRACT = (
    "Он родился 9 марта 1934 года в городе Гжатске (ныне Гагарин) Смоленской области.\n",
    "В июне Гагарин с отличием окончил Саратовский индустриальный техникум, в "
    + "июле – совершил первый самостоятельный полет на самолете Як-18 и 10 октября "
    + "того же года окончил Саратовский аэроклуб.\n",
    "Юрий Алексеевич 7 октября 1955 года был призван в ряды Советской Армии и "
    + "направлен в город Оренбург на учебу в 1-е Чкаловское военно-авиационное "
    + "училище летчиков имени К.Е.Ворошилова.\n",
    "В конце 1957 года Гагарин прибыл к месту своего назначения – истребительный "
    + "авиационный полк Северного флота.\n",
    "Гагарин 9 декабря 1959 года написал заявление с просьбой зачислить его в "
    + "группу кандидатов в космонавты.\n",
    "В 9 часов 7 минут по московскому времени 12 апреля 1961 года с космодрома "
    + 'Байконур стартовал космический корабль "Восток" с пилотом–космонавтом Юрием '
    + "Алексеевичем Гагариным на борту.\n",
    "С 23 мая 1961 года Гагарин – командир отряда космонавтов.\n",
    "Но сделано это было уже без Юрия Гагарина. 17 февраля 1968 года он защитил "
    + "диплом в Академии имени Н.Е.Жуковского.\n",
    "С большим трудом добился разрешения самостоятельно пилотировать самолет. 27 "
    + "марта 1968 года был первый такой полет.\n",
    "Но чтобы не произошло в тот день, ясно только одно – погиб первый космонавт "
    + "планеты Земля Юрий Алексеевич Гагарин.",
)

SUMMARY = "".join(EXTRACT)


@pytest.mark.lab_4_summarization_textrank
@pytest.mark.mark10
def test_text_rank_inheritance() -> None:
    """
    Checks that TextRankSummarizer inherits from NaiveSummarizer
    """
    assert issubclass(TextRankSummarizer, NaiveSummarizer)


@pytest.mark.lab_4_summarization_textrank
@pytest.mark.mark10
def test_text_rank_initialization() -> None:
    """
    Checks TextRankSummarizer initialization
    """
    sim_graph = TextGraph()
    text_rank = TextRankSummarizer(sim_graph)
    for attribute in [
        "_graph",
        "_damping_factor",
        "_convergence_threshold",
        "_max_iter",
        "_scores",
    ]:
        assert hasattr(text_rank, attribute)
    assert text_rank._damping_factor == 0.85
    assert text_rank._convergence_threshold == 0.0001
    assert text_rank._max_iter == 50


@pytest.mark.lab_4_summarization_textrank
@pytest.mark.mark10
def test_text_rank_str_ideal() -> None:
    """
    Checks the __str__ method of TextRankSummarizer
    """
    sim_graph = TextGraph()
    text_rank = TextRankSummarizer(sim_graph)
    assert str(text_rank) == (
        f"TextRankSummarizer(graph={sim_graph}, "
        "damping_factor=0.85, convergence_threshold=0.0001, max_iter=50)"
    )


@pytest.mark.lab_4_summarization_textrank
@pytest.mark.mark10
def test_text_rank_len_ideal(graph: TextGraph) -> None:
    """
    Checks the __len__ method of TextRankSummarizer

    Args:
        graph (TextGraph): An instance of TextGraph
    """
    text_rank = TextRankSummarizer(graph)
    assert len(text_rank) == 0
    text_rank.train()
    assert len(text_rank) == len(graph)


@pytest.mark.lab_4_summarization_textrank
@pytest.mark.mark10
def test_text_rank_initialization_incorrect_argument_error(
    invalid_inputs: list[InvalidInput],
) -> None:
    """
    Checks that TextRankSummarizer initialization with invalid input raises IncorrectArgumentError

    Args:
        invalid_inputs (list[InvalidInput]): Invalid inputs
    """
    for wrong_input in invalid_inputs:
        with pytest.raises(IncorrectArgumentError):
            TextRankSummarizer(wrong_input)


@pytest.mark.lab_4_summarization_textrank
@pytest.mark.mark10
def test_text_rank_update_vertex_score_uses_documented_degree() -> None:
    """Checks the TextRank update against the documented degree denominator."""
    vertex = Sentence("vertex", 0)
    neighbor = Sentence("neighbor", 1)
    vertex.set_encoded((1, 2))
    neighbor.set_encoded((1, 3))
    graph = TextGraph()
    graph.build([vertex, neighbor])
    summarizer = TextRankSummarizer(graph)

    summarizer._update_vertex_score(vertex, [neighbor], {vertex: 1.0, neighbor: 2.0})

    assert summarizer._scores[vertex] == pytest.approx(1.85)


@pytest.mark.lab_4_summarization_textrank
@pytest.mark.mark10
def test_text_rank_does_not_count_self_as_neighbor() -> None:
    """Checks that a lone vertex receives only the base TextRank score."""
    vertex = Sentence("vertex", 0)
    vertex.set_encoded((1,))
    graph = TextGraph()
    graph.build([vertex])
    summarizer = TextRankSummarizer(graph)

    summarizer.train()

    assert summarizer._scores[vertex] == pytest.approx(0.15)


@pytest.mark.lab_4_summarization_textrank
@pytest.mark.mark10
def test_text_rank_update_vertex_score_incorrect_argument_error(
    graph: TextGraph, invalid_inputs: list[InvalidInput]
) -> None:
    """
    Checks that _update_vertex_score with invalid input raises IncorrectArgumentError

    Args:
        graph (TextGraph): An instance of TextGraph
        invalid_inputs (list[InvalidInput]): Invalid inputs
    """
    text_rank = TextRankSummarizer(graph)
    valid_vertex = graph.get_vertices()[0]
    valid_incidental = [valid_vertex]
    valid_scores = {valid_vertex: 1.0}
    for invalid_input in invalid_inputs:
        invalid_scores = {} if isinstance(invalid_input, dict) else invalid_input
        for args in (
            (invalid_input, valid_incidental, valid_scores),
            (valid_vertex, invalid_input, valid_scores),
            (valid_vertex, valid_incidental, invalid_scores),
            (invalid_input, invalid_input, invalid_input),
        ):
            with pytest.raises(IncorrectArgumentError):
                text_rank._update_vertex_score(*args)


@pytest.mark.lab_4_summarization_textrank
@pytest.mark.mark10
def test_ranking_pipeline(graph: TextGraph) -> None:
    """
    Checks TextRank sentence ranking pipeline

    Args:
        graph (TextGraph): An instance of TextGraph
    """
    text_rank = TextRankSummarizer(graph)
    text_rank.train()
    top = text_rank._get_top_n_sentences(10)
    assert isinstance(top, tuple)
    expected_positions = [7, 1, 8, 11, 27, 51, 12, 45, 47, 15]
    assert [sentence.get_position() for sentence in top] == expected_positions
    assert text_rank.summarize(10) == SUMMARY


@pytest.mark.lab_4_summarization_textrank
@pytest.mark.mark10
def test_text_rank_get_top_n_sentences_incorrect_argument_error(
    graph: TextGraph, invalid_inputs: list[InvalidInput]
) -> None:
    """
    Checks that _get_top_n_sentences with invalid input raises IncorrectArgumentError

    Args:
        graph (TextGraph): An instance of TextGraph
        invalid_inputs (list[InvalidInput]): Invalid inputs
    """
    text_rank = TextRankSummarizer(graph)
    wrong_inputs = [item for item in invalid_inputs if not isinstance(item, int)] + [0, -1]
    for invalid_input in wrong_inputs:
        with pytest.raises(IncorrectArgumentError):
            text_rank._get_top_n_sentences(invalid_input)
