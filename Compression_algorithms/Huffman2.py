from collections import Counter
import heapq
import os
import pickle

from Compression_algorithms import Super


class HuffmanNode:
    """Узел дерева Хаффмана"""

    def __init__(self, char=None, freq=0, left=None, right=None):
        self.char = char  # Символ (None для внутренних узлов)
        self.freq = freq  # Частота
        self.left = left  # Левый потомок
        self.right = right  # Правый потомок

    def __lt__(self, other):
        if self.freq == other.freq:
            # Если частоты равны, сравниваем по символу для стабильности
            if self.char is None and other.char is None:
                return False
            elif self.char is None:
                return False
            elif other.char is None:
                return True
            return self.char < other.char
        return self.freq < other.freq

    def is_leaf(self):
        """Проверка, является ли узел листом"""
        return self.char is not None


class HuffmanCoding(Super.CompressionAlgorithm):
    """Реализация кодирования Хаффмана"""

    def __init__(self):
        super().__init__("Huffman Coding")
        self.root = None
        self.codes = {}
        self.reverse_codes = {}

    def compress(self, text):
        """
        Сжатие текста алгоритмом Хаффмана

        Args:
            text (str): Исходный текст

        Returns:
            tuple: (сжатая битовая строка, дерево кодов, исходная длина)
        """
        if not text:
            return "", {}, 0

        # Особый случай: только один уникальный символ
        if len(set(text)) == 1:
            char = text[0]
            return "0" * len(text), {char: "0"}, len(text)

        # 1. Подсчет частот
        frequencies = Counter(text)

        # 2. Построение дерева Хаффмана
        self.root = self._build_huffman_tree(frequencies)

        # 3. Генерация кодов
        self.codes = {}
        self.generate_codes(self.root, "")

        # 4. Кодирование текста
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

        # Декодирование
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

    def _build_huffman_tree(self, frequencies):
        """Построение дерева Хаффмана"""
        # Создаем приоритетную очередь из листьев
        heap = []
        for char, freq in frequencies.items():
            node = HuffmanNode(char, freq)
            heapq.heappush(heap, node)

        # Строим дерево снизу вверх
        while len(heap) > 1:
            # Извлекаем два узла с наименьшими частотами
            left = heapq.heappop(heap)
            right = heapq.heappop(heap)

            # Создаем новый внутренний узел
            merged_freq = left.freq + right.freq
            merged_node = HuffmanNode(None, merged_freq, left, right)

            # Добавляем обратно в очередь
            heapq.heappush(heap, merged_node)

        return heap[0] if heap else None

    def generate_codes(self, node, initial_code=""):
        """Генерация кодов Хаффмана (итеративный обход дерева)"""
        if node is None:
            return

        stack = [(node, initial_code)]  # (узел, текущий код)

        while stack:
            current, code = stack.pop()

            # Если это лист, сохраняем код
            if current.is_leaf():
                self.codes[current.char] = code if code else "0"
            else:
                # Добавляем потомков в стек
                if current.right:
                    stack.append((current.right, code + "1"))
                if current.left:
                    stack.append((current.left, code + "0"))

    def get_tree_structure(self):
        """Получение структуры дерева для визуализации (итеративно)"""
        if self.root is None:
            return []

        result = []
        stack = [(self.root, 0)]  # (узел, глубина)

        while stack:
            node, depth = stack.pop()
            indent = "  " * depth

            if node.is_leaf():
                result.append(f"{indent}'{node.char}' (freq: {node.freq})")
            else:
                result.append(f"{indent}Internal (freq: {node.freq})")

                if node.right:
                    stack.append((node.right, depth + 1))
                if node.left:
                    stack.append((node.left, depth + 1))

        return result

    def save_to_file(self, encoded_text, codes, original_length, filename):
        """
        Args:
            encoded_text (str): Закодированный текст (битовая строка)
            codes (dict): Словарь кодов Хаффмана
            original_length (int): Длина исходного текста
            filename (str): Имя файла для сохранения
        """
        data = {
            'encoded_text': encoded_text,
            'codes': codes,
            'original_length': original_length
        }

        # Сохраняем данные в файл
        with open(filename, 'wb') as file:
            pickle.dump(data, file)

        # Рассчитываем степень сжатия
        if os.path.exists(filename):
            file_size = os.path.getsize(filename)
            compression_ratio = file_size / original_length if original_length else 0
            print(f"Файл сохранен как {filename} (размер: {file_size} байт)")

    def load_from_file(self, filename):
        """
        Args:
            filename (str): Имя файла для чтения

        Returns:
            tuple: (закодированный текст, коды, исходная длина)
        """
        with open(filename, 'rb') as file:
            data = pickle.load(file)

        encoded_text = data['encoded_text']
        codes = data['codes']
        original_length = data['original_length']

        return encoded_text, codes, original_length

    def compress_to_file(self, text, filename):
        """
        Сжимает текст и сохраняет результат в файл

        Args:
            text (str): Исходный текст для сжатия
            filename (str): Имя файла для сохранения
        """
        encoded_text, codes, original_length = self.compress(text)
        self.save_to_file(encoded_text, codes, original_length, filename)
        return encoded_text, codes, original_length

    def decompress_from_file(self, filename):
        """
        Читает сжатые данные из файла и декодирует их

        Args:
            filename (str): Имя файла для чтения

        Returns:
            str: Декодированный текст
        """
        encoded_text, codes, original_length = self.load_from_file(filename)
        return self.decompress(encoded_text, codes, original_length)

    @staticmethod
    def get_encoded_size(compressed_data):
        encoded_text, codes, text = compressed_data
        return len(encoded_text)

if __name__ == "__main__":
    huffman = HuffmanCoding()

    with open('Original_text.txt', 'r+') as f:
        text = str(f.read())

    with open('Original_text.bin', 'w+') as f:
        f.write(' '.join(format(ord(i), '08b') for i in text))

    with open('Huffman_compressed.txt', 'w+') as f:
        f.write(str(huffman.compress(text)))

    huffman.compress_to_file(text, "Huffman_compressed.bin")

    decoded_text = huffman.decompress_from_file("Huffman_compressed.bin")

    print(f"Текст совпадает с оригиналом: {text == decoded_text}")