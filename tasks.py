import http
import logging
import json

from concurrent.futures import ThreadPoolExecutor
from external.client import YandexWeatherAPI
from urllib.error import HTTPError

from utils import url_by_city_name, CITIES
from exceptions import (
    DataFetchingException,
    DataAnalyzingException,
    DataAggregationException,
    DataCalculationException,
)

logger = logging.getLogger(__name__)


class DataFetchingTask:
    """Fetching data using YandexWeatherAPI."""

    def __init__(self, client: YandexWeatherAPI, timeout=None):
        self.client = client
        self.timeout = timeout
        self.city_to_forecasting_data = {}

    def fetch_forecasting(self, city: str) -> None:
        try:
            url = url_by_city_name(city)
            logger.debug(f'Processing url {url} for city {city}')
            self.city_to_forecasting_data[city] = self.client.get_forecasting(url)
            logger.debug(f'Forecasting data successfully fetched for city {city}')
        except (json.JSONDecodeError, HTTPError) as err:
            logger.warning(f'Unable to fetch data for {city}: {err}')
        except Exception as err:
            logger.exception(err)
            raise DataFetchingException(err)

    def fetch_cities_forecasting(
            self,
            cities: list[str] = CITIES,
            max_workers: int = 5,
    ) -> None:
        try:
            logger.info(f'Fetching forecasting started on {max_workers} workers')
            with ThreadPoolExecutor(max_workers=max_workers) as pool:
                pool.map(self.fetch_forecasting, cities, timeout=self.timeout)
        except (TimeoutError, Exception) as err:
            msg = f'Failed fetch forecasting data: {err}'
            logger.exception(msg)
            raise DataFetchingException(msg)
        logger.info('Fetching forecasting finished')


class DataCalculationTask:
    pass


class DataAggregationTask:
    pass


class DataAnalyzingTask:
    pass
