import csv

from tabulate import tabulate

from exceptions import OperatorNotFound, AggregateFunctionNotFound


class CSVItem:
    def __init__(self, data: dict):
        for key, value in data.items():
            value = self._convert_values(value)
            setattr(self, key, value)

    def _convert_values(self, value):
        try:
            return float(value)
        except ValueError:
            return value

    def __getitem__(self, attr: str):
        try:
            return getattr(self, attr)
        except AttributeError as e:
            raise e('У таблицы нет такой колонки')


class CSVData:
    OPERATORS = ['>', '<', '=']

    def __init__(self, file_path: str):
        with open(file_path, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            self.data = []
            self.aggregated_data = None

            for data_item in list(reader):
                csv_item = CSVItem(data_item)
                self.data.append(csv_item)

    def min(self, column: str):
        min_value = float('inf')
        for item in self.data:
            min_value = min(item[column], min_value)

        self.aggregated_data = {column + '_min': min_value}

    def max(self, column: str):
        max_value = float('-inf')
        for item in self.data:
            max_value = max(item[column], max_value)

        self.aggregated_data = {column + '_max': max_value}

    def avg(self, column: str):
        avg_value = 0
        for item in self.data:
            avg_value += item[column]
        avg_value /= len(self.data)

        self.aggregated_data = {column + '_avg': avg_value}

    def split_expression(self, condition: str):
        operator = None
        for op in self.OPERATORS:
            if op in condition:
                operator = op

        if not operator:
            raise OperatorNotFound(
                f'Доступны только эти операторы сравнения: {self.OPERATORS}.'
            )

        condition = condition.split(operator)
        try:
            return (condition[0], operator, float(condition[1]))
        except ValueError:
            return (condition[0], operator, condition[1])

    def compare(self, a, b, op) -> bool:
        ops = {
            '>': lambda x, y: x > y,
            '<': lambda x, y: x < y,
            '=': lambda x, y: x == y,
        }
        return ops[op](a, b)

    def filter(self, condition: str):
        '''
        Фильтрует данные в таблице.

        Шаблон для фильтрации: <Название колонки><оператор сравнения><значение>

        Доступные операторы для сравнения: <, >, =
        '''

        column, operator, value = self.split_expression(condition)
        filtered_data = [
            item for item in self.data
            if self.compare(item[column], value, operator)
        ]

        self.data = filtered_data

    def aggregate(self, condition: str):
        '''
        Агрегация значений таблицы.

        Поддерживает следующие операции:
        - avg: находит среднее значение по колонке
        - min: находит минимальное значение в колонке
        - max: находит максимальное значение в колонке

        Шаблон для агрегации: <Название колонки>=<операция>

        Примечание: поддерживает только колонки с числовыми типами данных.
        '''

        column, value = tuple(condition.split('='))

        if isinstance(self.data[0][column], str):
            raise TypeError(
                'Агрегация работает только с числовыми типами данных.'
            )

        match (value):
            case 'avg':
                self.avg(column)
            case 'min':
                self.min(column)
            case 'max':
                self.max(column)
            case _:
                raise AggregateFunctionNotFound(
                    'Агрегация не поддерживает данную операцию.'
                )

    def print(self, tablefmt: str = 'grid', headers: str = 'keys'):
        '''
        Выводит данные в консоль.

        Параметры:
        - tablefmt: формат таблицы ("grid", "pipe", "html").
        - headers: способ отображения заголовков ("keys", "firstrow").
        '''

        if self.aggregated_data:
            data = [self.aggregated_data]
        else:
            data = [vars(item) for item in self.data]
        print(tabulate(data, tablefmt=tablefmt, headers=headers))
