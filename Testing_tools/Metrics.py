import math
import collections


class CompressionMetrics:
    """Класс для расчёта различных метрик эффективности кодирования"""
    @staticmethod
    def compression_ratio(original_size, encoded_size):
        """Вычисляет коэффициент сжатия"""
        return (original_size - encoded_size)/ original_size if encoded_size > 0 else 0

    @staticmethod
    def space_saving(original_size, encoded_size):
        """Вычисляет экономию пространства"""
        return original_size - encoded_size if original_size > 0 else 0

    @staticmethod
    def encoding_speed(data_size, encoding_time):
        """Вычисляет скорость кодирования в байтах в секунду"""
        return data_size / encoding_time if encoding_time > 0 else 0

    @staticmethod
    def entropy(original_string: str):
        """Вычисляет теоретический предел сжатия"""
        if not original_string:
            return 0

        entropy = 0.0
        length = len(original_string)
        freq = collections.Counter(original_string)

        for count in freq.values():
            probability = count / length
            entropy -= probability * math.log2(probability)

        return entropy





