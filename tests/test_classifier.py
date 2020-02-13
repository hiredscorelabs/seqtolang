import torch
from seqtolang.model import SeqToLangModel
from seqtolang.vectorizer import SeqToLangVectorizer


def test_classifier():
    texts = ['this is english text', 'this']
    vectorizer = SeqToLangVectorizer().fit(texts)
    v = torch.tensor(vectorizer.vectorize(texts)).long()

    model = SeqToLangModel(num_of_ngrams=len(vectorizer.ngram2id),
                           output_size=10,
                           hidden_size=8,
                           embedding_dim=8)

    output = model(v)

    assert output.shape == (v.shape[0], v.shape[1], 10)
