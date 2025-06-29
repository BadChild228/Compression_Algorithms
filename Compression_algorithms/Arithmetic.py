import sys
from collections import Counter
from decimal import Decimal, getcontext
import math
from sys import getsizeof
import pickle

from Compression_algorithms import Super

class ArithmeticCoding(Super.CompressionAlgorithm):
    def __init__(self, name = 'Arithmetic', precision=50):
        super().__init__("Arithmetic Coding")
        """
        Args:
            precision (int): Точность вычислений (количество знаков после запятой)
        """
        getcontext().prec = precision
        self.precision = precision

    def compress(self, text):
        """
        Args:
            text (str): Исходный текст

        Returns:
            tuple: (код, таблица вероятностей, длина)
        """
        if not text:
            return None, {}, 0

        probabilities = self._calculate_probabilities(text)
        cumulative_probs = self._create_cumulative_table(probabilities)

        low = Decimal('0')
        high = Decimal('1')

        for symbol in text:
            range_size = high - low
            symbol_low, symbol_high = cumulative_probs[symbol]

            high = low + range_size * symbol_high
            low = low + range_size * symbol_low

        code = (low + high) / 2

        return Decimal(code), probabilities, len(text)

    def decompress(self, encoded_data):
        code, probabilities, length = encoded_data
        """
        Args:
            code (float): Арифметический код
            probabilities (dict): Таблица вероятностей символов
            length (int): Длина исходного текста

        Returns:
            str: Восстановленный текст
        """
        if length == 0:
            return ""

        code = Decimal(str(code))
        cumulative_probs = self._create_cumulative_table(probabilities)

        intervals = []
        for symbol, (low, high) in cumulative_probs.items():
            intervals.append((low, high, symbol))
        intervals.sort()

        result = []

        for _ in range(length):
            symbol = self._find_symbol(code, intervals)
            result.append(symbol)

            symbol_low, symbol_high = cumulative_probs[symbol]
            range_size = symbol_high - symbol_low
            code = (code - symbol_low) / range_size

        return ''.join(result)

    @staticmethod
    def _calculate_probabilities(text):
        """Вычисление вероятностей символов"""
        counter = Counter(text)
        total = len(text)

        probabilities = {}
        for char, count in counter.items():
            probabilities[char] = Decimal(count) / Decimal(total)

        return probabilities

    @staticmethod
    def _create_cumulative_table(probabilities):
        """Создание кумулятивной таблицы вероятностей"""
        cumulative_probs = {}
        cumulative = Decimal('0')

        for symbol in sorted(probabilities.keys()):
            prob = probabilities[symbol]
            cumulative_probs[symbol] = (cumulative, cumulative + prob)
            cumulative += prob

        return cumulative_probs

    @staticmethod
    def _find_symbol(code, intervals):
        """Поиск символа по коду в интервалах"""
        for low, high, symbol in intervals:
            if low <= code < high:
                return symbol

        return intervals[-1][2]

    @staticmethod
    def get_encoded_size(compressed_data):
        code, probabilities, text = compressed_data
        """
        Args:
            code (float): число, представляющее диапазон
            probabilities: таблица вероятностей 
            text_length (int): длина исходного текста

        Returns:
            int: размер в битах
        """
        return (getsizeof(str(abs(code))) + getsizeof(str(probabilities.keys())) + getsizeof(str(probabilities.values))
                + getsizeof(text))

if __name__ == '__main__':
    arithmetic_codding = ArithmeticCoding()

    import os

    print(os.getcwd())

    with open('Original_text.txt', 'r+') as f:
        text = f.read()

    with open('Arithmetic_compressed.txt', 'w+') as f:
        f.write(str(arithmetic_codding.compress(text)))

    with open('Arithmetic_compressed.bin', 'w+') as f:
        f.write(pickle.dumps(arithmetic_codding.compress(text)))
