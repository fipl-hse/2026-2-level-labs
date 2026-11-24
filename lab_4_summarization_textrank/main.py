"""
Lab 4
Summarize text using TextRank algorithm

.. py:class:: EncodedSentence

   Type alias representing an encoded sentence as a tuple of integers.

.. py:class:: PreprocessedSentence

   Type alias representing a preprocessed sentence as a tuple of strings.
"""

import re

# pylint:disable=too-few-public-methods, unused-argument, super-init-not-called
from typing import Sequence

PreprocessedSentence = tuple[str, ...]
EncodedSentence = tuple[int, ...]


class IncorrectArgumentError(ValueError):
    """Raised when a provided input has an invalid type or value."""


class TextGraphError(IncorrectArgumentError):
    """Raised when an invalid graph operation or vertex lookup occurs."""


class Sentence:
    """
    An abstraction over a real-world sentence.

    Attributes:
        _text (str): The text of the sentence.
        _position (int): The position of the sentence in the text.
        _preprocessed (PreprocessedSentence): Preprocessed representation of the sentence.
        _encoded (EncodedSentence): Encoded representation of the sentence.
    """

    def __init__(self, text: str, position: int) -> None:
        """
        Initializes a sentence with its text and position.

        Args:
            text (str): Text of the sentence.
            position (int): Position of the sentence in the text.
        """
        if not isinstance(text, str) or not isinstance(position, int) or isinstance(position, bool):
            raise IncorrectArgumentError("Incorrect input value")
        self._text = text
        self._position = position
        self._preprocessed = tuple()
        self._encoded = tuple()

    def __eq__(self, other: object) -> bool:
        """
        Checks equality between two Sentence instances.

        Args:
            other (object): Another object to compare.

        Returns:
            bool: True if both are Sentence instances with the same text and position,
              otherwise False.
        """
        return isinstance(other, Sentence) and (self._text, self._position) == (
            other._text, other._position
        )

    def __hash__(self) -> int:
        """
        Returns a hash value for the Sentence instance.

        Returns:
            int: Hash value based on the text and position.
        """
        return hash((self._text, self._position))

    def __str__(self) -> str:
        """
        Returns a string representation of the sentence.

        Returns:
            str: String representation of the sentence.
        """
        return f"Sentence(text={self._text!r}, position={self._position})"

    def get_encoded(self) -> EncodedSentence:
        """
        Returns the encoded representation of the sentence.

        Returns:
            EncodedSentence: Encoded sequence of integers.
        """
        return self._encoded

    def get_position(self) -> int:
        """
        Returns the position of the sentence in the text.

        Returns:
            int: Position of the sentence.
        """
        return self._position


    def get_preprocessed(self) -> PreprocessedSentence:
        """
        Returns the preprocessed representation of the sentence.

        Returns:
            PreprocessedSentence: Preprocessed sequence of tokens.
        """
        return self._preprocessed

    def get_text(self) -> str:
        """
        Returns the text of the sentence.

        Returns:
            str: Text of the sentence.
        """
        return self._text

    def set_encoded(self, encoded_sentence: EncodedSentence) -> None:
        """
        Sets the encoded representation of the sentence.

        Args:
            encoded_sentence (EncodedSentence): Encoded sequence of integers.
        """
        if (
            not isinstance(encoded_sentence, Sequence)
            or isinstance(encoded_sentence, (str, bytes, bytearray))
            or any(
                not isinstance(value, int) or isinstance(value, bool)
                for value in encoded_sentence
            )
        ):
            raise IncorrectArgumentError("Incorrect input value")
        self._encoded = tuple(encoded_sentence)

    def set_preprocessed(self, preprocessed_sentence: PreprocessedSentence) -> None:
        """
        Sets the preprocessed representation of the sentence.

        Args:
            preprocessed_sentence (PreprocessedSentence): Preprocessed sequence of tokens.
        """
        if (
            not isinstance(preprocessed_sentence, Sequence)
            or isinstance(preprocessed_sentence, (str, bytes, bytearray))
            or any(not isinstance(token, str) for token in preprocessed_sentence)
        ):
            raise IncorrectArgumentError("Incorrect input value")
        self._preprocessed = tuple(preprocessed_sentence)


class SentencePreprocessor:
    """
    Class for sentence preprocessing.

    Attributes:
        _stop_words (Sequence[str]): Insignificant words to remove from tokens.
        _punctuation (Sequence[str]): Punctuation symbols to remove during text cleaning.
    """

    def __init__(self, stop_words: Sequence[str], punctuation: Sequence[str]) -> None:
        """
        Initializes the text preprocessor.

        Args:
            stop_words (Sequence[str]): Insignificant words to remove from tokens.
            punctuation (Sequence[str]): Punctuation symbols to remove during text cleaning.
        """
        if (
            not isinstance(stop_words, Sequence)
            or isinstance(stop_words, (str, bytes, bytearray))
            or any(not isinstance(word, str) for word in stop_words)
        ):
            raise IncorrectArgumentError("Incorrect input value")
        if (
            not isinstance(punctuation, Sequence)
            or isinstance(punctuation, (str, bytes, bytearray))
            or any(not isinstance(symbol, str) for symbol in punctuation)
        ):
            raise IncorrectArgumentError("Incorrect input value")
        self._stop_words = tuple(stop_words)
        self._punctuation = tuple(punctuation)

    def __str__(self) -> str:
        """
        Returns a string representation of the preprocessor.

        Returns:
            str: String representation of the preprocessor.
        """
        return (
            f"SentencePreprocessor(stop_words={len(self._stop_words)}, "
            f"punctuation={len(self._punctuation)})"
        )

    def _clean_and_tokenize(self, text: str) -> tuple[str, ...]:
        """
        Removes punctuation, converts text to lowercase, and splits it into tokens.

        Args:
            text (str): Raw text.

        Returns:
            tuple[str, ...]: Clean lowercase tokens.
        """
        if not isinstance(text, str):
            raise IncorrectArgumentError("Incorrect input value")
        cleaned = "".join(char for char in text.lower() if char not in self._punctuation)
        return tuple(cleaned.split())

    def _preprocess_sentences(self, sentences: Sequence[Sentence]) -> None:
        """
        Preprocesses a sequence of sentences and stores their token representations.

        Args:
            sentences (Sequence[Sentence]): Sequence of sentences to preprocess.
        """
        if (
            not isinstance(sentences, Sequence)
            or isinstance(sentences, (str, bytes, bytearray))
            or any(not isinstance(sentence, Sentence) for sentence in sentences)
        ):
            raise IncorrectArgumentError("Incorrect input value")
        for sentence in sentences:
            sentence.set_preprocessed(self.preprocess_text(sentence.get_text()))

    def _remove_stop_words(self, tokens: Sequence[str]) -> tuple[str, ...]:
        """
        Removes stop words from a sequence of tokens.

        Args:
            tokens (Sequence[str]): Sequence of tokens containing stop words.

        Returns:
            tuple[str, ...]: Sequence of tokens without stop words.
        """
        if (
            not isinstance(tokens, Sequence)
            or isinstance(tokens, (str, bytes, bytearray))
            or any(not isinstance(token, str) for token in tokens)
        ):
            raise IncorrectArgumentError("Incorrect input value")
        return tuple(token for token in tokens if token not in self._stop_words)

    def _split_by_sentence(self, text: str) -> tuple[Sentence, ...]:
        """
        Splits the provided text into sentences.

        Args:
            text (str): Raw text to split.

        Returns:
            tuple[Sentence, ...]: Sequence of sentences extracted from the text.
        """
        if not isinstance(text, str):
            raise IncorrectArgumentError("Incorrect input value")
        normalized = " ".join(text.replace("\n", " ").split())
        parts = re.split(r"(?<=[.!?])\s+(?=[A-ZА-ЯЁ])", normalized)
        return tuple(Sentence(part, index) for index, part in enumerate(parts) if part)

    def get_sentences(self, text: str) -> tuple[Sentence, ...]:
        """
        Splits the provided text into sentences and preprocesses them.

        Args:
            text (str): Raw text to split and preprocess.

        Returns:
            tuple[Sentence, ...]: Sequence of preprocessed sentences extracted from the text.
        """
        sentences = self._split_by_sentence(text)
        self._preprocess_sentences(sentences)
        return sentences

    def preprocess_text(self, text: str) -> tuple[str, ...]:
        """
        Produces filtered, clean, lowercase tokens from raw text.

        Args:
            text (str): Raw text.

        Returns:
            tuple[str, ...]: Clean lowercase tokens without stop words.
        """
        return self._remove_stop_words(self._clean_and_tokenize(text))


class SentenceEncoder:
    """
    A class to encode string sequences into matching integer sequences.

    Attributes:
        _word2id (dict[str, int]): Maps words to integers.
        _id2word (dict[int, str]): Maps integers to words.
        last (int): Counter for the last assigned identifier.
    """

    def __init__(self) -> None:
        """
        Initializes the sentence encoder.
        """
        self._word2id = {}
        self._id2word = {}
        self.last = 999

    def __str__(self) -> str:
        """
        Returns a string representation of the encoder.

        Returns:
            str: String representation of the encoder.
        """
        return f"SentenceEncoder(vocabulary_size={len(self._word2id)})"

    def _learn_indices(self, tokens: Sequence[str]) -> None:
        """
        Creates mappings between words and their integer equivalents.

        Args:
            tokens (Sequence[str]): Sequence of string tokens.
        """
        if (
            not isinstance(tokens, Sequence)
            or isinstance(tokens, (str, bytes, bytearray))
            or any(not isinstance(token, str) for token in tokens)
        ):
            raise IncorrectArgumentError("Incorrect input value")
        for token in tokens:
            if token not in self._word2id:
                self.last += 1
                self._word2id[token] = self.last
                self._id2word[self.last] = token

    def encode_sentences(self, sentences: Sequence[Sentence]) -> None:
        """
        Encodes the preprocessed tokens of each sentence.

        Args:
            sentences (Sequence[Sentence]): Sequence of sentences to encode.
        """
        if (
            not isinstance(sentences, Sequence)
            or isinstance(sentences, (str, bytes, bytearray))
            or any(not isinstance(sentence, Sentence) for sentence in sentences)
        ):
            raise IncorrectArgumentError("Incorrect input value")
        for sentence in sentences:
            tokens = sentence.get_preprocessed()
            self._learn_indices(tokens)
            sentence.set_encoded(tuple(self._word2id[token] for token in tokens))


def calculate_similarity(sequence: Sequence, other_sequence: Sequence) -> float:
    """
    Calculates the similarity between two sequences using the Jaccard index.

    Args:
        sequence (Sequence): First sequence of items.
        other_sequence (Sequence): Second sequence of items.

    Returns:
        float: Jaccard similarity score between the two sequences.
    """
    if not isinstance(sequence, Sequence) or not isinstance(other_sequence, Sequence):
        raise IncorrectArgumentError("Incorrect input value")
    if not sequence or not other_sequence:
        return 0.0
    first = set(sequence)
    second = set(other_sequence)
    union = first | second
    return len(first & second) / len(union)

class TextGraph:
    """
    A class to represent relations between sentences.

    Attributes:
        _vertices (list[Sentence]): List of sentence vertices in the graph.
        _matrix (list[list[float]]): Similarity matrix representing edges between vertices.
    """

    def __init__(self) -> None:
        """
        Initializes an empty similarity graph.
        """
        self._vertices = []
        self._matrix = []

    def __len__(self) -> int:
        """
        Returns the number of sentence vertices in the graph.

        Returns:
            int: Number of vertices.
        """
        return len(self._vertices)

    def __str__(self) -> str:
        """
        Returns a short description of the graph.

        Returns:
            str: Description of the graph.
        """
        return f"TextGraph(vertices={len(self._vertices)})"

    def _add_edge(self, vertex1: Sentence, vertex2: Sentence) -> None:
        """
        Adds an edge between two vertices in the graph.

        Args:
            vertex1 (Sentence): First vertex.
            vertex2 (Sentence): Second vertex.
        """
        if not isinstance(vertex1, Sentence) or not isinstance(vertex2, Sentence):
            raise IncorrectArgumentError("Incorrect input value")
        if vertex1 == vertex2:
            raise TextGraphError("Cannot add an edge from a vertex to itself")
        self._add_vertex(vertex1)
        self._add_vertex(vertex2)
        first_index = self._vertices.index(vertex1)
        second_index = self._vertices.index(vertex2)
        score = calculate_similarity(vertex1.get_encoded(), vertex2.get_encoded())
        self._matrix[first_index][second_index] = score
        self._matrix[second_index][first_index] = score

    def _add_vertex(self, vertex: Sentence) -> None:
        """
        Adds a vertex and extends the matrix without computing similarity scores.

        Args:
            vertex (Sentence): Vertex to add to the graph.
        """
        if not isinstance(vertex, Sentence):
            raise IncorrectArgumentError("Incorrect input value")
        if vertex in self._vertices:
            return
        for row in self._matrix:
            row.append(0.0)
        self._vertices.append(vertex)
        new_row = [0.0] * len(self._vertices)
        new_row[-1] = 1.0
        self._matrix.append(new_row)

    def build(self, sentences: Sequence[Sentence]) -> None:
        """
        Builds the graph from preprocessed and encoded sentences.

        Args:
            sentences (Sequence[Sentence]): Sequence of sentences to add.
        """
        if (
            not isinstance(sentences, Sequence)
            or isinstance(sentences, (str, bytes, bytearray))
            or not sentences
            or any(not isinstance(sentence, Sentence) for sentence in sentences)
        ):
            raise IncorrectArgumentError("Incorrect input value")
        for sentence in sentences:
            self._add_vertex(sentence)
        for first_index, first_sentence in enumerate(sentences):
            for second_sentence in sentences[first_index + 1:]:
                if first_sentence != second_sentence:
                    self._add_edge(first_sentence, second_sentence)

    def calculate_inout_score(self, vertex: Sentence) -> int:
        """
        Calculates the number of vertices similar to the specified vertex.

        Args:
            vertex (Sentence): Vertex whose similar vertices should be counted.

        Returns:
            int: Number of similar vertices.
        """
        if not isinstance(vertex, Sentence):
            raise IncorrectArgumentError("Incorrect input value")
        if vertex not in self._vertices:
            raise TextGraphError("Vertex is not in the graph")
        vertex_index = self._vertices.index(vertex)
        return sum(
            score > 0.0 and index != vertex_index
            for index, score in enumerate(self._matrix[vertex_index])
        )


    def get_vertices(self) -> tuple[Sentence, ...]:
        """
        Returns all vertices present in the graph.

        Returns:
            tuple[Sentence, ...]: Sequence of vertices in the graph.
        """
        return tuple(self._vertices)

    def get_similarity_score(self, vertex1: Sentence, vertex2: Sentence) -> float:
        """
        Returns the similarity score between two vertices.

        Args:
            vertex1 (Sentence): First vertex.
            vertex2 (Sentence): Second vertex.

        Returns:
            float: Similarity score between the two vertices.
        """
        if not isinstance(vertex1, Sentence) or not isinstance(vertex2, Sentence):
            raise IncorrectArgumentError("Incorrect input value")
        if vertex1 not in self._vertices or vertex2 not in self._vertices:
            raise TextGraphError("Vertex is not in the graph")
        first_index = self._vertices.index(vertex1)
        second_index = self._vertices.index(vertex2)
        return float(self._matrix[first_index][second_index])

    def get_top_n_sentences(self, n: int) -> tuple[Sentence, ...]:
        """
        Returns the top n sentences with the highest sum of similarity scores.

        Args:
            n (int): Number of top sentences to return.

        Returns:
            tuple[Sentence, ...]: Top n sentences with the highest similarity score sum.
        """
        if not self._vertices:
            raise TextGraphError("Graph is empty")
        if not isinstance(n, int) or isinstance(n, bool) or n <= 0:
            raise IncorrectArgumentError("Incorrect input value")
        ranked_indices = sorted(
            range(len(self._vertices)),
            key=lambda index: sum(self._matrix[index]),
            reverse=True,
        )
        return tuple(self._vertices[index] for index in ranked_indices[:n])


class NaiveSummarizer:
    """
    Naive graph summarizer and shared interface for graph-based algorithms.

    Attributes:
        _graph (TextGraph): Graph of sentence vertices and their relations.
    """

    def __init__(self, graph: TextGraph) -> None:
        """
        Initializes a graph summarizer with a similarity graph.

        Args:
            graph (TextGraph): Built graph of encoded sentences.
        """
        if not isinstance(graph, TextGraph):
            raise IncorrectArgumentError("Incorrect input value")
        self._graph = graph

    def __str__(self) -> str:
        """
        Returns a string representation of the summarizer.

        Returns:
            str: String representation of the summarizer.
        """
        return f"NaiveSummarizer(graph={self._graph})"

    def _get_top_n_sentences(self, n: int) -> tuple[Sentence, ...]:
        """
        Returns the top n sentences with the highest significance scores.

        Args:
            n (int): Number of top sentences to return.

        Returns:
            tuple[Sentence, ...]: Top n sentences with the highest significance scores.
        """
        return self._graph.get_top_n_sentences(n)

    def summarize(self, n_sentences: int) -> str:
        """
        Returns a summary from the current sentence scores.

        Args:
            n_sentences (int): Number of sentences to include.

        Returns:
            str: Selected sentences in source order.
        """
        top_sentences = self._get_top_n_sentences(n_sentences)
        ordered_sentences = sorted(
            top_sentences,
            key=lambda sentence: sentence.get_position(),
        )
        return "\n".join(sentence.get_text() for sentence in ordered_sentences)


class TextRankSummarizer(NaiveSummarizer):
    """
    TextRank algorithm for text summarization.

    Attributes:
        _damping_factor (float): Damping factor for score calculation.
        _convergence_threshold (float): Threshold for convergence of scores.
        _max_iter (int): Maximum number of iterations for score calculation.
        _scores (dict[Sentence, float]): Significance scores for each vertex.
    """

    def __init__(self, graph: TextGraph) -> None:
        """
        Initializes a TextRank summarizer with a similarity graph.

        Args:
            graph (TextGraph): Built graph of encoded sentences.
        """

    def __len__(self) -> int:
        """
        Returns the number of vertices in the graph.

        Returns:
            int: Number of vertices in the graph.
        """

    def __str__(self) -> str:
        """
        Returns a string representation of the TextRank summarizer.

        Returns:
            str: String representation of the TextRank summarizer.
        """

    def _get_top_n_sentences(self, n: int) -> tuple[Sentence, ...]:
        """
        Returns the top n sentences with the highest significance scores.

        Args:
            n (int): Number of top sentences to return.

        Returns:
            tuple[Sentence, ...]: Top n sentences with the highest significance scores.
        """

    def _update_vertex_score(
        self,
        vertex: Sentence,
        incidental_vertices: Sequence[Sentence],
        current_scores: dict[Sentence, float],
    ) -> None:
        """
        Updates a vertex significance score using the TextRank formula.

        Args:
            vertex (Sentence): Sentence whose score should be updated.
            incidental_vertices (Sequence[Sentence]): Vertices related to the sentence.
            current_scores (dict[Sentence, float]): Current scores of all vertices.
        """

    def train(self) -> None:
        """
        Iteratively calculates significance scores for all vertices until convergence.
        """
