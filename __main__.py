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

if __name__ == '__main__':
    try:
        # DataFetchingTask.
        data_fetcher = DataFetchingTask(client=YandexWeatherAPI())
        data_fetcher.run()

        # DataCalculationTask.
        data_calculator = DataCalculationTask(
            data_fetcher.city_to_forecasting_data
        )
        data_calculator.run()

        # DataAggregationTask.
        data_aggregator = DataAggregationTask(
            data_calculator.city_to_analyzed_days_info
        )
        aggregation_results_path = data_aggregator.run()

        # DataAnalyzingTask.
        data_analysis = DataAnalyzingTask(aggregation_results_path)
        resulted_cities = data_analysis.run(top_index=3)

        for rating, resulted_city in enumerate(resulted_cities):
            for city_name, temperature, relevant_days in resulted_city:
                print(f'{rating}. {city_name} - {temperature}°C - {relevant_days} days')
    except (
            DataFetchingException,
            DataAggregationException,
            DataAnalyzingException,
    ) as exc:
        print(exc)
        exit(1)
