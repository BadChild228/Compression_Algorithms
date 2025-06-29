import heapq
from collections import Counter



class HuffmanNode:
    def __init__(self, char=None, freq=0, left=None, right=None):
        self.char = char
        self.freq = freq
        self.left = left
        self.right = right

    def __lt__(self, other):
        if self.freq == other.freq:
            if self.char is None and other.char is None:
                return False
            elif self.char is None:
                return False
            elif other.char is None:
                return True
            return self.char < other.char
        return self.freq < other.freq

    def is_leaf(self):
        return self.char is not None

class HuffmanCoding:
    def __init__(self):
        self.root = None
        self.codes = {}
        self.reverse_codes = {}

    def compress(self, text):
        """
        Args:
            text (str): Исходный текст

        Returns:
            tuple: (сжатая битовая строка, дерево кодов, исходная длина)
        """
        if not text:
            return "", {}, 0

        if len(set(text)) == 1:
            char = text[0]
            return "0" * len(text), {char: "0"}, len(text)

        frequencies = Counter(text)

        self.root = self._build_huffman_tree(frequencies)
        self.codes = {}
        self._generate_codes(self.root, "")

        encoded_text = ""
        for char in text:
            encoded_text += self.codes[char]

        return encoded_text, self.codes, len(text)

    def decompress(self, encoded_text, codes, original_length):
        """
        Args:
            encoded_text (str): Сжатая битовая строка
            codes (dict): Таблица кодов Хаффмана
            original_length (int): Длина исходного текста

        Returns:
            str: Восстановленный текст
        """
        if original_length == 0:
            return ""

        self.reverse_codes = {code: char for char, code in codes.items()}

        if len(codes) == 1:
            char = list(codes.keys())[0]
            return char * original_length

        decoded_text = ""
        current_code = ""

        for bit in encoded_text:
            current_code += bit
            if current_code in self.reverse_codes:
                decoded_text += self.reverse_codes[current_code]
                current_code = ""
                if len(decoded_text) == original_length:
                    break
        return decoded_text

    @staticmethod
    def _build_huffman_tree(frequencies):
        heap = []
        for char, freq in frequencies.items():
            node = HuffmanNode(char, freq)
            heapq.heappush(heap, node)

        while len(heap) > 1:
            left = heapq.heappop(heap)
            right = heapq.heappop(heap)

            merged_freq = left.freq + right.freq
            merged_node = HuffmanNode(None, merged_freq, left, right)
            heapq.heappush(heap, merged_node)

        return heap[0] if heap else None

    def _generate_codes(self, node, code):
        if node is None:
            return

        if node.is_leaf():
            self.codes[node.char] = code if code else "0"
            return

        self._generate_codes(node.left, code + "0")
        self._generate_codes(node.right, code + "1")

if __name__ == "__main__":
