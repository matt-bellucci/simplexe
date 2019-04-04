import numpy as np
from simplexe import *

class DimError(Exception):
	def __init__(self,sizeA,sizeB,sizeC):
		self.sizeA=sizeA
		self.sizeB=sizeB
	def __str__(self):
		return "Erreur dimensions, A : {0}, b : {1} et c : {2}".format(self.sizeA,self.sizeB,self.sizeC)

class Probleme_standard:

	def __init__(self,A,b,c):
		if 1 in A.shape:
			raise DimError(A.shape,b.shape)
		else:
			self.A = A
		if b.ndim == 1 and b.size==A.shape[0]:
			self.b = b
		else:
			raise DimError(A.shape,b.shape,c.shape)
		if c.ndim == 1 and c.size == A.shape[1]:
			self.c = c
		else:
			raise DimError(A.shape,b.shape,c.shape)

	def affiche(self):
		print("Inf z = ",end="")
		for i in range(self.c.size-1):
			print("{0} * x{1} + ".format(self.c[i],i),end='')
		print("{0} * x{1}".format(self.c[i+1],i+1))
		print("Avec : ")
		for n in range(self.A.shape[0]):
			j = 0
			for i in range(self.A.shape[1]-1):
				print("{0} * x{1} + ".format(self.A[n][i],j),end='')
				j += 1
			print("{0} * x{1} = {2}".format(self.A[n][i+1],j,self.b[n]))
		print("x >= 0")

	def resoudre(self):
		base = [self.c.size-1-k for k in range(self.b.size)]
		base.sort()
		print(base)
		x = simplexe(self,base)

def main():
	A = np.array([[1,1,1,0],[1,2,0,1]])
	b = np.array([3,2])
	c = np.array([-3,4,0,0])
	pb = Probleme_standard(A,b,c)
	pb.affiche()
	pb.resoudre()

if __name__ == "__main__":
	main()