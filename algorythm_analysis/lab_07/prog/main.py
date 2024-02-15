from time import process_time, time
from copy import deepcopy
from matplotlib import pylab
from random import randrange, choice
from time import time, time_ns 
import datetime


class treeNode(object):
	def __init__(self, value):
		self.value = value
		self.l = None
		self.r = None
		self.h = 1

class AVLTree(object):
    avl = 0
    worst_h = -1
    worst_num = None
    def insert(self, root, key):
	
        if not root:
            return treeNode(key)
        elif key < root.value:
            root.l = self.insert(root.l, key)
        else:
            root.r = self.insert(root.r, key)

        root.h = 1 + max(self.getHeight(root.l), self.getHeight(root.r))

        b = self.getBal(root)
        
        if b > 1 and key < root.l.value:
            return self.rRotate(root)

        if b < -1 and key > root.r.value:
            return self.lRotate(root)

        if b > 1 and key > root.l.value:
            root.l = self.lRotate(root.l)
            return self.rRotate(root)

        if b < -1 and key < root.r.value:
            root.r = self.rRotate(root.r)
            return self.lRotate(root)

        return root

    def lRotate(self, z):
        y = z.r
        if (y != None):
            T2 = y.l
            
            y.l = z
            z.r = T2
            
            z.h = 1 + max(self.getHeight(z.l), self.getHeight(z.r))
            y.h = 1 + max(self.getHeight(y.l), self.getHeight(y.r))
        return y

    def rRotate(self, z):
            
        y = z.l
        if (y != None):
            T3 = y.r
            y.r = z
            z.l = T3
        
            z.h = 1 + max(self.getHeight(z.l), self.getHeight(z.r))
            y.h = 1 + max(self.getHeight(y.l), self.getHeight(y.r))
        
        return y

    def getHeight(self, root):
        if not root:
            return 0

        return root.h

    def getBal(self, root):
        if not root:
            return 0

        return self.getHeight(root.l) - self.getHeight(root.r)
    
    def find(self, root, key):
        self.avl = 0
        if not root:
            return None
        else:
            return self._find(key, root)
    def _find(self, key, node):
        if not node:
            return self.avl
        self.avl += 1
        if key == node.value:
            return self.avl
        
        self.avl += 2
        if key < node.value:
            return self._find(key, node.l)
        
        #self.avl += 1
        if key > node.value:
            return self._find(key, node.r)
        
        
        return self.avl
    def preOrder(self, root):
        if not root:
            return

        print("{0} ".format(root.value), end="")
        self.preOrder(root.l)
        self.preOrder(root.r)
    def height_worst(self, root):
        if not root:
            return
        self.worst_h = root.h
        self.worst_num = root.value
        self._height_worst(root.l)
        self._height_worst(root.r)
        
        print(self.worst_h, self.worst_num)
        return self.worst_num
        
    
    def _height_worst(self, root):
        if not root:
            return
        if (root.h < self.worst_h):
            self.worst_h = root.h
            self.worst_num = root.value
        self._height_worst(root.l)
        self._height_worst(root.r)

def BinarySearch(key, list_keys):
        l, r = 0, len(list_keys) - 1
        k = 0
        #print("searching for ", key)
        while l <= r:
            middle = (r + l) // 2
            elem = list_keys[middle]
            #print("now at ", elem)
            #print("k - ", k)
            k += 1
            if elem == key:
                return k
            #print("elem not key +1")
            k +=1
            if elem < key:
                #print("elem  < key +1")
                l = middle + 1
            elif elem > key:
                #print("elem  > key +2")
                k+=1
                r = middle - 1
            else:
                k += 1
                print("not found")
                break
        
        return k

def main():
    tree = AVLTree()
    root = None
    mass = []
    
    #while (True):
    #    a = input("enter num: ")
    #    try:
    #        i = int(a)
    #    except:
    #        break
    #    mass.append(i)
    
    #for a in mass:
    #    root = tree.insert(root, a)
    
    values = [128, 256, 512, 1024, 2048]
    #128, 256, 512, 1024, 2048
    print("in mass\n")
    print("     | ", "  tree(ns)"," | ", "  binary(ns)  ")

    for v in values:
        tree = AVLTree()
        root = None
        mass = []
        
        for i in range(v):
            app =  randrange(1000000)
            mass.append(app)
            root = tree.insert(root, app)
        
        mass.sort()
        finder = root.value
        finder2 = mass[(len(mass) - 1) // 2]
        req = tree.find(root, finder)    
        req2 = BinarySearch(finder2, mass)
        
        print(v," | ", req ," | ", req2, "   - best")
        
        finder = 10000000
        req = tree.find(root, finder)
        req2 = BinarySearch(finder, mass)
        
        print(v," | ", req ," | ", req2, "   - worst")
    
        
main()