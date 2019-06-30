import datetime


class API:
    codes = {
        'stress': ['bio', 'mental', 'Stress_Avg']
    }

    @staticmethod
    def get_avg_metric(token: str, name: str, start: datetime.datetime, end: datetime.datetime):
        pass

    @staticmethod
    def get_even_measurements(token: str, metric_name: str, start: datetime.datetime,
                              end: datetime.datetime, delta: datetime.timedelta = None):
        if delta is None:
            delta = datetime.timedelta(0, 1)
        res = []

        for span_start in API._datetime_range(start, end, delta):
            res.append(API.get_avg_metric(token, metric_name,
                                           span_start, span_start + delta))
        return res

    @staticmethod
    def get_involve_estimate(token: str, start: datetime.datetime, end: datetime.datetime,
                             delta: datetime.timedelta = None):
        return API.get_even_measurements(token, 'stress', start, end, delta)

    @staticmethod
    def format_time(time: datetime.datetime):
        return time.strftime('%d-%m-%Y %H:%M')

    @staticmethod
    def _datetime_range(start: datetime.datetime, end: datetime.datetime,
                        delta: datetime.timedelta):
        while start < end:
            yield start
            start += delta
