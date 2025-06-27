import csv

from tabulate import tabulate

from exceptions import OperatorNotFound, AggregateFunctionNotFound


class CSVItem:
    '''
    Строка в таблице.
    '''

    def __init__(self, data: dict) -> None:
        for key, value in data.items():
            value = self._convert_values(value)
            setattr(self, key, value)

    def _convert_values(self, value: str) -> str | float:
        '''
        Конвертирует string в float, если возможно.
        '''

        try:
            return float(value)
        except ValueError:
            return value

    def __getitem__(self, attr: str) -> str | float:
        '''
        Возвращает значение атрибута класса, запрошенного
        в виде class_object[<attr>].
        '''

        try:
            return getattr(self, attr)
        except AttributeError as e:
            raise e('У таблицы нет такой колонки')


class CSVData:
    '''
    Таблица, полученная из csv-файла.
    '''

    OPERATORS = ['>', '<', '=']

    def __init__(self, file_path: str):
        with open(file_path, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            self.data = []
            self.aggregated_data = None

            for data_item in list(reader):
                csv_item = CSVItem(data_item)
                self.data.append(csv_item)

    def min(self, column: str) -> None:
        '''
        Поиск минимального числа в колонке.
        '''

        min_value = float('inf')
        for item in self.data:
            min_value = min(item[column], min_value)

        self.aggregated_data = {column + '_min': min_value}

    def max(self, column: str) -> None:
        '''
        Поиск максимального чесла в колонке.
        '''

        max_value = float('-inf')
        for item in self.data:
            max_value = max(item[column], max_value)

        self.aggregated_data = {column + '_max': max_value}

    def avg(self, column: str) -> None:
        '''
        Поиск среднего числа для колонки.
        '''

        avg_value = 0
        for item in self.data:
            avg_value += item[column]
        avg_value /= len(self.data)

        self.aggregated_data = {column + '_avg': avg_value}

    def split_expression(self, condition: str) -> tuple:
        '''
        Разделяет строку вида <Название колонки><Оператор сравнения><Значение>
        на три соответствующих переменных.
        '''

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

    def compare(self, a: str | float, b: str | float, op: str) -> bool:
        '''
        Сравнивает переданные в метод значения между собой.
        '''

        ops = {
            '>': lambda x, y: x > y,
            '<': lambda x, y: x < y,
            '=': lambda x, y: x == y,
        }
        return ops[op](a, b)

    def filter(self, condition: str) -> None:
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

    def aggregate(self, condition: str) -> None:
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

    def print(self, tablefmt: str = 'grid', headers: str = 'keys') -> None:
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
