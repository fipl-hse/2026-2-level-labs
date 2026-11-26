"""
Lab 4
Summarize text using TextRank algorithm

.. py:class:: EncodedSentence

   Type alias representing an encoded sentence as a tuple of integers.

.. py:class:: PreprocessedSentence

   Type alias representing a preprocessed sentence as a tuple of strings.
"""

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
        if (
            not isinstance(text, str)
            or not isinstance(position, int)
            or isinstance(position, bool)
        ):
            raise IncorrectArgumentError

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

    def __hash__(self) -> int:
        """
        Returns a hash value for the Sentence instance.

        Returns:
            int: Hash value based on the text and position.
        """

    def __str__(self) -> str:
        """
        Returns a string representation of the sentence.

        Returns:
            str: String representation of the sentence.
        """
        return f'Sentence(text={self._text!r}, position={self._position})'

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
        if not isinstance(encoded_sentence, (tuple, list)):
            raise IncorrectArgumentError
        for integer in encoded_sentence:
            if not isinstance(integer, int):
                raise IncorrectArgumentError

        self._encoded = tuple(encoded_sentence)

    def set_preprocessed(self, preprocessed_sentence: PreprocessedSentence) -> None:
        """
        Sets the preprocessed representation of the sentence.

        Args:
            preprocessed_sentence (PreprocessedSentence): Preprocessed sequence of tokens.
        """
        if not isinstance(preprocessed_sentence, (tuple, list)):
            raise IncorrectArgumentError
        for token in preprocessed_sentence:
            if not isinstance(token, str):
                raise IncorrectArgumentError

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
            not isinstance(stop_words, (tuple, list))
            or not isinstance(punctuation, (tuple, list))
        ):
            raise IncorrectArgumentError

        for word in stop_words:
            if not isinstance(word, str):
                raise IncorrectArgumentError

        for symb in punctuation:
            if not isinstance(symb, str):
                raise IncorrectArgumentError

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
            raise IncorrectArgumentError

        cleaned_text = text.lower()

        for punct_mark in self._punctuation:
            cleaned_text = cleaned_text.replace(punct_mark, " ")

        return tuple(cleaned_text.split())

    def _preprocess_sentences(self, sentences: Sequence[Sentence]) -> None:
        """
        Preprocesses a sequence of sentences and stores their token representations.

        Args:
            sentences (Sequence[Sentence]): Sequence of sentences to preprocess.
        """
        for sentence in sentences:
            if not isinstance(sentence, Sentence):
                raise IncorrectArgumentError

        for sentence in sentences:
            preprocessed_tokens = self.preprocess_text(sentence.get_text())
            sentence.set_preprocessed(preprocessed_tokens)

    def _remove_stop_words(self, tokens: Sequence[str]) -> tuple[str, ...]:
        """
        Removes stop words from a sequence of tokens.

        Args:
            tokens (Sequence[str]): Sequence of tokens containing stop words.

        Returns:
            tuple[str, ...]: Sequence of tokens without stop words.
        """
        for token in tokens:
            if not isinstance(token, str):
                raise IncorrectArgumentError

        filtered_tokens = []

        for token in tokens:
            if token not in self._stop_words:
                filtered_tokens.append(token)

        return tuple(filtered_tokens)

    def _split_by_sentence(self, text: str) -> tuple[Sentence, ...]:
        """
        Splits the provided text into sentences.

        Args:
            text (str): Raw text to split.

        Returns:
            tuple[Sentence, ...]: Sequence of sentences extracted from the text.
        """
        if not isinstance(text, str):
            raise IncorrectArgumentError

        format_text = ' '.join(text.replace('\n', ' ').split())
        if not format_text:
            return ()

        sentences = []
        start = 0
        for i in range(len(format_text) - 2):
            if (
                format_text[i] in '.!?'
                and format_text[i+1] == ' '
                and format_text[i+2].isupper()
            ):
                sentences.append(Sentence(format_text[start:i + 1], len(sentences)))
                start = i + 2

        sentences.append(Sentence(format_text[start:], len(sentences)))

        return tuple(sentences)

    def get_sentences(self, text: str) -> tuple[Sentence, ...]:
        """
        Splits the provided text into sentences and preprocesses them.

        Args:
            text (str): Raw text to split and preprocess.

        Returns:
            tuple[Sentence, ...]: Sequence of preprocessed sentences extracted from the text.
        """
        if not isinstance(text, str):
            raise IncorrectArgumentError

        sentences = self._split_by_sentence(text)
        self._preprocess_sentences(sentences)

        return tuple(sentences)

    def preprocess_text(self, text: str) -> tuple[str, ...]:
        """
        Produces filtered, clean, lowercase tokens from raw text.

        Args:
            text (str): Raw text.

        Returns:
            tuple[str, ...]: Clean lowercase tokens without stop words.
        """
        if not isinstance(text, str):
            raise IncorrectArgumentError

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
        return f'SentenceEncoder(vocabulary_size={len(self._word2id)})'

    def _learn_indices(self, tokens: Sequence[str]) -> None:
        """
        Creates mappings between words and their integer equivalents.

        Args:
            tokens (Sequence[str]): Sequence of string tokens.
        """
        if not isinstance(tokens, (tuple, list)):
            raise IncorrectArgumentError
        for token in tokens:
            if not isinstance(token, str):
                raise IncorrectArgumentError
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
        if not isinstance(sentences, (tuple, list)):
            raise IncorrectArgumentError
        for sentence in sentences:
            if not isinstance(sentence, Sentence):
                raise IncorrectArgumentError

            preprocessed_tokens = sentence.get_preprocessed()
            self._learn_indices(preprocessed_tokens)
            encoded_sentences = tuple(
                self._word2id[token]
                for token in preprocessed_tokens
            )
            sentence.set_encoded(encoded_sentences)


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
        not isinstance(sequence, (list, tuple))
        or not isinstance(other_sequence, (list, tuple))
    ):
        raise IncorrectArgumentError
    if len(sequence) == 0 or len(other_sequence) == 0:
        return 0.0

    elements = set(sequence)
    other_elements = set(other_sequence)
    intersection_value = len(elements & other_elements)
    union_value = len(elements | other_elements)

    return intersection_value / union_value


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

    def __len__(self) -> int:
        """
        Returns the number of sentence vertices in the graph.

        Returns:
            int: Number of vertices.
        """

    def __str__(self) -> str:
        """
        Returns a short description of the graph.

        Returns:
            str: Description of the graph.
        """

    def _add_edge(self, vertex1: Sentence, vertex2: Sentence) -> None:
        """
        Adds an edge between two vertices in the graph.

        Args:
            vertex1 (Sentence): First vertex.
            vertex2 (Sentence): Second vertex.
        """

    def _add_vertex(self, vertex: Sentence) -> None:
        """
        Adds a vertex and extends the matrix without computing similarity scores.

        Args:
            vertex (Sentence): Vertex to add to the graph.
        """

    def build(self, sentences: Sequence[Sentence]) -> None:
        """
        Builds the graph from preprocessed and encoded sentences.

        Args:
            sentences (Sequence[Sentence]): Sequence of sentences to add.
        """

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

    def get_similarity_score(self, vertex1: Sentence, vertex2: Sentence) -> float:
        """
        Returns the similarity score between two vertices.

        Args:
            vertex1 (Sentence): First vertex.
            vertex2 (Sentence): Second vertex.

        Returns:
            float: Similarity score between the two vertices.
        """

    def get_top_n_sentences(self, n: int) -> tuple[Sentence, ...]:
        """
        Returns the top n sentences with the highest sum of similarity scores.

        Args:
            n (int): Number of top sentences to return.

        Returns:
            tuple[Sentence, ...]: Top n sentences with the highest similarity score sum.
        """


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

    def __str__(self) -> str:
        """
        Returns a string representation of the summarizer.

        Returns:
            str: String representation of the summarizer.
        """

    def _get_top_n_sentences(self, n: int) -> tuple[Sentence, ...]:
        """
        Returns the top n sentences with the highest significance scores.

        Args:
            n (int): Number of top sentences to return.

        Returns:
            tuple[Sentence, ...]: Top n sentences with the highest significance scores.
        """

    def summarize(self, n_sentences: int) -> str:
        """
        Returns a summary from the current sentence scores.

        Args:
            n_sentences (int): Number of sentences to include.

        Returns:
            str: Selected sentences in source order.
        """


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
