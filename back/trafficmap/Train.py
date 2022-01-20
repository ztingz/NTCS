from back.trafficmap.Time import Time
from back.trafficmap.TrainStation import TrainStation
from back.trafficmap.digraph.Edge import Edge


class Train(Edge):
    """列车类

    这个类描述交通图中的列车
    继承自Edge类
    每趟列车有5个受保护成员属性:
        航班号_flightNumber
        航班公司_company
        航班机型_mode
        出发时间_startTime
        到达时间_arriveTime

    """
    __slots__ = ('_trainNumber', '_trainType', '_startTime', '_arriveTime', '_waitingTime')

    def __init__(self, train_number: str, train_type: str, v1: TrainStation, v2: TrainStation,
                 start_time: Time, arrive_time: Time, waiting_time, **kwargs):
        super(Train, self).__init__(v1, v2, **kwargs)
        self._trainNumber = train_number
        self._trainType = train_type
        self._startTime = start_time
        self._arriveTime = arrive_time
        self._waitingTime = waiting_time

    # 保护成员的公共调用方法
    def getNumber(self):
        return self._trainNumber

    def getTrainType(self):
        return self._trainType

    def getStartTime(self):
        return self._startTime

    def getArriveTime(self):
        return self._arriveTime

    def getWaitingTime(self):
        return self._waitingTime

    # 用于测试输出
    def __str__(self):
        delimiter = ' '
        seq = ('【' + self._trainType, self._trainNumber + '】',
               str(self.getStart()), '->', str(self.getArrive()),
               self._startTime, '-', self._arriveTime, 'wait:', self.getWaitingTime(), str(self._weight))
        return delimiter.join(map(str, seq))

    # 用于判断两趟列车是否相等
    def __eq__(self, other):
        if super(Train, self).__eq__(other):
            if self.getStartTime() == other.getStartTime() and self.getArriveTime() == other.getArriveTime():
                if self.getNumber() == other.getNumber() and self.getTrainType() == other.getTrainType():
                    return self._weight == other._weight
        return False


if __name__ == "__main__":
    pass
