from abc import abstractmethod


class AbstractCollection(object):
    """抽象集合类.

    这个类描述抽象的集合
    负责引入和初始化self._size变量，在所有集合类中都使用这个变量
    这个类还包含了所有集合可用的最通用的方法：isEmpty, __len__和__add__
    “最通用”意味着它们的实现不需要由子类来修改
    最后，AbstractCollection类中还包含了__str__和__eq__方法的默认实现

    """
    __slots__ = '_size'

    def __init__(self, sourceCollection=None):
        """AbstractCollection类的初始化方法

        Args:
            sourceCollection: 接收一个可迭代参数，将其放置到本集合中，不传入时默认为None

        """
        self._size = 0
        if sourceCollection:
            for item in sourceCollection:
                self.add(item)

    @abstractmethod
    def add(self, item):
        pass

    def isEmpty(self):
        return len(self) == 0

    def __len__(self):
        """返回集合的长度."""
        return self._size

    def __str__(self):
        """返回集合的字符串输出形式."""
        return '[' + ','.join(map(str, self)) + ']'

    def __add__(self, other):
        """重载集合'+'号运算符.

        Args:
            other: 一个能转换为AbstractCollection类的对象，作为加数之一。

        Return:
            返回相加后的集合
        """
        result = type(self)(self)
        for item in other:
            result.add(item)
        return result

    def __eq__(self, other):
        """重载'=='号运算符.

        Args:
            other: 一个用于比较对象。

        Return:
            返回False的情况：
                other与此对象类型不匹配
                other与此对象类型匹配但长度不同
                other与此对象类型匹配但内容存在不相同
            返回True的情况：
                other就是此对象本身
                其他非False的情况

        """
        if self is other: return True
        if type(self) != type(other) or len(self) != len(other):
            return False
        otherIter = iter(other)
        for item in self:
            if item != next(otherIter):
                return False
        return True


if __name__ == "__main__":
    pass
