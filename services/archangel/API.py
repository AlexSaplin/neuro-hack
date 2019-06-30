import datetime
import requests

from common.config import api_user_id, token


class API:
    codes = {
        'stress': ['bio', 'mental', 'Stress_Avg']
    }

    @staticmethod
    def get_avg_metric(token: str, name: str, start: datetime.datetime,
                       end: datetime.datetime):
        res = requests.get(
            'https://cdb.neurop.org/api/secured/eventdata/statistics/average?Start={}&Stop={}&Group={}&Class={}&Kind={}&UserIds={}'
                .format(API.format_time(start), API.format_time(end),
                        API.codes[name][0], API.codes[name][1],
                        API.codes[name][2], api_user_id),
            headers={"accept": "application/json",
                     "Authorization": token})
        return res

    @staticmethod
    def get_even_measurements(token: str, metric_name: str,
                              start: datetime.datetime,
                              end: datetime.datetime,
                              delta: datetime.timedelta = None):
        if delta is None:
            delta = datetime.timedelta(0, 1)
        res = []

        for span_start in API._datetime_range(start, end, delta):
            res.append(API.get_avg_metric(token, metric_name,
                                          span_start, span_start + delta))
        return res

    @staticmethod
    def get_involve_estimate(token: str, start: datetime.datetime,
                             end: datetime.datetime,
                             delta: datetime.timedelta = None):
        return API.get_even_measurements(token, 'stress', start, end, delta)

    @staticmethod
    def format_time(time: datetime.datetime):
        return time.strftime('%d-%m-%Y%20%H%3A%M')

    @staticmethod
    def _datetime_range(start: datetime.datetime, end: datetime.datetime,
                        delta: datetime.timedelta):
        while start < end:
            yield start
            start += delta


print((
    'https://cdb.neurop.org/api/secured/eventdata/statistics/average?Start={}&Stop={}&Group={}&Class={}&Kind={}&UserIds={}'
        .format("01-10-200120%10%3A10", '01-10-202120%10%3A10',
                API.codes['stress'][0], API.codes['stress'][1],
                API.codes['stress'][2], api_user_id),
    {"accept": "application/json",
             "Authorization": token})
)
