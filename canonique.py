import numpy as np
from probleme import Probleme_standard

class Probleme_canonique:

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
			print("{0} * x{1} + ".format(self.c[i],i+1),end='')
		print("{0} * x{1}".format(self.c[i+1],i+2))
		print("Avec : ")
		for n in range(self.A.shape[0]):
			j = 1
			for i in range(self.A.shape[1]-1):
				print("{0} * x{1} + ".format(self.A[n][i],j),end='')
				j += 1
			print("{0} * x{1} <= {2}".format(self.A[n][i+1],j,self.b[n]))
		print("x >= 0")

	def canon2stand(self):

		nb_contraintes = self.b.shape[0]
		id = np.eye(nb_contraintes)
		new_A = np.concatenate((self.A, id), axis=1)
		zeros = np.zeros(nb_contraintes)
		new_c = np.concatenate((self.c,zeros))
		return Probleme_standard(new_A,self.b,new_c)


def main():
	A = np.array([[1,1,1,0],[1,2,0,1]])
	b = np.array([3,2])
	c = np.array([-3,4,0,0])
	pb = Probleme_canonique(A,b,c)
	pb.affiche()
	pb2 = pb.canon2stand()
	pb2.affiche()

if __name__ == "__main__":
	main()
