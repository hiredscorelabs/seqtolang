# -*- coding: utf-8 -*-
from seqtolang import Detector


def test_detector_aggregated():
    detector = Detector()
    output = detector.detect('Je rentre chez moi Je rentre chez moi this is very english sentence')

    assert type(output) == list
    assert len(output) > 0
    assert type(output[0]) == tuple



def test_detector_not_aggregated():
    detector = Detector()
    output = detector.detect('Je rentre chez moi Je rentre chez moi this is very english sentence', aggregated=False)

    assert type(output) == list
    assert len(output) > 0
    assert type(output[0]) == str
