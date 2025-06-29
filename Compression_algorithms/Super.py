import sys


class CompressionAlgorithm:
    def __init__(self, name):
        self.name = name

    def compress(self, data):
        raise NotImplementedError

    def decompress(self, compressed_data):
        raise NotImplementedError

    @staticmethod
    def get_encoded_size(compressed_data):
        return sys.getsizeof(compressed_data)