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
