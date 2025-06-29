from tabulate import tabulate

class ResultVisualizer:
    """Класс для визуализации результатов тестирования"""

    def print_table(self, results):

        """Выводит результаты в виде таблицы"""
        headers = ["Алгоритм", "Исходный размер", "Сжатый размер",
                   "Коэфф. сжатия", "Экономия", "Время (сек)", "Скорость (КБ/с)"]

        table_data = []
        for algo_name, metrics in results.items():
            table_data.append([
                algo_name,
                metrics["original_size"],
                metrics["encoded_size"],
                f"{metrics['compression_ratio']:.2f}",
                f"{metrics['space_saving']} Bit",
                f"{metrics['encoding_time']:.4f}",
                f"{metrics['encoding_speed'] / 1024:.2f}"
            ])

        print(tabulate(table_data, headers=headers, tablefmt="grid"))
