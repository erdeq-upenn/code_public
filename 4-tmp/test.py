# import pandas as pd
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
%matplotlib inline

x = np.arange(50)
y = np.random.rand(50)
plt.plot(x,y);
Z = np.array([[1+2j,1+3j],[5+6j,3+8j]])

class animal(object):
    def __init__(self,name,sound):
        self.name = name
        self.sound = sound

    def getName(self):
        return self.name

    def getSound(self):
        return self.sound

    def __str__(self):
        return "%s is %s" %(self.name,self.sound)

a = animal('dog','bark')

class dog(animal):
    def __init__(self,name,legs):
        animal.__init__(self,name,"bark")
        self.legs  = 4

print(a)

from fractions import *
import math


class Fractions:
    """Some comment
    In a galaxy far, far away~"""
    def __init__(self, nom, denom):
        self.nom = nom
        self.denom = denom
        self.__reduce()

    def __reduce(self):
        GCD = math.gcd(self.nom, self.denom)
        self.nom, self.denom = self.nom // GCD, self.denom // GCD

    def __str__(self):
        if self.nom/self.denom >= 1:
            integer = self.nom // self.denom
            flt = Fractions(self.nom % self.denom, self.denom)
            if flt.nom == 0:
                return str(integer)
            else:
                return str(integer)+' '+str(flt)
        else:
            return str(self.nom)+'/'+str(self.denom)

    def __add__(self, other):
        nom = self.nom*other.denom + self.denom*other.nom
        denom = self.denom * other.denom
        return Fractions(nom, denom)

    def __sub__(self, other):
        nom = self.nom*other.denom - self.denom*other.nom
        denom = self.denom * other.denom
        return Fractions(nom, denom)

    def __truediv__(self, other):
        nom, denom = self.nom*other.denom, self.denom*other.nom
        return Fractions(nom, denom)

    def __mul__(self, other):
        nom, denom = self.nom * other.nom, self.denom * other.denom
        return Fractions(nom, denom)

    def __copy__(self):
        return Fractions(self.nom, self.denom)

    def __pow__(self, power, modulo=None):
        ret = self.__copy__()

        if power == 0:
            return Fractions(1,1)
        elif power < 0:
            for _ in range(abs(power)-1):
                ret *= self
            return Fractions(1,1)/ret
        else:
            for _ in range(abs(power)):
                ret *= self
            return ret

    def __eq__(self, other):
        return self.nom == other.nom and self.denom == other.denom

    def astuple(self):
        return self.nom, self.denom

    def destroy(self):
        self.nom = None
        self.denom = None


myf1 = Fractions(1,2)
myf2 = Fractions(3,4)
print(myf1==myf2)
cc= myf1.__add__(myf2)
print(cc)
nom = 1*4 + 2*3
denom = 2*4
nom/denom
myf2.destroy()


###############
# rod cutting problem
import sys
sys.setrecursionlimit(100) #增大递归次数限制
p = [1, 5, 8, 9, 10, 17, 17, 20, 24, 30] #价格表
def cut_rod(p, n):
    # this is O(2^n)
    if n == 0: #递归终止条件
        return 0
    q = -1
    for i in range(n):
        q = max(q, p[i] + cut_rod(p, n-i-1)) #递归比对所有i的收益，求最大值
    return q
%timeit cut_rod(p,4)
s = []
for i in range(len(p)):
    s.append(cut_rod(p,i+1))
s
##################
memo = [ -1 for _ in range(len(p)) ]
def cut_rod2(p, n):
    if n == 0:
        return 0
    if memo[n-1] > 0: #memo的下标从0开始，而n是自然下标需要变换
        return memo[n-1]
    q = -1
    for i in range(n):
        q = max(q, p[i] + cut_rod2(p, n-i-1))
    memo[n-1] = q
    return q
%timeit cut_rod2(p,10)
memo
#################

p = [1, 5, 8, 9, 10, 17, 17, 20, 24, 30]
n = len(p)
r = [ 0 for _ in range(n+1) ] #此处使用自然下标，0即为长度为0的钢条
def bottom_up_cut_rod(p, n):
    for j in range(1, n+1): #规模从小到大求解所有子问题
        #此处的求解方法与自顶向下相同
        q = -1
        for i in range(1, j+1):
            q = max(q, p[i-1] + r[j-i])
        r[j] = q
    return r[n]
bottom_up_cut_rod(p,4)

##################
p = [1, 5, 8, 9, 10, 17, 17, 20, 24, 30]
def my_rod(p,n):
    r = [0 for _ in range(n+1)]
    s= [0 for _ in range(n+1)]
    # r[0] = 0

    for j in range(1,n+1):
        q = -1
        for i in range(1,j+1):
            # q = max(q, p[i-1] + r[j-i])
            if q< p[i-1] + r[j-i]:
                q = p[i-1] + r[j-i]

                s[j] = i
        r[j] = q
    return (r,s)
my_rod(p,9)
