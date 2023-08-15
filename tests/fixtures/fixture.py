from pathlib import Path

import pytest

from external.client import YandexWeatherAPI


@pytest.fixture
def yandex_weather_api():
    return YandexWeatherAPI()


@pytest.fixture
def aggregation_path():
    return Path('.').parent.parent / 'mock_aggregation_data' / 'results.csv'
