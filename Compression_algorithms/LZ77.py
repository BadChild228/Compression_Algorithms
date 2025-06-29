from Compression_algorithms import Super

class LZ77(Super.CompressionAlgorithm):
    def __init__(self, window_size=100000, lookahead_size=100000):
        super().__init__("LZ77")
        """
        Args:
            window_size (int): Размер окна поиска
            lookahead_size (int): Размер буфера просмотра вперед
        """
        self.window_size = window_size
        self.lookahead_size = lookahead_size

    def compress(self, text):
        """
        Args:
            text (str): Входная строка для сжатия
        Returns:
            list: Список троек (offset, length, next_char)
        """
        if not text:
            return []

        compressed = []
        i = 0

        while i < len(text):
            search_start = max(0, i - self.window_size)
            search_buffer = text[search_start:i]
            lookahead_buffer = text[i:i + self.lookahead_size]

            best_match = self._find_longest_match(search_buffer, lookahead_buffer)

            if best_match[1] > 0:
                offset, length = best_match
                next_char = text[i + length] if i + length < len(text) else ''
                compressed.append((offset, length, next_char))
                i += length + 1
            else:
                compressed.append((0, 0, text[i]))
                i += 1

        return compressed

    @staticmethod
    def _find_longest_match(search_buffer, lookahead_buffer):
        """
        Args:
            search_buffer (str): Буфер поиска
            lookahead_buffer (str): Буфер просмотра вперед

        Returns:
            tuple: (offset, length) - смещение и длина совпадения
        """
        if not search_buffer or not lookahead_buffer:
            return (0, 0)
        best_offset = 0
        best_length = 0

        for i in range(len(search_buffer)):
            current_length = 0

            while (current_length < len(lookahead_buffer) and
                   current_length < len(search_buffer) - i and
                   search_buffer[i + current_length] == lookahead_buffer[current_length]):
                current_length += 1

            if current_length > best_length:
                best_length = current_length
                best_offset = len(search_buffer) - i

        return (best_offset, best_length)

    """@staticmethod
    def get_encoded_size(compressed):
        BITS_OFFSET = 8
        BITS_LENGTH = 8
        BITS_CHAR = 8

        bits_per_triplet = BITS_OFFSET + BITS_LENGTH + BITS_CHAR
        total_bits = len(compressed) * bits_per_triplet
        return total_bits"""

    @staticmethod
    def decompress(compressed_data):
        """
        Args:
            compressed_data (list): Список троек (offset, length, next_char)

        Returns:
            str: Восстановленная строка
        """
        if not compressed_data:
            return ""

        result = []

        for offset, length, next_char in compressed_data:
            if offset > 0 and length > 0:
                start_pos = len(result) - offset
                for i in range(length):
                    result.append(result[start_pos + i])

            if next_char:
                result.append(next_char)

        return ''.join(result)

