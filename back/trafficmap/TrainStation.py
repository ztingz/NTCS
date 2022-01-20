from back.trafficmap.Time import Time
from back.trafficmap.digraph.Vertex import Vertex


class TrainStation(Vertex):
    """列车站类

    这个类描述交通图中的列车站
    继承自Vertex类

    """
    __slots__ = ()

    def __init__(self, name: str, **kwargs):
        super(TrainStation, self).__init__(name, **kwargs)

    # 获得到达一个另一个车站的最优列车
    def bestByTo(self, target: Vertex, departure_time: Time, strategy: str):
        ways = self.toSomewhere(target)
        if ways:
            weights = []
            for way in ways:
                if strategy == 'time':
                    if departure_time <= way.getStartTime():
                        wait_time = way.getStartTime() - departure_time
                    else:
                        wait_time = way.getStartTime().nextDay() - departure_time
                    weights.append(wait_time + way.getWeight(strategy) + way.getWaitingTime())
                else:
                    weights.append(way.getWeight(strategy))
            return ways[weights.index(min(weights))], min(weights)
        return None, None


if __name__ == "__main__":
    a = TrainStation('北京')
    b = TrainStation('北京')
    print(a == b)
    print(a)
    for item in a.edgesIter():
        print(item)
        print(type(item))
