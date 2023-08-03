import json
import logging

from http import HTTPStatus
from urllib.request import urlopen

logger = logging.getLogger()


class YandexWeatherAPI:
    """
    Base class for requests
    """

    @staticmethod
    def get_forecasting(url: str):
        """
        :param url: url_to_json_data as str
        :return: response data as json
        """
        return YandexWeatherAPI.__do_req(url)

    @staticmethod
    def __do_req(url: str) -> str:
        """Base request method"""
        try:
            with urlopen(url) as response:
                resp_body = response.read().decode('utf-8')
                data = json.loads(resp_body)
            if response.status != HTTPStatus.OK:
                return data

            raise Exception(f'Error during execute request. {resp_body.status}: {resp_body.reason}')
        except Exception as ex:
            logger.error(ex)
            raise Exception(f'Unexpected error: {ex}')
