from numba import jit


class Vertex(object):
    """点类

    这个类描述图中的节点
    每条边有2个受保护成员属性:
        名字_name
        邻接边表_edgeList
    1个公有成员属性:
        其他信息字典otherInfoDict

    """
    __slots__ = ('_name', '_edgeList', 'otherInfoDict')

    def __init__(self, name: str, **kwargs):
        self._name = name
        self._edgeList = list()
        self.otherInfoDict = kwargs

    # 节点名字属性_name的方法
    def getName(self):
        return self._name

    def setName(self, name: str):
        self._name = name

    # 节点邻接边表属性_edgeLists的方法
    def addEdge(self, edge):
        self._edgeList.append(edge)

    def delEdge(self, edge):
        if edge in self._edgeList:
            self._edgeList.remove(edge)
            return True
        return False

    def sizeofEdges(self):
        return len(self._edgeList)

    def getEdgeList(self):
        return self._edgeList

    def edgesIter(self):
        return iter(self._edgeList)

    # 获得到达一个另一节点的边表
    def toSomewhere(self, target):
        can_take_list = []
        for edge in self.edgesIter():
            if edge.getArrive() == target:
                can_take_list.append(edge)
        return can_take_list

    # 获得此节点的可达节点的迭代器
    def adjacentVerticesIter(self):
        vertices = list()
        for edge in self.edgesIter():
            if edge.getAnotherVertex(self) not in vertices:
                vertices.append(edge.getAnotherVertex(self))
        return iter(vertices)

    def __str__(self):
        return str('[' + self._name + ']')

    def __eq__(self, other):
        if self is other: return True
        if type(self) != type(other): return False
        return self.getName() == other.getName()


if __name__ == "__main__":
    v1 = Vertex('北京西')
    print(v1)
