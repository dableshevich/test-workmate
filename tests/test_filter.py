import pytest

from app.csv_data import CSVData
from app.exceptions import OperatorNotFound


@pytest.fixture
def csv_data():
    path_to_file = 'products.csv'
    return CSVData(path_to_file)


def test_equals_filter_success(csv_data):
    csv_data.filter('brand=apple')

    for item in csv_data.data:
        assert item['brand'] == 'apple'
    assert len(csv_data.data) == 4


def test_greater_then_filter_success(csv_data):
    csv_data.filter('rating>4.5')

    for item in csv_data.data:
        assert item['rating'] > 4.5
    assert len(csv_data.data) == 5


def test_least_then_filter_success(csv_data):
    csv_data.filter('rating<4.5')

    for item in csv_data.data:
        assert item['rating'] < 4.5
    assert len(csv_data.data) == 4


def test_split_expression_success(csv_data):
    assert csv_data.split_expression(
        'rating>4.5'
    ) == ('rating', '>', 4.5)
    assert csv_data.split_expression(
        'brand=apple'
    ) == ('brand', '=', 'apple')


def test_compare_success(csv_data):
    assert not csv_data.compare(1, 2, '>')
    assert csv_data.compare(1, 2, '<')
    assert not csv_data.compare(1, 2, '=')


def test_split_expression_incorrect(csv_data):
    with pytest.raises(OperatorNotFound):
        csv_data.split_expression('b')


def test_compare_incorrect(csv_data):
    with pytest.raises(TypeError):
        csv_data.compare('a')


def test_filter_int_colums_with_string_value(csv_data):
    with pytest.raises(TypeError):
        csv_data.filter('raiting>apple')
