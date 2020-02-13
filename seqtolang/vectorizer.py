import re
import itertools
import numpy as np
from collections import Counter

TOKENIZER_REGEX = re.compile(r"[^\d\W]+", re.UNICODE)
PAD_INDEX = 0
UNK_INDEX = 1
CHUNK_SIZE = 20000
MIN_NGRAM_FREQ = 2
TOKEN_PREFIX = '<'
TOKEN_SUFFIX = '>'


class SeqToLangVectorizer():
    def __init__(self, chars_ngram_range=(2,4), words_tokenizer=None):
        self.words_tokenizer = words_tokenizer or _default_tokenizer
        self.chars_ngram_range = chars_ngram_range
        self.max_words = 0
        self.max_ngrams = 0
        self.ngram2id = None
        self.ngrams_counter = Counter()

    def fit(self, texts):
        self.fit_tokens_stats(texts)
        self.build_ngram2id()
        self.ngrams_counter = None
        return self

    def fit_tokens_stats(self, texts):
        for chunk in _chunkenize(texts, CHUNK_SIZE):
            tokenized_text = self.tokenize(chunk)

            for tokens in tokenized_text:
                if len(tokens) > self.max_words:
                    self.max_words = len(tokens)
                max_chars_len = max(map(len, tokens))
                if max_chars_len > self.max_ngrams:
                    self.max_ngrams = max_chars_len

                self.ngrams_counter.update(itertools.chain(*tokens))

    def vectorize(self, texts):
        tokenized_texts = self.tokenize(texts)
        vectors = list(map(self.convert_token_to_ids, tokenized_texts))
        padded_texts = self.pad_tokenized_texts(vectors)
        return np.array(padded_texts, dtype=np.int)

    def tokenize(self, texts):
        return list(map(self.tokenize_single, texts))

    def build_ngram2id(self):
        self.ngram2id = {'__PAD__': PAD_INDEX, '__UNK__': UNK_INDEX}
        for ngram, cnt in self.ngrams_counter.most_common():
            if cnt < MIN_NGRAM_FREQ: break
            if ngram not in {TOKEN_PREFIX, TOKEN_SUFFIX}:
                self.ngram2id[ngram] = len(self.ngram2id)

    def pad_tokenized_texts(self, tokenized_texts):
        padded = []
        for tokens in tokenized_texts:
            padded_tokens = list(map(self.pad_single_token, tokens))
            padded.append(padded_tokens[:self.max_words] + [np.zeros(self.max_ngrams)]*(self.max_words - len(padded_tokens)))
        return padded

    def pad_single_token(self, token):
        return token[:self.max_ngrams] + [0]*(self.max_ngrams - len(token))

    def tokenize_single(self, text):
        tokens = self.words_tokenizer(text)
        tokens = list(map(self.chars_tokenizer, tokens))

        return list(tokens)

    def chars_tokenizer(self, token):
        token = TOKEN_PREFIX + token + TOKEN_SUFFIX
        ngrams = set()
        for ngram_size in range(self.chars_ngram_range[0], self.chars_ngram_range[1]+1):
            grams = zip(*[token[i:] for i in range(ngram_size)])
            ngrams |= {"".join(g) for g in grams}

        return ngrams

    def convert_token_to_ids(self, token):
        return list(map(self.convert_ngrams_to_ids, token))

    def convert_ngrams_to_ids(self, ngrams):
        if not self.ngram2id:
            raise Exception('SeqToLangVectorizer not fitted')

        ngram_ids = []
        for gram in ngrams:
            gram_id = self.ngram2id.get(gram)
            if gram_id: ngram_ids.append(gram_id)
        return ngram_ids


def _default_tokenizer(text):
    return TOKENIZER_REGEX.findall(text.lower().strip())


def _chunkenize(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]