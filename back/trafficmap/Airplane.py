from back.trafficmap.Airport import Airport
from back.trafficmap.Time import Time
from back.trafficmap.digraph.Edge import Edge


class Airplane(Edge):
    """航班类

    这个类描述交通图中的航班
    继承自Edge类
    每趟航班有5个受保护成员属性:
        航班号_flightNumber
        航班公司_company
        航班机型_mode
        出发时间_startTime
        到达时间_arriveTime

    """
    __slots__ = ('_flightNumber', '_company', '_mode', '_startTime', '_arriveTime')

    def __init__(self, flight_number: str, company: str, mode: str,
                 v1: Airport, v2: Airport, start_time: Time, arrive_time: Time, **kwargs):
        super(Airplane, self).__init__(v1, v2, **kwargs)
        self._flightNumber = flight_number
        self._company = company
        self._mode = mode
        self._startTime = start_time
        self._arriveTime = arrive_time

    # 保护成员的公共调用方法
    def getNumber(self):
        return self._flightNumber

    def getCompany(self):
        return self._company

    def getMode(self):
        return self._mode

    def getStartTime(self):
        return self._startTime

    def getArriveTime(self):
        return self._arriveTime

    # 用于测试输出
    def __str__(self):
        delimiter = ' '
        seq = ('【' + self._mode, self._flightNumber + '】',
               str(self.getStart()), '->', str(self.getArrive()),
               self._startTime, '-', self._arriveTime, self._company, str(self._weight))
        return delimiter.join(map(str, seq))

    # 用于判断两趟航班是否相等
    def __eq__(self, other):
        if super(Airplane, self).__eq__(other):
            if self.getStartTime() == other.getStartTime() and self.getArriveTime() == other.getArriveTime():
                if self.getNumber() == other.getNumber() and self.getMode() == other.getMode() and self.getCompany() == other.getCompany():
                    return self._weight == other._weight
        return False


if __name__ == "__main__":
    pass
