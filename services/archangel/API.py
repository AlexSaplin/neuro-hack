import datetime
import requests
import json

from utils.linear_interpolate import interpolate_events
from common.config import config


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
                        API.codes[name][2], config.API_USER_ID),
            headers={"accept": "application/json",
                     "Authorization": token,
                     "State": '1'}).text

        print(res)
        if json.loads(res)['c'] == 0:
            return None
        else:
            return json.loads(res)['v']

    @staticmethod
    def get_even_measurements(token: str, metric_name: str,
                              start: datetime.datetime,
                              end: datetime.datetime,
                              delta: datetime.timedelta = None):
        if delta is None:
            delta = datetime.timedelta(0, 1)
        res = []

        t = 0
        for i, span_start in enumerate(API._datetime_range(start, end, delta)):
            t += 1
            try:
                avg = API.get_avg_metric(token, metric_name,
                                     span_start, span_start + delta)
            except Exception as e:
                avg = None
            if avg is not None:
                res.append((i, avg))

        return interpolate_events(res, t)

    @staticmethod
    def get_involve_estimate(token: str, start: datetime.datetime,
                             end: datetime.datetime,
                             delta: datetime.timedelta = None):
        return API.get_even_measurements(token, 'stress', start, end, delta)

    @staticmethod
    def format_time(time: datetime.datetime):
        return time.isoformat()

    @staticmethod
    def _datetime_range(start: datetime.datetime, end: datetime.datetime,
                        delta: datetime.timedelta):
        while start < end:
            yield start
            start += delta
