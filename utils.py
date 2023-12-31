CITIES = {
    'MOSCOW': 'https://code.s3.yandex.net/async-module/moscow-response.json',
    'PARIS': 'https://code.s3.yandex.net/async-module/paris-response.json',
    'LONDON': 'https://code.s3.yandex.net/async-module/london-response.json',
    'BERLIN': 'https://code.s3.yandex.net/async-module/berlin-response.json',
    'BEIJING': 'https://code.s3.yandex.net/async-module/beijing-response.json',
    'KAZAN': 'https://code.s3.yandex.net/async-module/kazan-response.json',
    'SPETERSBURG': 'https://code.s3.yandex.net/async-module/spetersburg-response.json',
    'VOLGOGRAD': 'https://code.s3.yandex.net/async-module/volgograd-response.json',
    'NOVOSIBIRSK': 'https://code.s3.yandex.net/async-module/novosibirsk-response.json',
    'KALININGRAD': 'https://code.s3.yandex.net/async-module/kaliningrad-response.json',
    'ABUDHABI': 'https://code.s3.yandex.net/async-module/abudhabi-response.json',
    'WARSZAWA': 'https://code.s3.yandex.net/async-module/warszawa-response.json',
    'BUCHAREST': 'https://code.s3.yandex.net/async-module/bucharest-response.json',
    'ROMA': 'https://code.s3.yandex.net/async-module/roma-response.json',
    'CAIRO': 'https://code.s3.yandex.net/async-module/cairo-response.json',
    'GIZA': 'https://code.s3.yandex.net/async-module/giza-response.json',
    'MADRID': 'https://code.s3.yandex.net/async-module/madrid-response.json',
    'TORONTO': 'https://code.s3.yandex.net/async-module/toronto-response.json'
}

MIN_MAJOR_PYTHON_VER = 3
MIN_MINOR_PYTHON_VER = 9

CITY_FIELD = 'city'
DAYS_FIELD = 'days'
DATE_FIELD = 'date'
HOURS_START_FIELD = 'hours_start'
HOURS_END_FIELD = 'hours_end'
HOURS_COUNT_FIELD = 'hours_count'
RELEVANT_COND_HOURS_FIELD = 'relevant_cond_hours'
TEMP_AVG_FIELD = 'temp_avg'
RATING_FIELD = 'rating'
MEAN_SUFFIX = '_mean'
TEMP_AVG_MEAN_FIELD = f'temp_avg{MEAN_SUFFIX}'
RELEVANT_COND_HOURS_MEAN_FIELD = f'relevant_cond_hours{MEAN_SUFFIX}'


def check_python_version():
    import sys

    if (
            sys.version_info.major < MIN_MAJOR_PYTHON_VER
            or sys.version_info.minor < MIN_MINOR_PYTHON_VER
    ):
        raise Exception(
            f'Please use python version >= {MIN_MAJOR_PYTHON_VER}.{MIN_MINOR_PYTHON_VER}'
        )


def url_by_city_name(city_name: str) -> str:
    try:
        return CITIES[city_name]
    except KeyError:
        raise Exception(f'Please check that city {city_name} exists')
