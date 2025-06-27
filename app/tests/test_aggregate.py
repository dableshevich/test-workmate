import pytest

from csv_data import CSVData
from exceptions import AggregateFunctionNotFound


@pytest.fixture
def csv_data():
    path_to_file = 'products.csv'
    return CSVData(path_to_file)


def test_aggregate_success(csv_data):
    csv_data.aggregate('rating=avg')
    assert csv_data.aggregated_data == {'rating_avg': 4.49}

    csv_data.aggregate('rating=min')
    assert csv_data.aggregated_data == {'rating_min': 4.1}

    csv_data.aggregate('rating=max')
    assert csv_data.aggregated_data == {'rating_max': 4.9}


def test_aggregate_not_exists_function(csv_data):
    with pytest.raises(AggregateFunctionNotFound):
        csv_data.aggregate('rating=sum')


def test_aggregate_not_num_column(csv_data):
    with pytest.raises(TypeError):
        csv_data.aggregate('name=avg')
