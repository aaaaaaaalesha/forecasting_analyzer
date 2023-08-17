import json
import logging
from http import HTTPStatus
from urllib.error import HTTPError
from urllib.request import urlopen

logger = logging.getLogger(__name__)


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
        return YandexWeatherAPI._do_req(url)

    @staticmethod
    def _do_req(url: str) -> dict:
        """Base request method"""
        try:
            with urlopen(url) as response:
                resp_body = response.read().decode('utf-8')
                data = json.loads(resp_body)
            if response.status == HTTPStatus.OK:
                return data

            raise Exception(f'Error during execute request. {resp_body.status}: {resp_body.reason}')
        except (json.JSONDecodeError, HTTPError) as err:
            raise err
        except Exception as ex:
            logger.error(ex)
            raise Exception(f'Unexpected error: {ex}')
