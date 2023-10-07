#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time : 2023/9/24 15:31
# @Author :wyb
from collections import deque    # 在遍历的时候使用而已，其实并不需要
class TreeNode():
    def __init__(self):       # 这是没有设置父连接的版本
        self.data=0
        self.left=None        # 左孩子
        self.right=None       # 右孩子
        self.height=0         # 节点高度（这里设置所有节点的初始高度为0，后续会根据情况调整，根节点的高度会随之增加）

class BTree():
    def __init__(self):
        self.root=None
    def __Max(self,h1,h2):       # 比较左右孩子的高度，返回最大的那个
        if h1>h2:
            return h1
        elif h1<=h2:
            return h2

    def __LL(self,r):#左左情况，向右旋转     r是第一个高度差不满足的节点
        node=r.left
        r.left=node.right
        node.right=r
        r.height=self.__Max(self.getHeight(r.right),self.getHeight(r.left))+1
        node.height=self.__Max(self.getHeight(node.right),self.getHeight(node.left))+1
        return node            # 返回的是最开始r的左孩子，也是现在子树中的根节点
    def __RR(self,r):#右右，左旋           r是第一个高度差不满足条件的节点
        node = r.right
        r.right = node.left
        node.left = r
        r.height = self.__Max(self.getHeight(r.right), self.getHeight(r.left)) + 1
        node.height = self.__Max(self.getHeight(node.right), self.getHeight(node.left)) + 1
        return node            # 返回的是最开始r的右孩子，也是现在子树中的根节点
    def __LR(self,r):#左右，先左旋再右旋       r是第一个高度差不满足条件的节点
        r.left=self.__RR(r.left)           # 对r的左孩子进行左旋
        return self.__LL(r)                # 对r进行右旋，随即返回
    def __RL(self,r):#右左，先右旋再左旋       r是第一个高度差不满足条件的节点
        r.right=self.__LL(r.right)         # 对r的右孩子进行右旋
        return self.__RR(r)                # 对r进行左旋，随即返回
    def __insert(self,data,r):
        if r==None:               # 假入没有根节点，就新创建一个二叉树，插入值作为根节点的值
            node=TreeNode()
            node.data=data
            return node
        elif data==r.data:        # 假设插入值和根节点相同，那么就直接返回根节点
            return r
        elif data<r.data:         # 假设插入值比根节点的值要小，使用递归迭代，
            r.left=self.__insert(data,r.left)
            if self.getHeight(r.left)-self.getHeight(r.right)>=2:    # 如果左孩子的高度 比 右孩子的高度 大于等于2；简单的说其实是在判定是在左孩子的子树进行插入
                if data<r.left.data:    # 插入数值比左孩子要小（即在左子树中插入），使用右旋
                    r=self.__LL(r)
                else:                   # 插入数值比右孩子要大（即在右子树中插入），使用左旋-右旋
                    r=self.__LR(r)
        else:
            r.right=self.__insert(data,r.right)
            if self.getHeight(r.right)-self.getHeight(r.left)>=2:    # 如果右孩子的高度 比 左孩子的高度 大于等于2；简单的说其实是在判定是在右孩子的子树进行插入
                if data>r.right.data:    # 插入数值比右孩子要大（即在右子树中插入），使用左旋
                    r=self.__RR(r)
                else:                    # 插入数值比左孩子要小（即在左子树中插入），使用右旋-左旋
                    r=self.__RL(r)
        r.height=self.__Max(self.getHeight(r.left),self.getHeight(r.right))+1      # 修正树的根节点的深度
        return r

    # 删除data节点
    def __delete(self,data,r):
        if r==None:                 # 假如节点为空，就返回
            print("don't have %d"%data)
            return r
        elif r.data==data:          # 当节点的值和删除值相同时
            if r.left==None:        #如果被删除的节点只有右子树，直接将右子树赋值到此节点
                return r.right
            elif r.right==None:     #如果被删除的节点只有左子树，直接将左子树赋值到此节点
                return r.left
            else:#如果同时有左右子树
                if self.getHeight(r.left)>self.getHeight(r.right):  #左子树高度大于右子树
                    # 找到左子树的最右节点（最大值） 返回节点值 并删除该节点
                    node=r.left
                    while(node.right!=None):
                        node=node.right
                    r=self.__delete(node.data,r)       # 调用自身删除node
                    r.data=node.data
                    return r
                else:                           # 右子树高度大于左子树
                    node=r.right
                    # 找到右子树的最小节点（最小值） 返回节点值 并删除该节点
                    while node.left!=None:
                        node=node.left
                    r=self.__delete(node.data,r)       # 调用自身删除node
                    r.data=node.data
                    return r
        elif data<r.data:                 # 当删除值小于根节点的值时
            r.left=self.__delete(data,r.left)           # 在左子树中删除,使用递归删除
            if self.getHeight(r.right)-self.getHeight(r.left)>=2:   # 删除后，如果右子树高度与左子树高度相差超过1
                if self.getHeight(r.right.left)>self.getHeight(r.right.right):
                    r=self.__RL(r)            # 第一个错误点在右孩子的左子树中，使用右旋-左旋
                else:
                    r=self.__RR(r)            # 第一个错误点在右孩子的右子树中，使用左旋
        elif data>r.data:               # 当删除值大于根节点的值时
            r.right=self.__delete(data,r.right)         # 右子树中删除
            if self.getHeight(r.left)-self.getHeight(r.right)>=2:       # 左子树与右子树高度相差超过1
                if self.getHeight(r.left.right)>self.getHeight(r.left.left):
                    r=self.__LR(r)            # 第一个错误点在左孩子的右子树中，使用左旋-右旋
                else:
                    r=self.__LL(r)            # 第一个错误点在左孩子的左子树中，使用右旋
        r.height=self.__Max(self.getHeight(r.left),self.getHeight(r.right))+1             # 根节点的高度为 左右孩子节点最大的那个+1
        return r
    # 前序遍历
    def __show(self,root):
        if root!=None:
            print(root.data,end=',')
            self.__show(root.left)
            self.__show(root.right)
        else:
            return 0
    # 中序遍历
    def in_order(self, root):
        if root:
            self.in_order(root.left)
            print(root.data, end=',')
            self.in_order(root.right)
    # 层次遍历
    def level_order(self,root):
        queue = deque()
        queue.append(root)  # 将根节点放到队列之中
        while len(queue) > 0:  # 只要队列不空
            node = queue.popleft()  # 队头出队
            print(node.data, end=',')
            if node.left:  # 出队的节点存在左孩子，就把左孩子入队
                queue.append(node.left)
            if node.right:  # 如果存在右孩子，就把右孩子入队
                queue.append(node.right)


    def Insert(self,data):               # 插入操作
        self.root=self.__insert(data,self.root)           #  把新插入的节点从根节点开始比较
        return self.root           # 返回根节点
    def Delete(self,data):               # 删除操作
        self.root=self.__delete(data,self.root)           # 从根节点开始寻找，找到要删除的节点位置
        return self.root

    # 求结点的高度
    def getHeight(self,node):
        if node==None:
            return -1
        #print node
        return node.height

    def Show(self):
        self.__show(self.root)
        print('\n')
        self.in_order(self.root)
        print('\n')
        self.level_order(self.root)
