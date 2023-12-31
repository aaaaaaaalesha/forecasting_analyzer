import pytest


@pytest.fixture
def city_to_analyzed_days_info():
    return {
        'SPETERSBURG': [{'date': '2022-05-26', 'hours_start': 9, 'hours_end': 19, 'hours_count': 11, 'temp_avg': 12.182,
                         'relevant_cond_hours': 3},
                        {'date': '2022-05-27', 'hours_start': 9, 'hours_end': 19, 'hours_count': 11, 'temp_avg': 11.818,
                         'relevant_cond_hours': 0},
                        {'date': '2022-05-28', 'hours_start': 9, 'hours_end': 19, 'hours_count': 11, 'temp_avg': 11.636,
                         'relevant_cond_hours': 0},
                        {'date': '2022-05-29', 'hours_start': 9, 'hours_end': 9, 'hours_count': 1, 'temp_avg': 12.0,
                         'relevant_cond_hours': 1}],
        'ABUDHABI': [
            {'date': '2022-05-26', 'hours_start': 9, 'hours_end': 19, 'hours_count': 11, 'temp_avg': 34.818,
             'relevant_cond_hours': 11},
            {'date': '2022-05-27', 'hours_start': 9, 'hours_end': 19, 'hours_count': 11, 'temp_avg': 34.455,
             'relevant_cond_hours': 11},
            {'date': '2022-05-28', 'hours_start': 9, 'hours_end': 19, 'hours_count': 11, 'temp_avg': 33.818,
             'relevant_cond_hours': 11},
            {'date': '2022-05-29', 'hours_start': 9, 'hours_end': 10, 'hours_count': 2, 'temp_avg': 34.0,
             'relevant_cond_hours': 2}], 'CAIRO': [
            {'date': '2022-05-26', 'hours_start': 9, 'hours_end': 19, 'hours_count': 11, 'temp_avg': 32.545,
             'relevant_cond_hours': 11},
            {'date': '2022-05-27', 'hours_start': 9, 'hours_end': 19, 'hours_count': 11, 'temp_avg': 33.182,
             'relevant_cond_hours': 11},
            {'date': '2022-05-28', 'hours_start': 9, 'hours_end': 19, 'hours_count': 11, 'temp_avg': 34.455,
             'relevant_cond_hours': 11}],
        'WARSZAWA': [
            {'date': '2022-05-26', 'hours_start': 9, 'hours_end': 19, 'hours_count': 11, 'temp_avg': 19.636,
             'relevant_cond_hours': 11},
            {'date': '2022-05-27', 'hours_start': 9, 'hours_end': 19, 'hours_count': 11, 'temp_avg': 14.0,
             'relevant_cond_hours': 3},
            {'date': '2022-05-28', 'hours_start': 9, 'hours_end': 19, 'hours_count': 11, 'temp_avg': 12.818,
             'relevant_cond_hours': 0}], 'ROMA': [
            {'date': '2022-05-26', 'hours_start': 9, 'hours_end': 19, 'hours_count': 11, 'temp_avg': 29.0,
             'relevant_cond_hours': 11},
            {'date': '2022-05-27', 'hours_start': 9, 'hours_end': 19, 'hours_count': 11, 'temp_avg': 29.273,
             'relevant_cond_hours': 11},
            {'date': '2022-05-28', 'hours_start': 9, 'hours_end': 19, 'hours_count': 11, 'temp_avg': 25.545,
             'relevant_cond_hours': 11}],
        'BUCHAREST': [
            {'date': '2022-05-26', 'hours_start': 9, 'hours_end': 19, 'hours_count': 11, 'temp_avg': 27.455,
             'relevant_cond_hours': 11},
            {'date': '2022-05-27', 'hours_start': 9, 'hours_end': 19, 'hours_count': 11, 'temp_avg': 26.091,
             'relevant_cond_hours': 11},
            {'date': '2022-05-28', 'hours_start': 9, 'hours_end': 19, 'hours_count': 11, 'temp_avg': 27.818,
             'relevant_cond_hours': 11},
            {'date': '2022-05-29', 'hours_start': 9, 'hours_end': 9, 'hours_count': 1, 'temp_avg': 18.0,
             'relevant_cond_hours': 1}],
        'KALININGRAD': [
            {'date': '2022-05-26', 'hours_start': 9, 'hours_end': 19, 'hours_count': 11, 'temp_avg': 15.364,
             'relevant_cond_hours': 9},
            {'date': '2022-05-27', 'hours_start': 9, 'hours_end': 19, 'hours_count': 11, 'temp_avg': 12.818,
             'relevant_cond_hours': 2},
            {'date': '2022-05-28', 'hours_start': 9, 'hours_end': 19, 'hours_count': 11, 'temp_avg': 11.636,
             'relevant_cond_hours': 1}],
        'MOSCOW': [
            {'date': '2022-05-26', 'hours_start': 9, 'hours_end': 19, 'hours_count': 11, 'temp_avg': 17.727,
             'relevant_cond_hours': 7},
            {'date': '2022-05-27', 'hours_start': 9, 'hours_end': 19, 'hours_count': 11, 'temp_avg': 13.091,
             'relevant_cond_hours': 0},
            {'date': '2022-05-28', 'hours_start': 9, 'hours_end': 19, 'hours_count': 11, 'temp_avg': 12.182,
             'relevant_cond_hours': 0},
            {'date': '2022-05-29', 'hours_start': 9, 'hours_end': 9, 'hours_count': 1, 'temp_avg': 12.0,
             'relevant_cond_hours': 1}],
        'LONDON': [
            {'date': '2022-05-26', 'hours_start': 9, 'hours_end': 19, 'hours_count': 11, 'temp_avg': 17.364,
             'relevant_cond_hours': 11},
            {'date': '2022-05-27', 'hours_start': 9, 'hours_end': 19, 'hours_count': 11, 'temp_avg': 16.273,
             'relevant_cond_hours': 11},
            {'date': '2022-05-28', 'hours_start': 9, 'hours_end': 19, 'hours_count': 11, 'temp_avg': 14.636,
             'relevant_cond_hours': 11}],
        'NOVOSIBIRSK': [
            {'date': '2022-05-26', 'hours_start': 9, 'hours_end': 19, 'hours_count': 11, 'temp_avg': 24.909,
             'relevant_cond_hours': 11},
            {'date': '2022-05-27', 'hours_start': 9, 'hours_end': 19, 'hours_count': 11, 'temp_avg': 22.455,
             'relevant_cond_hours': 11},
            {'date': '2022-05-28', 'hours_start': 9, 'hours_end': 19, 'hours_count': 11, 'temp_avg': 23.273,
             'relevant_cond_hours': 11},
            {'date': '2022-05-29', 'hours_start': 9, 'hours_end': 13, 'hours_count': 5, 'temp_avg': 22.2,
             'relevant_cond_hours': 5}], 'PARIS': [
            {'date': '2022-05-26', 'hours_start': 9, 'hours_end': 19, 'hours_count': 11, 'temp_avg': 17.636,
             'relevant_cond_hours': 9},
            {'date': '2022-05-27', 'hours_start': 9, 'hours_end': 19, 'hours_count': 11, 'temp_avg': 17.364,
             'relevant_cond_hours': 11},
            {'date': '2022-05-28', 'hours_start': 9, 'hours_end': 19, 'hours_count': 11, 'temp_avg': 17.0,
             'relevant_cond_hours': 11}],
        'VOLGOGRAD': [
            {'date': '2022-05-26', 'hours_start': 9, 'hours_end': 19, 'hours_count': 11, 'temp_avg': 22.091,
             'relevant_cond_hours': 11},
            {'date': '2022-05-27', 'hours_start': 9, 'hours_end': 19, 'hours_count': 11, 'temp_avg': 21.909,
             'relevant_cond_hours': 11},
            {'date': '2022-05-28', 'hours_start': 9, 'hours_end': 19, 'hours_count': 11, 'temp_avg': 25.636,
             'relevant_cond_hours': 11},
            {'date': '2022-05-29', 'hours_start': 9, 'hours_end': 9, 'hours_count': 1, 'temp_avg': 25.0,
             'relevant_cond_hours': 1}],
        'BEIJING': [
            {'date': '2022-05-26', 'hours_start': 9, 'hours_end': 19, 'hours_count': 11, 'temp_avg': 31.818,
             'relevant_cond_hours': 11},
            {'date': '2022-05-27', 'hours_start': 9, 'hours_end': 19, 'hours_count': 11, 'temp_avg': 32.727,
             'relevant_cond_hours': 11},
            {'date': '2022-05-28', 'hours_start': 9, 'hours_end': 19, 'hours_count': 11, 'temp_avg': 33.818,
             'relevant_cond_hours': 11},
            {'date': '2022-05-29', 'hours_start': 9, 'hours_end': 14, 'hours_count': 6, 'temp_avg': 28.167,
             'relevant_cond_hours': 6}],
        'BERLIN': [
            {'date': '2022-05-26', 'hours_start': 9, 'hours_end': 19, 'hours_count': 11, 'temp_avg': 19.273,
             'relevant_cond_hours': 9},
            {'date': '2022-05-27', 'hours_start': 9, 'hours_end': 19, 'hours_count': 11, 'temp_avg': 16.0,
             'relevant_cond_hours': 6},
            {'date': '2022-05-28', 'hours_start': 9, 'hours_end': 19, 'hours_count': 11, 'temp_avg': 13.636,
             'relevant_cond_hours': 0}],
        'KAZAN': [
            {'date': '2022-05-26', 'hours_start': 9, 'hours_end': 19, 'hours_count': 11, 'temp_avg': 12.545,
             'relevant_cond_hours': 6},
            {'date': '2022-05-27', 'hours_start': 9, 'hours_end': 19, 'hours_count': 11, 'temp_avg': 13.727,
             'relevant_cond_hours': 0},
            {'date': '2022-05-28', 'hours_start': 9, 'hours_end': 19, 'hours_count': 11, 'temp_avg': 14.727,
             'relevant_cond_hours': 3},
            {'date': '2022-05-29', 'hours_start': 9, 'hours_end': 9, 'hours_count': 1, 'temp_avg': 14.0,
             'relevant_cond_hours': 1}]
    }
