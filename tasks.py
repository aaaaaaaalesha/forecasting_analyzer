import logging
import json
import multiprocessing

from abc import ABC, abstractmethod
from concurrent.futures import (
    ThreadPoolExecutor,
    ProcessPoolExecutor,
)

from urllib.error import HTTPError

from utils import url_by_city_name, CITIES
from external.client import YandexWeatherAPI
from external.analyzer import analyze_json
from exceptions import (
    DataFetchingException,
    DataAnalyzingException,
    DataAggregationException,
    DataCalculationException,
)

logger = logging.getLogger(__name__)

MAX_WORKERS = multiprocessing.cpu_count() - 1


class Task(ABC):
    """Abstract task class."""

    @abstractmethod
    def run(self, *args, **kwargs):
        pass


class DataFetchingTask(Task):
    """Fetching data using YandexWeatherAPI."""

    def __init__(self, client: YandexWeatherAPI, **kwagrs):
        super().__init__(**kwagrs)
        self.client = client
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

    def run(
            self,
            cities: list[str] = CITIES,
            max_workers: int = MAX_WORKERS,
            timeout: float | None = None,
    ) -> None:
        try:
            logger.info(f'Fetching forecasting started on {max_workers} workers')
            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                executor.map(self.fetch_forecasting, cities, timeout=timeout)
        except (TimeoutError, Exception) as err:
            msg = f'Failed fetch forecasting data: {err}'
            logger.exception(msg)
            raise DataFetchingException(msg)
        logger.info('Fetching forecasting finished')


class DataCalculationTask(Task):
    def __int__(self, city_to_forecasting_data: dict):
        self.city_to_forecasting_data = city_to_forecasting_data
        self.queue = multiprocessing.Queue()

    @staticmethod
    def __is_available_data(day_info: dict) -> bool:
        return all(
            field is not None
            for field in (  # required fields
                day_info.get('date'),
                day_info.get('hours_start'),
                day_info.get('hours_end'),
                day_info.get('hours_count'),
                day_info.get('relevant_cond_hours'),
                day_info.get('temp_avg'),
            ))

    def _analyze_forecast_producer(
            self,
            city: str,
            forecasting_data: dict,
    ):
        analyzed_data: dict = analyze_json(forecasting_data)
        days_info: list[dict] | None = analyzed_data.get('days')
        if analyzed_data and days_info is not None:
            filtered_days_info = [
                day_info
                for day_info in days_info
                if self.__is_available_data(day_info)
            ]
            self.queue.put((city, filtered_days_info))

    def run(
            self,
            max_workers: int = MAX_WORKERS,
            timeout: float | None = None,
    ):
        with ProcessPoolExecutor(max_workers=max_workers) as executor:
            executor.map(
                self._analyze_forecast_producer,
                self.city_to_forecasting_data.items(),
                timeout=timeout,
            )


class DataAggregationTask:
    pass


class DataAnalyzingTask:
    pass
