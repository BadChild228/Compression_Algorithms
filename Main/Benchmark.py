import sys

from Testing_tools.Compress_test import CompressionTester
from Data_load.Data_loading import DataLoader
from Testing_tools.Visualise import ResultVisualizer
from Compression_algorithms.Huffman2 import HuffmanCoding
from Compression_algorithms.Arithmetic import ArithmeticCoding
from Compression_algorithms.BWT import BWT
from Compression_algorithms.LZ77 import LZ77

class EncodingBenchmark:
    """Главный класс-фасад для взаимодействия с системой"""

    def __init__(self):
        self.tester = CompressionTester()
        self.data_loader = DataLoader()
        self.visualizer = ResultVisualizer()

    def register_algorithm(self, algorithm):
        """Регистрирует алгоритм для тестирования"""
        self.tester.add_algorithm(algorithm)

    def load_test_data(self, file_path, file_type="text"):
        """Загружает тестовые данные из файла"""
        return self.data_loader.load_file(file_path, file_type)

    def run_benchmark(self, data):
        """Запускает тестирование всех алгоритмов"""
        return self.tester.test_all(data)

    def show_results(self, results):
        """Отображает результаты тестирования"""
        self.visualizer.print_table(results)


def main():
    benchmark = EncodingBenchmark()
    algorithm1 = HuffmanCoding()
    algorithm2 = ArithmeticCoding()
    algorithm3 = BWT()
    algorithm4 = LZ77()
    algorithms = [algorithm1, algorithm2, algorithm3, algorithm4]
    for alg in algorithms: benchmark.register_algorithm(alg)


    # Загрузка тестовых данных из файла
    data = benchmark.load_test_data(".\sample_text.txt")
    print(sys.getsizeof(data))
    results = benchmark.run_benchmark(data)

    # Отображение результатов
    benchmark.show_results(results)


if __name__ == "__main__":
    main()