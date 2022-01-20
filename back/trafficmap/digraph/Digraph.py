from back.trafficmap.digraph.AbstractCollection import AbstractCollection
from back.trafficmap.digraph.Edge import Edge
from back.trafficmap.digraph.Vertex import Vertex
from numba import jit


class Digraph(AbstractCollection):
    """图类

    这个类描述图
    继承自AbstractCollection类
    每个图有2个受保护成员属性:
        拥有边数_edgeCount
        点集_verticesDict

    """
    __slots__ = ('_verticesDict', '_edgeCount')

    def __init__(self, sourceCollection=None):
        self._verticesDict = {}
        self._edgeCount = 0
        super(Digraph, self).__init__(sourceCollection)

    # 实现父类AbstractCollection的抽象方法
    def add(self, vertex: Vertex):
        self.addVertex(vertex)

    # 关于图中边和点size的方法
    def sizeofEdges(self):
        return self._edgeCount

    # 图关于图中点和点集_vertices相关的方法
    def addVertex(self, vertex: Vertex):
        if self.findVertex(vertex.getName()):
            return False
        self._verticesDict[vertex.getName()] = vertex
        self._size += 1
        return True

    def delVertex(self, v_name):
        if v_name in self._verticesDict:
            for edge in self.edgesIter():
                if edge.getArrive() == self.findVertex(v_name):
                    edge.getStart().delEdge(edge)
                    self._edgeCount -= 1
                if edge.getStart() == self.findVertex(v_name):
                    self.findVertex(v_name).delEdge(edge)
                    self._edgeCount -= 1
            self._verticesDict.pop(v_name, None)
            self._size -= 1
            return True
        return False

    def findVertex(self, v_name: str):
        try:
            return self._verticesDict[v_name]
        except KeyError:
            return None

    def verticesIter(self):
        return iter(self._verticesDict.values())

    # 图关于图中边和边数_edgeCount相关的方法
    def addEdge(self, edge: Edge):
        if self.containsEdge(edge):
            return False
        vertex = self.findVertex(edge.getStart().getName())
        if vertex:
            self.findVertex(edge.getStart().getName()).addEdge(edge)
            self._edgeCount += 1
            return True
        return False

    def delEdge(self, v1_name: str, v2_name: str, **kwargs):
        vertex1 = self.findVertex(v1_name)
        vertex2 = self.findVertex(v2_name)
        if vertex1 and vertex2:
            return False
        edge = Edge(vertex1, vertex2, **kwargs)
        if self.containsEdge(edge):
            vertex1.delEdge(edge)
            self._edgeCount -= 1
            return True
        return False

    def containsEdge(self, edge: Edge):
        v1 = self.findVertex(edge.getStart().getName())
        if v1:
            if edge in v1.edgesIter():
                return True
        return False

    def edgesIter(self):
        result = list()
        for vertex in self.verticesIter():
            result += list(vertex.edgesIter())
        return iter(result)

    def vertexEdgesIter(self, v_name):
        vertex = self.findVertex(v_name)
        if vertex:
            return vertex.edgesIter()
        else:
            return None

    def __iter__(self):
        return self.verticesIter()

    def __str__(self):
        result = str(len(self)) + "点："
        for vertex in self._verticesDict:
            result += ' ' + str(vertex)
        result += '\n'
        result += str(self.sizeofEdges()) + "边："
        for edge in self.edgesIter():
            result += '\n' + str(edge)
        return result


if __name__ == "__main__":
    v1 = Vertex('福州')
    v2 = Vertex('桂林')
    e1 = Edge(v1, v2, money=100)
    g = Digraph()
    g.addVertex(v1)
    g.addVertex(v2)
    g.addEdge(e1)
    print(g)
    pass
