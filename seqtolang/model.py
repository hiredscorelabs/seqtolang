import torch
from torch import nn
from torch import autograd
from torch.nn.utils.rnn import pack_padded_sequence, pad_packed_sequence


class SeqToLangModel(nn.Module):
    def __init__(self, num_of_ngrams, output_size, hidden_size, embedding_dim):
        super().__init__()

        self.chars_embedding = nn.Embedding(num_embeddings=num_of_ngrams, padding_idx=0, embedding_dim=embedding_dim)
        self.rnn = nn.LSTM(input_size=embedding_dim, hidden_size=hidden_size, bidirectional=True, batch_first=True)
        self.linear = nn.Linear(hidden_size*2, output_size)
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    def forward(self, tokenized_texts):
        batch_size = tokenized_texts.shape[0]
        num_of_words = tokenized_texts.shape[1]
        num_of_ngrams = tokenized_texts.shape[2]

        lens = torch.sum(tokenized_texts.sum(2) > 0, dim=1)

        x = tokenized_texts.view(batch_size * num_of_words, num_of_ngrams)
        embedded = self.chars_embedding(x)
        embedded = embedded.view(batch_size, num_of_words, num_of_ngrams, -1)
        embedded_sum = embedded.sum(2) / lens.view(batch_size, 1, 1).float()

        pack = pack_padded_sequence(embedded_sum, lens, batch_first=True, enforce_sorted=False)
        rnn_outputs, last_hidden = self.rnn(pack)
        unpacked, unpacked_len = pad_packed_sequence(rnn_outputs, batch_first=True)

        if unpacked.size(1) < num_of_words:
            dummy_tensor = autograd.Variable(torch.zeros(batch_size, num_of_words - unpacked.size(1), unpacked.shape[-1])).to(self.device)
            unpacked = torch.cat([unpacked, dummy_tensor], 1)

        output = self.linear(unpacked)

        return output
