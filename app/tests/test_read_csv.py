import pytest

from csv_data import CSVItem, CSVData


def test_create_csv_item_success():
    data = {
        'a': 1,
        'b': 'hello',
        'c': 1.2
    }
    csv_item = CSVItem(data=data)

    assert csv_item.a and isinstance(csv_item.a, float)
    assert csv_item.b and isinstance(csv_item.b, str)
    assert csv_item.c and isinstance(csv_item.c, float)


def test_create_csv_data_success():
    path_to_file = 'products.csv'
    csv_data = CSVData(path_to_file)

    assert len(csv_data.data) == 10
    assert csv_data.aggregated_data is None


def test_create_csv_item_without_data():
    with pytest.raises(TypeError):
        CSVItem()


def test_create_csv_data_without_path_to_file():
    with pytest.raises(TypeError):
        CSVData()


def test_create_csv_data_with_not_exists_file():
    with pytest.raises(FileNotFoundError):
        CSVData('p.csv')


def test_get_not_exists_csv_item_attribute():
    with pytest.raises(TypeError):
        data = {
            'a': 1,
            'b': 'hello',
            'c': 1.2
        }
        csv_item = CSVItem(data=data)
        csv_item['d']
