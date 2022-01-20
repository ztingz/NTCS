import time
from datetime import datetime, timedelta


class Time(object):
    """时间类

        这个类描述交通图中的时间信息
        每条边有1个受保护成员属性:
            日期时间_datetime

        """

    def __init__(self, strDate='2018-1-1', strTime=...):
        self._datetime = datetime.strptime(strDate + ' ' + strTime, format('%Y-%m-%d %H:%M'))

    def getDatetime(self):
        return self._datetime

    def getTimeClock(self):
        return time.mktime(self._datetime.timetuple())

    def setTime(self, new_datatime):
        self._datetime = new_datatime

    def nextDay(self):
        new_time = self._datetime + timedelta(days=1)
        return new_time

    def __sub__(self, other):
        return time.mktime(self._datetime.timetuple()) - time.mktime(other._datetime.timetuple())

    def __rsub__(self, other):
        if type(other) is datetime:
            return time.mktime(other.timetuple()) - time.mktime(self._datetime.timetuple())

    def __gt__(self, other):
        return self._datetime > other._datetime

    def __lt__(self, other):
        if type(other) is Time:
            return self._datetime < other._datetime
        if type(other) is datetime:
            return self._datetime < other
        if type(other) is float:
            return time.mktime(self._datetime.timetuple()) < other

    def __ge__(self, other):
        return self._datetime >= other._datetime

    def __le__(self, other):
        return self._datetime <= other._datetime

    def __eq__(self, other):
        return self._datetime == other._datetime

    def __str__(self):
        return str(self._datetime.time())


if __name__ == "__main__":
    departure_time = datetime(2018, 10, 30, 8, 32)
    b = datetime(2018, 10, 3, 8, 3)
    print(departure_time.day > b.day)
    print(timedelta(seconds=86200))
    print(type(timedelta(seconds=86200)))
    # if departure_time < b:
    #     wait = b - departure_time
    #     print(wait)
    # else:
    #     wait = b + timedelta(days=1) - departure_time
    #     print(wait)
    pass
