import math
import time
from datetime import timedelta, datetime

from back.configure import ENLIGHTENING_VALUE
from back.trafficmap.Time import Time
from back.trafficmap.TrafficMap import TrafficMap, TRAFFIC_MAP
from back.trafficmap.configure import get_from_ll_dict
from back.trafficmap.digraph import Vertex


class AStar(object):
    """A*算法类类

        这个类实现了交通图中最短路径的搜索
        每个A*对象有12个受保护成员属性:
            要搜索的图_map
            始点_start
            终点_end
            出发时间_departureTime
            出行策略_strategy

            用来存放所有已经生成但是还是没有被扩展的节点_open
            用来存放所有已经扩展的节点_close
            {此节点名:父节点}字典_cameFrom
            {此节点名:父节点到此节点的边}_byways
            {此节点名:到此节点的时间}_arrivalTime
            当前时间_nowTime
            {此节点名:到达该点的所用付出的代价}_gScore
            {此节点名:到达终点预计要付出的代价}_fScore

        """
    __slots__ = ('_map', '_start', '_end', '_departureTime', '_nowTime', '_strategy',
                 '_open', '_close', '_cameFrom', '_howBy', '_arrivalTime',
                 '_gScore', '_fScore')

    def __init__(self, g: TrafficMap, start_name: str, end_name: str, departure_time, strategy: str):
        self._map = g
        self._start = g.findVertex(start_name)

        if self._start is None:
            raise Exception("不存在的点", start_name)
        self._end = g.findVertex(end_name)
        if self._end is None:
            raise Exception("不存在的点", end_name)

        self._departureTime = Time(strTime=departure_time)
        self._nowTime = self._departureTime
        self._strategy = strategy

        self._open = [self._start]
        self._close = []
        self._cameFrom = {}
        self._howBy = {}
        self._arrivalTime = {start_name: self._departureTime}
        self._gScore = {start_name: 0}
        self._fScore = {start_name: self.calcH(self._start.getName())}

    # 计算相邻两点之间的最短路径和代价
    def distBetween(self, start: Vertex, end: Vertex):
        if start == end:
            return None, 0
        if start and end and end in start.adjacentVerticesIter():
            way, weight = start.bestByTo(end, self._nowTime, self._strategy)
            if way:
                return way, weight
        return None, float('inf')

    # 计算此节点到终点预计需要付出的代价
    def calcH(self, v_name):
        if v_name == self._end.getName():
            return 0
        v_ll = get_from_ll_dict(v_name)
        end_ll = get_from_ll_dict(self._end.getName())
        if v_ll and end_ll:
            result = math.sqrt(math.pow(v_ll[0] - end_ll[0], 2) + math.pow(v_ll[1] - end_ll[1], 2))
            return result * ENLIGHTENING_VALUE
        return float('inf')

    # 将一个节点和他的父节点连接、初始化代价字典并加入_open列表
    def addInOpen(self, father: Vertex, current: Vertex):
        self._cameFrom[current.getName()] = father
        self._howBy[current.getName()], self._gScore[current.getName()] = self.distBetween(father, current)
        if self._howBy[current.getName()]:
            self._gScore[current.getName()] += self._gScore[father.getName()]
            if type(self._howBy[current.getName()].getArriveTime()) == datetime:
                print()
            self._arrivalTime[current.getName()] = self._howBy[current.getName()].getArriveTime()
        else:
            raise Exception(current, "'s father not", father)
        self._fScore[current.getName()] = self.calcH(current.getName()) + self._gScore[current.getName()]
        self._open.append(current)

    # 将一个节点从_open列表中移出，并相应的删除字典中对应的键值对并将其加入_close列表
    def fromOpenToClose(self, vertex: Vertex):
        if vertex in self._open:
            self._open.pop(self._open.index(vertex))
            self._fScore.pop(vertex.getName())
            self._close.append(vertex)
            return True
        raise Exception('无法移除不存在的节点', vertex)

    # 执行A*算法搜寻最短路径
    def runSearch(self):
        while self._open:
            current_name = min(self._fScore, key=self._fScore.get)
            current = self._map.findVertex(current_name)
            if current == self._end:
                return self.reconstructPath(current)
            self.fromOpenToClose(current)
            self._nowTime = self._arrivalTime.get(current_name)
            for neighbor in current.adjacentVerticesIter():
                if neighbor in self._close:
                    continue
                if neighbor not in self._open:
                    self.addInOpen(current, neighbor)
                    continue
                way, gscore = self.distBetween(current, neighbor)
                # 试探代价
                tentative_gScore = self._gScore.get(current_name) + gscore
                # 判断试探代价是否比已知代价划算
                if tentative_gScore < self._gScore.get(neighbor.getName()):
                    self._cameFrom[neighbor.getName()] = current
                    self._howBy[neighbor.getName()] = way
                    self._arrivalTime[neighbor.getName()] = way.getArriveTime()
                    self._gScore[neighbor.getName()] = tentative_gScore
                    self._fScore[neighbor.getName()] = tentative_gScore + self.calcH(neighbor.getName())
        return False

    # 根据尾节点回溯路径
    def reconstructPath(self, end_vertex):
        total_path = []
        while end_vertex.getName() in self._cameFrom:
            way = self._howBy[end_vertex.getName()]
            end_vertex = self._cameFrom[end_vertex.getName()]
            total_path.append(way)
        total_path.reverse()
        return total_path

    # 确定权值
    def checkWeight(self, paths):
        total_money = 0
        total_time = paths[-1].getArriveTime() - paths[0].getStartTime()
        for i in range(len(paths)):
            total_money += paths[i].getWeight('money')
            # 某段跨0点
            if paths[i].getArriveTime().getDatetime().day > paths[i].getStartTime().getDatetime().day:
                total_time += 86400
            try:
                # 某两段之间因等待跨0点
                if paths[i].getArriveTime().getDatetime().time() > paths[i + 1].getStartTime().getDatetime().time():
                    total_time += 86400
            except Exception as e:
                continue
        return timedelta(seconds=total_time), round(total_money, 2)

    # 格式化路径列表获得方案
    def formatPath(self, paths):
        programme = []
        index = 0
        i = 0
        while i < len(paths):
            count = 1
            sum_time = 0
            sum_money = 0
            programme.append([])

            number = paths[i].getNumber()
            programme[index].append(number)
            programme[index].append(str(paths[i].getStartTime()))
            programme[index].append(str(paths[i].getStart()))
            programme[index].append('-->')
            sum_time += paths[i].getWeight('time')
            sum_money += paths[i].getWeight('money')
            while i + 1 < len(paths) and paths[i + 1].getNumber() == number:
                i += 1
                sum_time += paths[i].getWeight('time')
                sum_money += paths[i].getWeight('money')
                count += 1
            programme[index].append(str(paths[i].getArrive()))
            programme[index].append(str(paths[i].getArriveTime()))
            programme[index].append(str(count) + '站')
            programme[index].append(sum_money)
            index += 1
            i += 1
        return programme

    # 返回处理过的结果元组
    def getResult(self):
        paths = self.runSearch()

        total_time, total_money = self.checkWeight(paths)
        statistical = {'start_time': paths[0].getStartTime(),
                       'arrive_time': paths[-1].getArriveTime(),
                       'total_time': total_time, 'total_money': total_money}

        programme = self.formatPath(paths)
        return programme, statistical


if __name__ == "__main__":
    _from = '福州'
    _to = '长沙'
    _departureTime = '8:0'
    begin = time.time()
    a = AStar(TRAFFIC_MAP, _from, _to, _departureTime, 'money')
    for edge in a.getResult():
        print(str(edge))
    end = time.time()
    print('run Main time:', end - begin)
