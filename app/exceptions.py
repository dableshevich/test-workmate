class OperatorNotFound(Exception):
    '''
    Ошибка - оператор сравнения не найден.
    '''

    @property
    def message(message: str):
        return message


class AggregateFunctionNotFound(Exception):
    '''
    Ошибка - функция агрегации не найдена.
    '''

    @property
    def message(message: str):
        return message
