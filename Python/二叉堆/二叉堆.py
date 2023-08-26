'''
# ADT BinaryHeap
BinaryHeap():创建 一个空二叉堆对象
insert(k):将新key加入到堆中
findMin():返回堆中的最小项
delMin():
isEmpty():
size():返回堆中key的个数
buildHeap(list):从一个key列表创建新堆
'''



from Python.pythonds.trees.binheap import BinHeap

bh = BinHeap()
bh.insert(5)
bh.insert(7)
bh.insert(3)
bh.insert(11)
print(bh.delMin())
print(bh.delMin())
print(bh.delMin())
print(bh.delMin())