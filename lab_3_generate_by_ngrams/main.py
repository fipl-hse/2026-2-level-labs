"""
Lab 3.

Beam-search and natural language generation evaluation
"""

# pylint:disable=too-few-public-methods


class TextProcessor:
    """
    Handle text tokenization, encoding and decoding.

    Attributes:
        _end_of_word_token (str): A token denoting word boundary
        _storage (dict): Dictionary in the form of <token: identifier>
    """

    def __init__(self, end_of_word_token: str) -> None:
        """
        Initialize an instance of TextProcessor.

        Args:
            end_of_word_token (str): A token denoting word boundary
        """
        self._end_of_word_token = end_of_word_token
        self._storage = {end_of_word_token: 0}

    def _tokenize(self, text: str) -> tuple[str, ...] | None:
        """
        Tokenize text into unigrams, separating words with special token.

        Punctuation and digits are removed. EoW token is appended after the last word in two cases:
        1. It is followed by punctuation
        2. It is followed by space symbol

        Args:
            text (str): Original text

        Returns:
            tuple[str, ...] | None: Tokenized text

        In case of corrupt input arguments, None is returned.
        In case any of methods used return None, None is returned.
        """
        if not isinstance(text, str):
            return None

        if not isinstance(self._end_of_word_token, str):
            return None

        preprocessed_text = "".join(
            sym
            for sym in text.lower()
            if sym.isalpha() or sym == " "
        ).split()
        if not preprocessed_text:
            return None

        tokens = []
        for word in preprocessed_text:
            tokens.extend(sym for sym in word)
            if not(word is preprocessed_text[-1] and text[-1].isalpha()):
                tokens.append(self._end_of_word_token)
        return tuple(tokens)

    def get_id(self, element: str) -> int | None:
        """
        Retrieve a unique identifier of an element.

        Args:
            element (str): String element to retrieve identifier for

        Returns:
            int | None: Integer identifier that corresponds to the given element

        In case of corrupt input arguments or arguments not included in storage,
        None is returned
        """
        if not isinstance(element, str):
            return None

        return self._storage.get(element)

    def get_end_of_word_token(self) -> str:  # type: ignore[empty-body]
        """
        Retrieve value stored in self._end_of_word_token attribute.

        Returns:
            str: EoW token
        """
        return self._end_of_word_token

    def get_token(self, element_id: int) -> str | None:
        """
        Retrieve an element by unique identifier.

        Args:
            element_id (int): Identifier to retrieve identifier for

        Returns:
            str | None: Element that corresponds to the given identifier

        In case of corrupt input arguments or arguments not included in storage, None is returned
        """
        if not isinstance(element_id, int):
            return None

        for element, identifier in self._storage.items():
            if identifier == element_id:
                return element
        return None

    def encode(self, text: str) -> tuple[int, ...] | None:
        """
        Encode text.

        Tokenize text, assign each symbol an integer identifier and
        replace letters with their ids.

        Args:
            text (str): An original text to be encoded

        Returns:
            tuple[int, ...] | None: Processed text

        In case of corrupt input arguments, None is returned.
        In case any of methods used return None, None is returned.
        """
        if not(isinstance(text, str) and text):
            return None

        tokens = self._tokenize(text)
        if tokens is None:
            return None

        encoded_corpus = []
        for token in tokens:
            self._put(token)
            identifier = self.get_id(token)
            if identifier is None:
                return None
            encoded_corpus.append(identifier)
        return tuple(encoded_corpus)

    def _put(self, element: str) -> None:
        """
        Put an element into the storage, assign a unique id to it.

        Args:
            element (str): An element to put into storage

        In case of corrupt input arguments or invalid argument length,
        an element is not added to storage
        """
        if not(isinstance(element, str) and len(element) == 1):
            return None

        if element not in self._storage:
            self._storage[element] = len(self._storage)
        return True

    def decode(self, encoded_corpus: tuple[int, ...]) -> str | None:
        """
        Decode and postprocess encoded corpus by converting integer identifiers to string.

        Special symbols are replaced with spaces (no multiple spaces in a row are allowed).
        The first letter is capitalized, resulting sequence must end with a full stop.

        Args:
            encoded_corpus (tuple[int, ...]): A tuple of encoded tokens

        Returns:
            str | None: Resulting text

        In case of corrupt input arguments, None is returned.
        In case any of methods used return None, None is returned.
        """
        if not(
            (isinstance(encoded_corpus, tuple) and encoded_corpus)
            and all(isinstance(identifier, int) for identifier in encoded_corpus)
        ):
            return None

        tokens = self._decode(encoded_corpus)
        return self._postprocess_decoded_text(tokens)

    def fill_from_ngrams(self, content: dict) -> None:
        """
        Fill internal storage with letters from external JSON.

        Args:
            content (dict): ngrams from external JSON
        """
        if not(isinstance(content, dict)):
            return None

        frequencies = content.get("freq")
        if frequencies is None:
            return None
        if not all(isinstance(n_gram, str) for n_gram in frequencies):
            return None

        for n_gram in frequencies:
            n_gram_by_sym = (sym for sym in n_gram if sym.isalpha())
            for sym in n_gram_by_sym:
                self._put(sym)
        return True

    def _decode(self, corpus: tuple[int, ...]) -> tuple[str, ...] | None:
        """
        Decode sentence by replacing ids with corresponding letters.

        Args:
            corpus (tuple[int, ...]): A tuple of encoded tokens

        Returns:
            tuple[str, ...] | None: Sequence with decoded tokens

        In case of corrupt input arguments, None is returned.
        In case any of methods used return None, None is returned.
        """
        if not(
            (isinstance(corpus, tuple) and corpus)
            and all(isinstance(identifier, int) for identifier in corpus)
        ):
            return None

        tokens = []
        for identifier in corpus:
            token = self.get_token(identifier)
            if token is None:
                return None
            tokens.append(token)
        return tuple(tokens)

    def _postprocess_decoded_text(self, decoded_corpus: tuple[str, ...]) -> str | None:
        """
        Convert decoded sentence into the string sequence.

        Special symbols are replaced with spaces (no multiple spaces in a row are allowed).
        The first letter is capitalized, resulting sequence must end with a full stop.

        Args:
            decoded_corpus (tuple[str, ...]): A tuple of decoded tokens

        Returns:
            str | None: Resulting text

        In case of corrupt input arguments, None is returned
        """
        if not(
            (isinstance(decoded_corpus, tuple) and decoded_corpus)
            and all(isinstance(token, str) for token in decoded_corpus)
        ):
            return None

        if not isinstance(self._end_of_word_token, str):
            return None

        postprocessed_text = "".join(decoded_corpus).replace(
            self._end_of_word_token,
            " ",
        ).capitalize().strip()
        return postprocessed_text + "."


class WordProcessor(TextProcessor):
    """
    Handle text tokenization, encoding and decoding on the level of words.

    Attributes:
        _end_of_word_token (str): A token denoting sentence boundary
        _storage (dict): Dictionary in the form of <token: identifier>
    """

    def _tokenize(self, text: str) -> tuple[str, ...] | None:
        """
        Tokenize text into words, separating sentences with special token.

        Punctuation and digits are removed. Special token is appended after the word
        that ends a sentence, i.e. is followed by '.', '!' or '?'.

        Args:
            text (str): Original text

        Returns:
            tuple[str, ...] | None: Tokenized text

        In case of corrupt input arguments, None is returned.
        In case text does not contain any words, None is returned.
        """

    def _put(self, element: str) -> None:
        """
        Put a word into the storage, assign a unique id to it.

        Args:
            element (str): A word to put into storage

        In case of corrupt input arguments, an element is not added to storage
        """
        # if not (isinstance(element, str) and element):
        #     return None

        # if element not in self._storage:
        #     self._storage[element] = len(self._storage)
        # return True

    def _postprocess_decoded_text(self, decoded_corpus: tuple[str, ...]) -> str | None:
        """
        Convert decoded sequence of words into the string sequence.

        Words are separated with spaces, special tokens are replaced with full stops.
        Each sentence is capitalized, resulting sequence must end with a full stop.

        Args:
            decoded_corpus (tuple[str, ...]): A tuple of decoded tokens

        Returns:
            str | None: Resulting text

        In case of corrupt input arguments, None is returned.
        In case decoded corpus does not contain any words, None is returned.
        """


class NGramLanguageModel:
    """
    Store language model by n_grams, predict the next token.

    Attributes:
        __n_gram_size (int): A size of n-grams to use for language modelling
        _n_gram_frequencies (dict): Frequencies for n-grams
        _encoded_corpus (tuple): Encoded text
    """

    def __init__(self, encoded_corpus: tuple | None, n_gram_size: int) -> None:
        """
        Initialize an instance of NGramLanguageModel.

        Args:
            encoded_corpus (tuple | None): Encoded text
            n_gram_size (int): A size of n-grams to use for language modelling
        """
        self._encoded_corpus = encoded_corpus
        self.__n_gram_size = n_gram_size
        self._n_gram_frequencies = {}

    def get_n_gram_size(self) -> int:  # type: ignore[empty-body]
        """
        Retrieve value stored in self.__n_gram_size attribute.

        Returns:
            int: Size of stored n_grams
        """
        return self.__n_gram_size

    def set_n_grams(self, frequencies: dict) -> None:
        """
        Setter method for n-gram frequencies.

        Args:
            frequencies (dict): Computed in advance frequencies for n-grams
        """
        if not(isinstance(frequencies, dict) and frequencies):
            return None

        self._n_gram_frequencies = frequencies

    def build(self) -> bool:
        """
        Fill attribute `_n_gram_frequencies` from encoded corpus.

        Encoded corpus is stored in the attribute `_encoded_corpus`

        Returns:
            bool: True if attribute is filled successfully, otherwise False

        In case of corrupt input arguments or methods used return None,
        False is returned
        """
        if not(
            (isinstance(self._encoded_corpus, tuple) and self._encoded_corpus)
            and all(isinstance(identifier, int) for identifier in self._encoded_corpus)
        ):
            return False

        n_grams = self._extract_n_grams(self._encoded_corpus)
        if n_grams is None:
            return False

        freq_dict = {}
        for n_gram in n_grams:
            freq_dict[n_gram] = freq_dict.get(n_gram, 0) + 1

        n_grams_cut = tuple(n_gram[:-1] for n_gram in n_grams)

        freq_dict_cut = {}
        for n_gram_cut in n_grams_cut:
            freq_dict_cut[n_gram_cut] = freq_dict_cut.get(n_gram_cut, 0) + 1

        for n_gram, n_gram_cut in zip(n_grams, n_grams_cut):
            if n_gram not in self._n_gram_frequencies:
                frequency = freq_dict[n_gram] / freq_dict_cut[n_gram_cut]
                self._n_gram_frequencies[n_gram] = frequency
        return True

    def generate_next_token(self, sequence: tuple[int, ...]) -> dict | None:
        """
        Retrieve tokens that can continue the given sequence along with their probabilities.

        Args:
            sequence (tuple[int, ...]): A sequence to match beginning of NGrams for continuation

        Returns:
            dict | None: Possible next tokens with their probabilities

        In case of corrupt input arguments, None is returned
        """
        if not(
            (isinstance(sequence, tuple) and sequence)
            and all(isinstance(identifier, int) for identifier in sequence)
        ):
            return None

        if not isinstance(self.__n_gram_size, int):
            return None
        if len(sequence) < self.__n_gram_size - 1:
            return None

        candidates = {}
        for n_gram in self._n_gram_frequencies:
            if n_gram[:-1] == sequence[len(sequence) - self.__n_gram_size + 1:]:
                candidates[n_gram[-1]] = self._n_gram_frequencies[n_gram]
        return candidates

    def _extract_n_grams(
        self, encoded_corpus: tuple[int, ...]
    ) -> tuple[tuple[int, ...], ...] | None:
        """
        Split encoded sequence into n-grams.

        Args:
            encoded_corpus (tuple[int, ...]): A tuple of encoded tokens

        Returns:
            tuple[tuple[int, ...], ...] | None: A tuple of extracted n-grams

        In case of corrupt input arguments, None is returned
        """
        if not(
            (isinstance(encoded_corpus, tuple) and encoded_corpus)
            and all(isinstance(identifier, int) for identifier in encoded_corpus)
        ):
            return None

        if not isinstance(self.__n_gram_size, int):
            return None

        n_grams = []
        for ind in range(len(encoded_corpus) - self.__n_gram_size + 1):
            n_grams.append(encoded_corpus[ind:ind + self.__n_gram_size])
        return tuple(n_grams)


class GreedyTextGenerator:
    """
    Greedy text generation by N-grams.

    Attributes:
        _model (NGramLanguageModel): A language model to use for text generation
        _text_processor (TextProcessor): A TextProcessor instance to handle text processing
    """

    def __init__(self, language_model: NGramLanguageModel, text_processor: TextProcessor) -> None:
        """
        Initialize an instance of GreedyTextGenerator.

        Args:
            language_model (NGramLanguageModel): A language model to use for text generation
            text_processor (TextProcessor): A TextProcessor instance to handle text processing
        """
        self._model = language_model
        self._text_processor = text_processor

    def run(self, prompt: str, seq_len: int) -> str | None:
        """
        Generate sequence based on NGram language model and prompt provided.

        Args:
            prompt (str): Beginning of sequence
            seq_len (int): Number of tokens to generate

        Returns:
            str | None: Generated sequence

        In case of corrupt input arguments or methods used return None,
        None is returned
        """
        if not (
            (isinstance(prompt, str) and prompt)
            and (isinstance(seq_len, int) and seq_len > 0)
        ):
            return None

        encoded_prompt = self._text_processor.encode(prompt)
        if encoded_prompt is None:
            return None

        if not isinstance(self._model.get_n_gram_size(), int):
            return None

        for _ in range(seq_len):
            candidates = self._model.generate_next_token(encoded_prompt)
            if candidates is None or not candidates:
                break
            next_identifier = max(candidates.items(), key=lambda item: (item[1], item[0]))[0]
            encoded_prompt += (next_identifier,)
        return self._text_processor.decode(encoded_prompt)


class BeamSearcher:
    """
    Beam Search algorithm for diverse text generation.

    Attributes:
        _beam_width (int): Number of candidates to consider at each step
        _model (NGramLanguageModel): A language model to use for next token prediction
    """

    def __init__(self, beam_width: int, language_model: NGramLanguageModel) -> None:
        """
        Initialize an instance of BeamSearcher.

        Args:
            beam_width (int): Number of candidates to consider at each step
            language_model (NGramLanguageModel): A language model to use for next token prediction
        """

    def get_next_token(self, sequence: tuple[int, ...]) -> list[tuple[int, float]] | None:
        """
        Retrieve candidate tokens for sequence continuation.

        Candidates are sorted by probability and then by token in descending order.
        Number of tokens retrieved must not be bigger than beam width parameter.

        The return value has the following format: [(token, probability), ...].

        Args:
            sequence (tuple[int, ...]): Base sequence to continue

        Returns:
            list[tuple[int, float]] | None: Tokens to use for base sequence continuation

        In case of corrupt input arguments or methods used return None.
        """

    def continue_sequence(
        self,
        sequence: tuple[int, ...],
        next_tokens: list[tuple[int, float]],
        sequence_candidates: dict[tuple[int, ...], float],
    ) -> dict[tuple[int, ...], float] | None:
        """
        Generate new sequences from the base sequence with next tokens provided.

        The base sequence is deleted after continued variations are added.

        Args:
            sequence (tuple[int, ...]): Base sequence to continue
            next_tokens (list[tuple[int, float]]): Token for sequence continuation
            sequence_candidates (dict[tuple[int, ...], float]):
                Storage with all sequences generated

        Returns:
            dict[tuple[int, ...], float] | None: Updated sequence candidates

        In case of corrupt input arguments or unexpected behaviour of methods used return None.
        """

    def prune_sequence_candidates(
        self, sequence_candidates: dict[tuple[int, ...], float]
    ) -> dict[tuple[int, ...], float] | None:
        """
        Remove those sequence candidates that do not make top-N most probable sequences.

        Args:
            sequence_candidates (dict[tuple[int, ...], float]): Current candidate sequences

        Returns:
            dict[tuple[int, ...], float] | None: Pruned sequences

        In case of corrupt input arguments return None.
        """


class BeamSearchTextGenerator:
    """
    Class for text generation with BeamSearch.

    Attributes:
        _language_model (NGramLanguageModel): Language model for next token prediction
        _text_processor (TextProcessor): A TextProcessor instance to handle text processing
        _beam_width (int): Beam width parameter for generation
        beam_searcher (BeamSearcher): Searcher instance for the language model
    """

    def __init__(
        self, language_model: NGramLanguageModel, text_processor: TextProcessor, beam_width: int
    ) -> None:
        """
        Initializes an instance of BeamSearchTextGenerator.

        Args:
            language_model (NGramLanguageModel): Language model to use for text generation
            text_processor (TextProcessor): A TextProcessor instance to handle text processing
            beam_width (int): Beam width parameter for generation
        """

    def run(self, prompt: str, seq_len: int) -> str | None:
        """
        Generate sequence based on NGram language model and prompt provided.

        Args:
            prompt (str): Beginning of sequence
            seq_len (int): Number of tokens to generate

        Returns:
            str | None: Generated sequence

        In case of corrupt input arguments or methods used return None,
        None is returned
        """

    def _get_next_token(
        self, sequence_to_continue: tuple[int, ...]
    ) -> list[tuple[int, float]] | None:
        """
        Retrieve next tokens for sequence continuation.

        Args:
            sequence_to_continue (tuple[int, ...]): Sequence to continue

        Returns:
            list[tuple[int, float]] | None: Next tokens for sequence
            continuation

        In case of corrupt input arguments return None.
        """


class NGramLanguageModelReader:
    """
    Factory for loading language models ngrams from external JSON.

    Attributes:
        _json_path (str): Local path to assets file
        _eow_token (str): Special token for text processor
        _text_processor (TextProcessor): A TextProcessor instance to handle text processing
    """

    def __init__(self, json_path: str, eow_token: str) -> None:
        """
        Initialize reader instance.

        Args:
            json_path (str): Local path to assets file
            eow_token (str): Special token for text processor
        """

    def load(self, n_gram_size: int) -> NGramLanguageModel | None:
        """
        Fill attribute `_n_gram_frequencies` from dictionary with N-grams.

        The N-grams taken from dictionary must be cleaned from digits and punctuation,
        their length must match n_gram_size, and spaces must be replaced with EoW token.

        Args:
            n_gram_size (int): Size of ngram

        Returns:
            NGramLanguageModel | None: Built language model.

        In case of corrupt input arguments or unexpected behaviour of methods used,
        None is returned.
        """

    def get_text_processor(self) -> TextProcessor:  # type: ignore[empty-body]
        """
        Get method for the processor created for the current JSON file.

        Returns:
            TextProcessor: processor created for the current JSON file.
        """


class BackOffGenerator:
    """
    Language model for back-off based text generation.

    Attributes:
        _language_models (dict[int, NGramLanguageModel]): Language models for next token prediction
        _text_processor (TextProcessor): A TextProcessor instance to handle text processing
    """

    def __init__(
        self, language_models: tuple[NGramLanguageModel, ...], text_processor: TextProcessor
    ) -> None:
        """
        Initializes an instance of BackOffGenerator.

        Args:
            language_models (tuple[NGramLanguageModel, ...]):
                Language models to use for text generation
            text_processor (TextProcessor): A TextProcessor instance to handle text processing
        """

    def run(self, prompt: str, seq_len: int) -> str | None:
        """
        Generate sequence based on NGram language model and prompt provided.

        Args:
            prompt (str): Beginning of sequence
            seq_len (int): Number of tokens to generate

        Returns:
            str | None: Generated sequence

        In case of corrupt input arguments or methods used return None,
        None is returned
        """

    def _get_next_token(self, sequence_to_continue: tuple[int, ...]) -> dict[int, float] | None:
        """
        Retrieve next tokens for sequence continuation.

        Args:
            sequence_to_continue (tuple[int, ...]): Sequence to continue

        Returns:
            dict[int, float] | None: Next tokens for sequence continuation

        In case of corrupt input arguments return None.
        """
