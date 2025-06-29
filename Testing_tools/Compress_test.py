import sys
import time
from Testing_tools.Metrics import CompressionMetrics
from decimal import Decimal

class CompressionTester:
    """Класс для тестирования и сравнения алгоритмов кодирования"""

    def __init__(self):
        self.algorithms = []
        self.results = {}

    def add_algorithm(self, algorithm):
        """Добавляет алгоритм в список для тестирования"""
        self.algorithms.append(algorithm)

    def test_all(self, data):
        """Тестирует все зарегистрированные алгоритмы на указанных данных"""
        for algorithm in self.algorithms:
            self.results[algorithm.name] = self._test_single_algorithm(algorithm, data)
        return self.results


    def _test_single_algorithm(self, algorithm, data):
        """Тестирует отдельный алгоритм и собирает метрики"""
        result = {}

        # Замер исходного размера
        original_size = len(data) * 8
        result["original_size"] = original_size

        # Замер времени кодирования
        start_time = Decimal(time.time())
        encoded_data = algorithm.compress(data)
        encoding_time = Decimal(time.time()) - start_time

        # Сбор метрик
        encoded_size = algorithm.get_encoded_size(encoded_data)
        result["encoded_size"] = encoded_size
        result["encoding_time"] = encoding_time
        result["compression_ratio"] = CompressionMetrics.compression_ratio(original_size, encoded_size)
        result["space_saving"] = CompressionMetrics.space_saving(original_size, encoded_size)
        result["encoding_speed"] = CompressionMetrics.encoding_speed(original_size, encoding_time)

        algorithm_name = type(algorithm).__name__
        filename = f"{algorithm_name}_compressed.txt"

        if isinstance(encoded_data, str):
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(encoded_data)
        elif isinstance(encoded_data, list):
            import json
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(encoded_data, f)
        else:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(str(encoded_data))

        return result

