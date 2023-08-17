from pathlib import Path

import pytest
import pytest_dependency

from tasks import (
    DataFetchingTask,
    DataCalculationTask,
    DataAggregationTask,
    DataAnalyzingTask,
)
from utils import (
    DATE_FIELD,
    HOURS_START_FIELD,
    HOURS_END_FIELD,
    HOURS_COUNT_FIELD,
    RELEVANT_COND_HOURS_FIELD,
    TEMP_AVG_FIELD,
)


def test_data_fetching_task(yandex_weather_api):
    data_fetcher = DataFetchingTask(client=yandex_weather_api)
    data_fetcher.run()
    city_to_forecasting_data = data_fetcher.city_to_forecasting_data
    assert len(city_to_forecasting_data) == 16
    assert not city_to_forecasting_data['MADRID']
    city_to_forecasting_data.pop('MADRID')
    for _, forecasting_data in city_to_forecasting_data.items():
        assert 'fact' in forecasting_data


def test_data_calculation_task(city_to_forecasting_data: dict):
    data_calculator = DataCalculationTask(city_to_forecasting_data)
    data_calculator.run()

    city_to_analyzed_days_info = data_calculator.city_to_analyzed_days_info
    assert city_to_analyzed_days_info
    for _, days_info in city_to_analyzed_days_info.items():
        assert all(
            field is not None
            for day_info in days_info
            for field in (
                day_info.get(DATE_FIELD),
                day_info.get(HOURS_START_FIELD),
                day_info.get(HOURS_END_FIELD),
                day_info.get(HOURS_COUNT_FIELD),
                day_info.get(RELEVANT_COND_HOURS_FIELD),
                day_info.get(TEMP_AVG_FIELD),
            ))


@pytest.mark.dependency()
def test_data_aggregation_task(city_to_analyzed_days_info):
    data_aggregator = DataAggregationTask(city_to_analyzed_days_info)
    aggregation_results_path = None
    try:
        aggregation_results_path = data_aggregator.run(save_format='csv')
        assert aggregation_results_path.exists()
        assert aggregation_results_path.parent.is_dir()
        assert [
            *aggregation_results_path.parent.glob('*.csv'),
            *aggregation_results_path.parent.glob('*.json'),
        ]
    finally:
        if aggregation_results_path is not None:
            # Remove created file.
            aggregation_results_path.unlink(missing_ok=True)
            aggregation_results_path.parent.rmdir()


@pytest.mark.dependency('test_data_aggregation_task')
def test_data_analyzing_task(aggregation_path: Path):
    data_analyzer = DataAnalyzingTask(aggregation_path)
    correct_results = [
        ('ABUDHABI', 34.27275, 8.75),
        ('CAIRO', 33.394, 11.0),
        ('BEIJING', 31.6325, 9.75),
    ]
    top_index = 3
    relevant_cities = data_analyzer.run(top_index=top_index)
    assert len(correct_results) == len(relevant_cities)
    msgs = (
        'Incorrect city name: %s, must be %s',
        'Incorrect temperature: %s, must be %s',
        'Incorrect relevant days count: %s, must be %s',
    )
    for correct, relevant in zip(correct_results, relevant_cities):
        for i in range(3):
            assert correct[i] == relevant[i], msgs[i] % (relevant[i], correct[i])
