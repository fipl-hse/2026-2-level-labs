# pylint: disable=protected-access
"""
Checks the fourth lab NaiveSummarizer abstraction
"""

import pytest

from lab_4_summarization_textrank.main import (
    IncorrectArgumentError,
    NaiveSummarizer,
    TextGraph,
)
from lab_4_summarization_textrank.tests.conftest import InvalidInput

EXTRACT = (
    "Юрий Алексеевич Гагарин является первым космонавтом земли.\n",
    "Он родился 9 марта 1934 года в городе Гжатске (ныне Гагарин) Смоленской области.\n",
    "В июне Гагарин с отличием окончил Саратовский индустриальный техникум, в "
    + "июле – совершил первый самостоятельный полет на самолете Як-18 и 10 октября "
    + "того же года окончил Саратовский аэроклуб.\n",
    "В конце 1957 года Гагарин прибыл к месту своего назначения – истребительный "
    + "авиационный полк Северного флота.\n",
    "Гагарин 9 декабря 1959 года написал заявление с просьбой зачислить его в "
    + "группу кандидатов в космонавты.\n",
    "Уже в конце апреля Юрий Гагарин отправился в свою первую зарубежную поездку.\n",
    "С 23 мая 1961 года Гагарин – командир отряда космонавтов.\n",
    "Одним из тех, кто стал готовиться к полету на Луну, стал и Гагарин.\n",
    "К нему готовились Владимир Михайлович Комаров и Юрий Алексеевич Гагарин.\n",
    "Но чтобы не произошло в тот день, ясно только одно – погиб первый космонавт "
    + "планеты Земля Юрий Алексеевич Гагарин.",
)

SUMMARY = "".join(EXTRACT)


@pytest.mark.lab_4_summarization_textrank
@pytest.mark.mark8
@pytest.mark.mark10
def test_naive_summarizer_initialization_incorrect_argument_error(
    invalid_inputs: list[InvalidInput],
) -> None:
    """
    Checks that NaiveSummarizer initialization with invalid input raises IncorrectArgumentError

    Args:
        invalid_inputs (list[InvalidInput]): Invalid inputs
    """
    for wrong_input in invalid_inputs:
        with pytest.raises(IncorrectArgumentError):
            NaiveSummarizer(wrong_input)


@pytest.mark.lab_4_summarization_textrank
@pytest.mark.mark8
@pytest.mark.mark10
def test_naive_summarizer_initialization_ideal() -> None:
    """
    Checks NaiveSummarizer initialization
    """
    sim_graph = TextGraph()
    summarizer = NaiveSummarizer(sim_graph)
    assert hasattr(summarizer, "_graph")
    assert summarizer._graph is sim_graph


@pytest.mark.lab_4_summarization_textrank
@pytest.mark.mark8
@pytest.mark.mark10
def test_naive_summarizer_str_ideal() -> None:
    """
    Checks the __str__ method of NaiveSummarizer
    """
    sim_graph = TextGraph()
    summarizer = NaiveSummarizer(sim_graph)
    assert str(summarizer) == f"NaiveSummarizer(graph={sim_graph})"


@pytest.mark.lab_4_summarization_textrank
@pytest.mark.mark8
@pytest.mark.mark10
def test_naive_summarizer_get_top_sentences(graph: TextGraph) -> None:
    """
    Checks NaiveSummarizer sentence ranking pipeline

    Args:
        graph (TextGraph): An instance of TextGraph
    """
    summarizer = NaiveSummarizer(graph)
    top = summarizer._get_top_n_sentences(10)
    assert isinstance(top, tuple)
    assert len(top) == 10


@pytest.mark.lab_4_summarization_textrank
@pytest.mark.mark8
@pytest.mark.mark10
def test_get_top_n_sentences_incorrect_argument_error(
    graph: TextGraph, invalid_inputs: list[InvalidInput]
) -> None:
    """
    Checks that _get_top_n_sentences with invalid input raises IncorrectArgumentError

    Args:
        graph (TextGraph): An instance of TextGraph
        invalid_inputs (list[InvalidInput]): Invalid inputs
    """
    summarizer = NaiveSummarizer(graph)
    wrong_inputs = [item for item in invalid_inputs if not isinstance(item, int)] + [0, -1]
    for wrong_input in wrong_inputs:
        with pytest.raises(IncorrectArgumentError):
            summarizer._get_top_n_sentences(wrong_input)


@pytest.mark.lab_4_summarization_textrank
@pytest.mark.mark8
@pytest.mark.mark10
def test_summarize(graph: TextGraph) -> None:
    """
    Checks summary generation from top-ranked sentences

    Args:
        graph (TextGraph): An instance of TextGraph
    """
    summarizer = NaiveSummarizer(graph)
    summary = summarizer.summarize(10)
    assert isinstance(summary, str)
    assert len(summary.split("\n")) == 10


@pytest.mark.lab_4_summarization_textrank
@pytest.mark.mark8
@pytest.mark.mark10
def test_summarize_incorrect_argument_error(
    graph: TextGraph, invalid_inputs: list[InvalidInput]
) -> None:
    """
    Checks that summarize with invalid input raises IncorrectArgumentError

    Args:
        graph (TextGraph): An instance of TextGraph
        invalid_inputs (list[InvalidInput]): Invalid inputs
    """
    summarizer = NaiveSummarizer(graph)
    wrong_inputs = [item for item in invalid_inputs if not isinstance(item, int)] + [0, -1]
    for wrong_input in wrong_inputs:
        with pytest.raises(IncorrectArgumentError):
            summarizer.summarize(wrong_input)
