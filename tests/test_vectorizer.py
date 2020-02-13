from seqtolang.vectorizer import SeqToLangVectorizer


def test_vectorizer():
    texts = ['this is english text', 'seventeen']
    vectorizer = SeqToLangVectorizer().fit(texts)

    v = vectorizer.vectorize(texts)

    assert len(v.shape) == 3
    assert v.shape[0] == 2