import os
import json
import pickle
import torch
from operator import itemgetter
import torch.nn.functional as F
from seqtolang.model import SeqToLangModel

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
LANG_PROBA_THRESHOLD = 0.05
DEFAULT_HIDDEN_SIZE = 32
DEFAULT_EMBEDDING_DIM = 16

class Detector():
    def __init__(self, model=None, label2id=None, vectorizer=None):
        self.label2id = label2id or json.load(open(CURRENT_DIR +'/checkpoints/default_label2id.json', 'r'))
        self.vectorizer = vectorizer or pickle.load(open(CURRENT_DIR + '/checkpoints/default_vectorizer.pickle', 'rb'))
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        if model:
            self.model = model.to(self.device)
        else:
            self.model = SeqToLangModel(num_of_ngrams=len(self.vectorizer.ngram2id),
                                        output_size=len(self.label2id),
                                        hidden_size=DEFAULT_HIDDEN_SIZE,
                                        embedding_dim=DEFAULT_EMBEDDING_DIM).to(self.device).eval()

            state_dict = torch.load(CURRENT_DIR + '/checkpoints/default_model.state_dict', map_location=self.device)
            self.model.load_state_dict(state_dict)



    def detect(self, text, aggregated=True):
        v = torch.tensor(self.vectorizer.vectorize([text])).long().to(self.device)
        with torch.no_grad():
            output = self.model(v)
            probas = F.softmax(output, 2)
            mask = v.sum(2) > 0
            masked = probas[mask]

        if aggregated:
            means = masked.mean(0)

            results = []
            for label, label_id in self.label2id.items():
                if means[label_id].item() > LANG_PROBA_THRESHOLD:
                    results.append((label, means[label_id].item()))

            results = sorted(results, key=itemgetter(1), reverse=True)
            return results if results else [('unk', 1)]
        else:
            results = []
            id2label = {i:label for label, i in self.label2id.items()}
            for token in masked:
                value, ind = torch.max(token, 0)
                results.append(id2label[int(ind)])

            return results


    def print_output(self, output, text):
        for token, pred in zip(text.split(), output[0]):
            print(token)
            for label, label_id in self.label2id.items():
                print(label, ':', round(F.sigmoid(pred[label_id]).item(), 3))
            print()
