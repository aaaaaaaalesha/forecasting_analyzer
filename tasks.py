import json
import logging
from abc import ABC, abstractmethod
from concurrent.futures import (
    ThreadPoolExecutor,
    ProcessPoolExecutor,
)
from multiprocessing import cpu_count, Manager, Queue
from pathlib import Path
from urllib.error import HTTPError

import pandas as pd

from exceptions import (
    DataFetchingException,
    DataAggregationException,
    DataAnalyzingException,
)
from external.analyzer import analyze_json
from external.client import YandexWeatherAPI
from utils import (
    url_by_city_name,
    CITIES,
    CITY_FIELD,
    DAYS_FIELD,
    DATE_FIELD,
    HOURS_START_FIELD,
    HOURS_END_FIELD,
    HOURS_COUNT_FIELD,
    RELEVANT_COND_HOURS_FIELD,
    TEMP_AVG_FIELD,
    RATING_FIELD,
    TEMP_AVG_MEAN_FIELD,
    RELEVANT_COND_HOURS_MEAN_FIELD,
    MEAN_SUFFIX,
)

logger = logging.getLogger(__name__)

MAX_WORKERS = cpu_count() - 1


class Task(ABC):
    """Abstract task class."""

    @abstractmethod
    def run(self, *args, **kwargs):
        pass


class DataFetchingTask(Task):
    """Fetching data using YandexWeatherAPI."""

    def __init__(self, client: YandexWeatherAPI):
        self.client = client
        self.city_to_forecasting_data: dict[str, dict] = {}

    def fetch_forecasting(self, city: str) -> None:
        try:
            url = url_by_city_name(city)
            logger.debug(f'Processing url {url} for city {city}')
            self.city_to_forecasting_data[city] = self.client.get_forecasting(url)
            logger.debug(f'Forecasting data successfully fetched for city {city}')
        except (json.JSONDecodeError, HTTPError) as exc:
            logger.warning(f'Unable to fetch data for {city}: {exc}')
        except Exception as exc:
            logger.exception(exc)
            raise DataFetchingException from exc

    def run(
            self,
            cities: dict[str, str] = CITIES,
            max_workers: int = MAX_WORKERS,
            timeout: float | None = None,
    ) -> None:
        try:
            logger.info(f'Fetching forecasting started on {max_workers} workers')
            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                executor.map(self.fetch_forecasting, cities, timeout=timeout)
        except (TimeoutError, Exception) as exc:
            msg = f'Failed fetch forecasting data: {exc}'
            logger.exception(msg)
            raise DataFetchingException from exc
        logger.info('Fetching forecasting finished')


class DataCalculationTask(Task):
    """Calculating mean temperature and relevant hours count per day."""

    def __init__(self, city_to_forecasting_data: dict):
        self.city_to_forecasting_data: dict = city_to_forecasting_data
        self.queue = Manager().Queue()
        self.city_to_analyzed_days_info: dict[str, list[dict]] = {}

    @staticmethod
    def __is_available_data(day_info: dict) -> bool:
        return all(
            field is not None
            for field in (  # required fields
                day_info.get(DATE_FIELD),
                day_info.get(HOURS_START_FIELD),
                day_info.get(HOURS_END_FIELD),
                day_info.get(HOURS_COUNT_FIELD),
                day_info.get(RELEVANT_COND_HOURS_FIELD),
                day_info.get(TEMP_AVG_FIELD),
            ))

    def __dump_queue(self):
        while True:
            if self.queue.empty():
                logger.debug('Queue is empty')
                break

            city, day_info = self.queue.get(timeout=1)
            self.city_to_analyzed_days_info[city] = day_info

    def _analyze_forecast(
            self,
            queue: Queue,
            city: str,
            forecasting_data: dict,
    ):
        # DataAnalyzingException
        analyzed_data: dict = analyze_json(forecasting_data)
        days_info: list[dict] | None = analyzed_data.get(DAYS_FIELD)
        if analyzed_data and days_info is not None:
            filtered_days_info = [
                day_info
                for day_info in days_info
                if self.__is_available_data(day_info)
            ]
            queue.put((city, filtered_days_info))

    def run(
            self,
            max_workers: int = MAX_WORKERS,
            timeout: float | None = None,
    ):
        with ProcessPoolExecutor(max_workers=max_workers) as executor:
            executor.map(
                self._analyze_forecast,
                [self.queue] * len(self.city_to_forecasting_data),
                self.city_to_forecasting_data.keys(),
                self.city_to_forecasting_data.values(),
                timeout=timeout,
            )

        self.__dump_queue()


class DataAggregationTask(Task):
    """Aggregating data from multiple cities."""

    def __init__(
            self,
            city_to_analyzed_days_info: dict[str, list[dict]],
            path_to_results: Path = Path('.') / 'aggregation_results',
    ):
        logger.debug('Starting Aggregation. Generate DataFrame from input data... ')
        self.days_analyze_df: pd.DataFrame = pd.DataFrame([
            {
                CITY_FIELD: city,
                DATE_FIELD: day_info[DATE_FIELD],
                HOURS_START_FIELD: day_info[HOURS_START_FIELD],
                HOURS_END_FIELD: day_info[HOURS_END_FIELD],
                HOURS_COUNT_FIELD: day_info[HOURS_COUNT_FIELD],
                TEMP_AVG_FIELD: day_info[TEMP_AVG_FIELD],
                RELEVANT_COND_HOURS_FIELD: day_info[RELEVANT_COND_HOURS_FIELD]
            }
            for city, days_info in city_to_analyzed_days_info.items()
            for day_info in days_info
        ])

        if not path_to_results.exists():
            logger.debug(f'Directory {path_to_results} not exists. Creating...')
            try:
                path_to_results.mkdir()
            except (FileNotFoundError, OSError) as exc:
                raise DataAggregationException from exc
        self.path_to_results = path_to_results.absolute()
        logger.debug(f'Results will be saved to directory {self.path_to_results}')

    def _rank_relevant_cities(self) -> None:
        # Group by CITY_FIELD with aggregation method.
        grouped_df = self.days_analyze_df.groupby(CITY_FIELD).agg({
            TEMP_AVG_FIELD: 'mean',
            RELEVANT_COND_HOURS_FIELD: 'mean',
        }).reset_index()
        # Ranking cities (add RATING_FIELD column).
        grouped_df[RATING_FIELD] = grouped_df[[
            TEMP_AVG_FIELD,
            RELEVANT_COND_HOURS_FIELD,
        ]].apply(tuple, axis=1).rank(
            method='dense',
            ascending=False,
        ).astype(int)

        self.days_analyze_df = self.days_analyze_df.merge(
            right=grouped_df,
            on=CITY_FIELD,
            suffixes=('', MEAN_SUFFIX),
        )

    def run(
            self,
            save_format: str = 'csv',
    ) -> Path:
        self._rank_relevant_cities()
        save_format = save_format.lower()
        if save_format == 'csv':
            path = self.path_to_results / 'results.csv'
            self.days_analyze_df.to_csv(path, index=False)
            return path
        elif save_format == 'json':
            path = self.path_to_results / 'results.json'
            self.days_analyze_df.to_json(path, orient='records', index=False)
            return path
        else:
            raise DataAggregationException(
                f'Unsupported save format {save_format}'
            )


class DataAnalyzingTask:
    """Analyzing aggregated data from file."""
    SOURCE_TO_PARSER = {
        '.csv': pd.read_csv,
        '.json': pd.read_json,
    }

    def __init__(self, aggregation_path: Path):
        if not (aggregation_path.exists() and aggregation_path.is_file()):
            raise DataAnalyzingException(
                f'Path {aggregation_path} not exists or is not a file'
            )

        if aggregation_path.suffix not in self.SOURCE_TO_PARSER.keys():
            raise DataAnalyzingException(
                f'File extension {aggregation_path.suffix} is not available'
            )

        try:
            parser = self.SOURCE_TO_PARSER[aggregation_path.suffix]
            self.analysing_df: pd.DataFrame = parser(aggregation_path)
        except Exception as exc:
            raise DataAnalyzingException from exc

    def _get_top_cities(self, top_index: int = 1) -> pd.DataFrame:
        return self.analysing_df.groupby(CITY_FIELD).first()[[
            TEMP_AVG_MEAN_FIELD,
            RELEVANT_COND_HOURS_MEAN_FIELD,
            RATING_FIELD,
        ]].sort_values(by=RATING_FIELD)[:top_index]

    def run(self, top_index: int = 1) -> list[tuple[str, float, float]]:
        top_cities = self._get_top_cities(top_index)
        relevant_cities = []
        for city_name, series in top_cities.iterrows():
            logger.info(
                f'{series[RATING_FIELD]}. City {city_name}: {series[TEMP_AVG_MEAN_FIELD]} °C, '
                f'average relevant hours: {series[RELEVANT_COND_HOURS_MEAN_FIELD]}'
            )
            relevant_cities.append((
                city_name,
                series[TEMP_AVG_MEAN_FIELD],
                series[RELEVANT_COND_HOURS_MEAN_FIELD],
            ))

        return relevant_cities
