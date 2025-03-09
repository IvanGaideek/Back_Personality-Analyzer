import pickle

from keras_preprocessing.sequence import pad_sequences


class Tokenizer:
    def __init__(self, path):
        self.path = path
        self.tokenizer = None
        self.vocab_size = None
        self.max_len = None

    def to_data_for_model(self, texts: list):
        sequence = self.tokenizer.texts_to_sequences(texts)
        padded = pad_sequences(sequence, maxlen=self.max_len, padding='post')
        return padded

    def load(self):
        with open(self.path, 'rb') as f:
            data = pickle.load(f)

        self.tokenizer = data['tokenizer']
        self.vocab_size = data['vocab_size']
        self.max_len = data['max_len']
