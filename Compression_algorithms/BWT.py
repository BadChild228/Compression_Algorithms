import sys

from Compression_algorithms import Super


class BWT(Super.CompressionAlgorithm):
    def __init__(self, end_marker='$'):
        super().__init__('BWT')
        self.end_marker = end_marker

    def compress(self, text):
        if not text:
            return "", 0

        text_with_marker = text + self.end_marker
        n = len(text_with_marker)

        # Создаем индексы
        rotations_indices = list(range(n))

        # Сортируем индексы
        rotations_indices.sort(key=lambda i: text_with_marker[i:] + text_with_marker[:i])

        # Находим индекс оригинальной строки
        original_index = rotations_indices.index(0)

        # Создаем BWT строку, используя индексы
        bwt_chars = []
        for i in rotations_indices:
            prev_index = (i - 1) % n
            bwt_chars.append(text_with_marker[prev_index])

        return ''.join(bwt_chars), original_index

    def decompress(self, bwt_string, original_index):
        if not bwt_string:
            return ""

        n = len(bwt_string)

        # Создаем отсортированную первую колонку (F)
        f_column = sorted(bwt_string)

        # Создаем таблицу преобразования
        transform_table = {}
        for char in set(bwt_string):
            transform_table[char] = []

        # Заполняем таблицу преобразования
        for char in bwt_string:
            transform_table[char].append(len(transform_table[char]))

        # Создаем массив следующих индексов
        next_indices = [0] * n
        char_counts = {char: 0 for char in set(bwt_string)}

        for i in range(n):
            char = bwt_string[i]
            count = char_counts[char]
            char_counts[char] += 1

            # Находим позицию в F колонке
            pos = 0
            for c in sorted(char_counts.keys()):
                if c < char:
                    pos += char_counts[c]
                elif c == char:
                    pos += count
                    break

            next_indices[i] = pos

        # Восстанавливаем исходную строку
        result = []
        current_index = original_index

        for _ in range(n - 1):  # минус 1, так как не включаем маркер
            current_index = next_indices[current_index]
            if bwt_string[current_index] == self.end_marker:
                break
            result.append(bwt_string[current_index])

        return ''.join(reversed(result))

    @staticmethod
    def _build_suffix_array(text):
        """
        Args:
            text (str): Входная строка

        Returns:
            list: Суффиксный массив
        """
        n = len(text)

        suffixes = []
        for i in range(n):
            suffixes.append((text[i:], i))

        suffixes.sort(key=lambda x: x[0])

        return [suffix[1] for suffix in suffixes]

    @staticmethod
    def _build_transform_table(bwt_string):
        """
        Args:
            bwt_string (str): BWT строка

        Returns:
            list: Таблица преобразований
        """
        n = len(bwt_string)
        char_counts = {}
        for char in bwt_string:
            char_counts[char] = char_counts.get(char, 0) + 1

        sorted_chars = sorted(char_counts.keys())
        char_starts = {}
        pos = 0
        for char in sorted_chars:
            char_starts[char] = pos
            pos += char_counts[char]

        transform_table = [0] * n
        char_positions = char_starts.copy()

        for i in range(n):
            char = bwt_string[i]
            transform_table[i] = char_positions[char]
            char_positions[char] += 1

        return transform_table

    @staticmethod
    def get_encoded_size(encoded_data):
        bwt_string, original_index = encoded_data
        return len(bwt_string) * 8 + sys.getsizeof(original_index)

