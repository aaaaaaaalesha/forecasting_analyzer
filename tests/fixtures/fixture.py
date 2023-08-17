import os
from pathlib import Path

import pytest

from external.client import YandexWeatherAPI


@pytest.fixture
def yandex_weather_api():
    return YandexWeatherAPI()


@pytest.fixture
def aggregation_path():
    rel_path = Path('tests') / 'mock_aggregation_data' / 'results.csv'
    return Path(rel_path).absolute()
