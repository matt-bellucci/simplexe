import numpy as np

class DimError(Exception):
	"""
	Classe qui permet de gerer un probleme de dimensions dans la classe Probleme_standard
	"""
	def __init__(self,sizeA,sizeB,sizeC):
		self.sizeA=sizeA
		self.sizeB=sizeB
	def __str__(self):
		return "Erreur dimensions, A : {0}, b : {1} et c : {2}".format(self.sizeA,self.sizeB,self.sizeC)

class Probleme_standard:
	"""
	Classe qui permet de convertir un ensemble de matrices en un probleme standard d'optimisation lineaire

	Cette classe prend 1 matrice et 2 vecteurs en entree, la matrice represente les coefficients
	des variables pour chaque contrainte, le premier vecteur est les valeurs de l'autre cote de l'egalite
	des contraintes. Le dernier vecteur represente les coefficients des variables pour la fonction cout.
	On considerera que l'on cherche toujours des valeurs positives. La contrainte xi >= 0 n'a pas besoin 
	d'etre incluse dans les entrees

	Example
	-------
	On a le probleme d'optimisation suivant : 
	Min z = 3*x1 - 2*x2
	x1 + x2 + x3 = 5
	x1 - 2*x2 + x4 = 2
	x >= 0
	Donne la matrice 
	A = [[1 1 1 0]
		 [1 -2 0 1]
		 ]
	b = [5 2]
	c = [3 -2 0 0]

	Attributes
	----------
	A : numpy.ndarray
		La matrice des coefficients des contraintes
	b : numpy.ndarray
		Le vecteur des contraintes de l'autre cote de l'egalite
	c : numpy.ndarray
		Le vecteur des coefficients de la fonction cout a minimiser, tel que 
		<c,x> le produit scalaire de c par x (x le vecteur des valeurs des variables)
		donne la valeur de la fonction cout

	"""

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
		"""
		Fonction permettant d'afficher le probleme contenu par l'instance de cette classe
		"""
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


def main():
	A = np.array([[1,1,1,0],[1,2,0,1]])
	b = np.array([3,2])
	c = np.array([-3,4,0,0])
	pb = Probleme_standard(A,b,c)
	pb.affiche()

if __name__ == "__main__":
	main()