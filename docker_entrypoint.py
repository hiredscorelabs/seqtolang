import os
import sys
from seqtolang import Detector

detector = Detector()

if (os.environ.get('SEQTOLANG_TEXT') is None):
    print("Make sure to pass SEQTOLANG_TEXT environment variable.")
    sys.exit(1)

text = os.environ['SEQTOLANG_TEXT']
tokens = detector.detect(text, aggregated=False)

print(text.split(" "))
print(tokens)

