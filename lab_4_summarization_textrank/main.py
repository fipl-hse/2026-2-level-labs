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
        if not isinstance(text, str):
            raise IncorrectArgumentError("Incorrect input value")

        if not isinstance(position, int) or isinstance(position, bool):
            raise IncorrectArgumentError("Incorrect input value")

        self._text = text
        self._position = position
        self._preprocessed = ()
        self._encoded = ()


    def __eq__(self, other: object) -> bool:
        """
        Checks equality between two Sentence instances.

        Args:
            other (object): Another object to compare.

        Returns:
            bool: True if both are Sentence instances with the same text and position,
              otherwise False.
        """
        if not isinstance(other, Sentence):
            return False

        return self._text == other._text and self._position == other._position

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
        return f"Sentence(text='{self._text}', position={self._position})"

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
            or not all(isinstance(token, int) for token in encoded_sentence)
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
            not all(isinstance(token, str) for token in preprocessed_sentence)
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
            or not all(isinstance(word, str) for word in stop_words)
            or not isinstance (punctuation, Sequence)
            or not all(isinstance(char, str) for char in punctuation)
        ):
            raise IncorrectArgumentError("Incorrect input value")

        self._stop_words = stop_words
        self._punctuation = punctuation

    def __str__(self) -> str:
        """
        Returns a string representation of the preprocessor.

        Returns:
            str: String representation of the preprocessor.
        """
        return f"SentencePreprocessor(stop_words={len(self._stop_words)}, punctuation={len(self._punctuation)}"

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

        for punctuation in self._punctuation:
            text = text.replace(punctuation, "")

        return tuple(text.lower().split())

    def _preprocess_sentences(self, sentences: Sequence[Sentence]) -> None:
        """
        Preprocesses a sequence of sentences and stores their token representations.

        Args:
            sentences (Sequence[Sentence]): Sequence of sentences to preprocess.
        """
        if (
            not isinstance(sentences, Sequence)
            or not all(isinstance(sentence, Sentence) for sentence in sentences)
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
            or not all(isinstance(token, str) for token in tokens)
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

        normalized_text = " ".join(text.split())
        sentences_text = re.split(r"(?<=[.!?])\s+(?=[А-ЯЁA-Z])", normalized_text)

        return tuple(
            Sentence(sentence, position)
            for position, sentence in enumerate(sentences_text)
            if sentence
        )

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
        if not isinstance(text, str):
            raise IncorrectArgumentError("Incorrect input value")

        tokens = self._clean_and_tokenize(text)
        return self._remove_stop_words(tokens)

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
            or not all(isinstance(token, str) for token in tokens)
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
            or not all(isinstance(sentence, Sentence) for sentence in sentences)
        ):
            raise IncorrectArgumentError("Incorrect input value")

        for sentence in sentences:
            tokens = sentence.get_preprocessed()
            self._learn_indices(tokens)
            encoded = tuple(self._word2id[token] for token in tokens)
            sentence.set_encoded(encoded)


def calculate_similarity(sequence: Sequence, other_sequence: Sequence) -> float:
    """
    Calculates the similarity between two sequences using the Jaccard index.

    Args:
        sequence (Sequence): First sequence of items.
        other_sequence (Sequence): Second sequence of items.

    Returns:
        float: Jaccard similarity score between the two sequences.
    """
    if (
        not isinstance (sequence, Sequence)
        or not isinstance (other_sequence, Sequence)
    ):
        raise IncorrectArgumentError("Incorrect input value")

    if not sequence or not other_sequence:
        return 0.0

    intersection = set(sequence) & set(other_sequence)
    union = set(sequence) | set(other_sequence)

    return len(intersection) / len(union)

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
        return int(len(self._vertices))

    def __str__(self) -> str:
        """
        Returns a short description of the graph.

        Returns:
            str: Description of the graph.
        """
        return f"TextGraph(vertices={len(self)})"

    def _add_edge(self, vertex1: Sentence, vertex2: Sentence) -> None:
        """
        Adds an edge between two vertices in the graph.

        Args:
            vertex1 (Sentence): First vertex.
            vertex2 (Sentence): Second vertex.
        """
        if (
            not isinstance(vertex1, Sentence)
            or not isinstance(vertex2, Sentence)
        ):
            raise IncorrectArgumentError("Incorrect input value")

        if vertex1 == vertex2:
            raise TextGraphError("Self-loops are not allowed")

        if vertex1 not in self._vertices:
            self._add_vertex(vertex1)
        if vertex2 not in self._vertices:
            self._add_vertex(vertex2)

        index1 = self._vertices.index(vertex1)
        index2 = self._vertices.index(vertex2)

        encoded1 = vertex1.get_encoded()
        encoded2 = vertex2.get_encoded()

        weight = calculate_similarity(encoded1, encoded2)

        self._matrix[index1][index2] = weight
        self._matrix[index2][index1] = weight

    def _add_vertex(self, vertex: Sentence) -> None:
        """
        Adds a vertex and extends the matrix without computing similarity scores.

        Args:
            vertex (Sentence): Vertex to add to the graph.
        """
        if not isinstance(vertex, Sentence):
            raise IncorrectArgumentError("Incorrect input value")

        if vertex not in self._vertices:
            self._vertex = self._vertices.append(vertex)
            self._matrix.append([0.0] * len(self._vertices))
            for row in self._matrix[:-1]:
                row.append(0.0)

    def build(self, sentences: Sequence[Sentence]) -> None:
        """
        Builds the graph from preprocessed and encoded sentences.

        Args:
            sentences (Sequence[Sentence]): Sequence of sentences to add.
        """
        if (
            not isinstance(sentences, Sequence)
            or not all(isinstance(sentence, Sentence) for sentence in sentences)
            or not sentences
        ):
            raise IncorrectArgumentError("Incorrect input value")

        for sentence in sentences:
            self._add_vertex(sentence)

        for i in range(len(sentences)):
            for j in range(i + 1, len(sentences)):
                sentence1 = sentences[i]
                sentence2 = sentences[j]

                if sentence1 != sentence2:
                    self._add_edge(sentence1, sentence2)

    def calculate_inout_score(self, vertex: Sentence) -> int:
        """
        Calculates the number of vertices similar to the specified vertex.

        Args:
            vertex (Sentence): Vertex whose similar vertices should be counted.

        Returns:
            int: Number of similar vertices.
        """

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
        if vertex1 not in self._vertices or vertex2 not in self._vertices:
            raise TextGraphError("One or both vertices are not in the graph")

        index1 = self._vertices.index(vertex1)
        index2 = self._vertices.index(vertex2)

        return self._matrix[index1][index2]

    def get_top_n_sentences(self, n: int) -> tuple[Sentence, ...]:
        """
        Returns the top n sentences with the highest sum of similarity scores.

        Args:
            n (int): Number of top sentences to return.

        Returns:
            tuple[Sentence, ...]: Top n sentences with the highest similarity score sum.
        """
        if not isinstance(n, int):
            raise IncorrectArgumentError("Incorrect input value")
        if not self._vertices:
            raise TextGraphError("The graph is empty")

        vertex_scores = []
        for i, vertex in enumerate(self._vertices):
            score_sum = sum(self._matrix[i])
            vertex_scores.append((score_sum, vertex))

        vertex_scores.sort(key=lambda x: x[0], reverse=True)

        top_n = [x[1] for x in vertex_scores[:n]]

        return tuple(top_n)

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
        return f"NaiveSummarizer(graph={self._graph}"

    def _get_top_n_sentences(self, n: int) -> tuple[Sentence, ...]:
        """
        Returns the top n sentences with the highest significance scores.

        Args:
            n (int): Number of top sentences to return.

        Returns:
            tuple[Sentence, ...]: Top n sentences with the highest significance scores.
        """
        if not isinstance(n, int):
            raise IncorrectArgumentError("Incorrect input value")

        return self._graph.get_top_n_sentences(n)

    def summarize(self, n_sentences: int) -> str:
        """
        Returns a summary from the current sentence scores.

        Args:
            n_sentences (int): Number of sentences to include.

        Returns:
            str: Selected sentences in source order.
        """
        if not isinstance(n_sentences, int):
            raise IncorrectArgumentError("Incorrect input value")

        top_sentences = self._get_top_n_sentences(n_sentences)

        sorted_sentences = sorted(top_sentences, key=lambda sentence: sentence.get_position())

        summary = "\n".join(sentence.get_text() for sentence in sorted_sentences)

        return summary

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
