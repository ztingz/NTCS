import csv
import os

from back.trafficmap.Time import Time
from back.trafficmap.digraph.Vertex import Vertex

# 获得此文件的访问路径，防止找不到文件路径
current_path = os.path.dirname(__file__)


# 获得机场的城市信息字典
def getAirportCityDict(filename):
    city_dict = {}
    with open(current_path + "/CSV/" + filename, "r", encoding="utf-8-sig") as f:
        reader = csv.reader(f)
        fieldnames = next(reader)  # 获取数据的第一列，作为后续要转为字典的键名 生成器，next方法获取
        csv_reader = csv.DictReader(f, fieldnames=fieldnames)  # list of keys for the dict 以list的形式存放键名
        for row in csv_reader:
            row.pop('')
            row.pop('Address_en')
            city_dict[row['Abbreviation']] = row['Address_cn']
    return city_dict


# 实例化机场城市字典对象，方便搜索
cityDict = getAirportCityDict('Airport.csv')


class Airport(Vertex):
    """机场类

    这个类描述交通图中的机场
    继承自Vertex类
    每个机场有1个受保护属性:
        机场缩写_abbreviation

    """
    __slots__ = '_abbreviation'

    def __init__(self, name: str, abbreviation: str, **kwargs):
        super(Airport, self).__init__(name, **kwargs)
        self._abbreviation = abbreviation

    # 保护成员的公共调用方法
    def getAbbreviation(self):
        return self._abbreviation

    # 获得此机场所处的城市名字
    def getCityName(self):
        if self._abbreviation in cityDict:
            return cityDict[self.getAbbreviation()]
        return None

    # 获得到达一个另一个车站的最优航班
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
                    weights.append(wait_time + way.getWeight(strategy))
                else:
                    weights.append(way.getWeight(strategy))
            return ways[weights.index(min(weights))], min(weights)
        return None, None


if __name__ == "__main__":
    a = Airport('首都国际机场', 'BJS')
    print(a.getCityName())
