import logging

from multiprocessing import set_start_method

from external.client import YandexWeatherAPI
from exceptions import (
    DataFetchingException,
    DataAggregationException,
    DataAnalyzingException,
)
from tasks import (
    DataFetchingTask,
    DataCalculationTask,
    DataAggregationTask,
    DataAnalyzingTask,
)

TIMEOUT = 5.

logging.basicConfig(format='%(asctime)s [%(levelname)s] %(message)s')

if __name__ == '__main__':
    set_start_method('spawn')
    try:
        # DataFetchingTask.
        data_fetcher = DataFetchingTask(client=YandexWeatherAPI())
        data_fetcher.run(timeout=TIMEOUT)

        # DataCalculationTask.
        data_calculator = DataCalculationTask(
            data_fetcher.city_to_forecasting_data
        )
        data_calculator.run(timeout=TIMEOUT)

        # DataAggregationTask.
        data_aggregator = DataAggregationTask(
            data_calculator.city_to_analyzed_days_info
        )
        aggregation_results_path = data_aggregator.run(
            save_format='csv',
        )

        # DataAnalyzingTask.
        top_index = 3
        data_analysis = DataAnalyzingTask(aggregation_results_path)
        relevant_cities = data_analysis.run(top_index=top_index)
        print(f'{top_index} most relevant cities:')
        for rating, (
                city_name,
                temperature,
                relevant_days,
        ) in enumerate(relevant_cities):
            print(
                f'{rating + 1}. {city_name} - {temperature} °C '
                f'- {round(relevant_days)} days'
            )
    except (
            DataFetchingException,
            DataAggregationException,
            DataAnalyzingException,
    ) as exc:
        print(exc)
        exit(1)
    except Exception as exc:
        print(f'Uncaught exception: {exc}')
        exit(1)
