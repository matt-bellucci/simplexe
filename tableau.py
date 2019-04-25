import numpy as np
class Tableau:
	"""
	Cree un objet qui permet de manipuler un tableau du simplexe et donc faciliter
	l'implementation de l'algorithme

	Attributes
	----------
	tab : numpy.ndarray
		Matrice contenant tous les coefficients du tableau du simplexe
	nb_lines : int
		Le nombre de lignes de tab
	nb_cols : int
		Le nombre de colonnes de tab
	"""

	def __init__(self,A):
		self.tab = np.array(A,dtype=float)
		self.nb_lines = A.shape[0]
		self.nb_cols = A.shape[1]

	def add_lines(self,i,j,coef=1):
		"""
		Remplace la ligne j par l'addition de ligne i*coef + ligne j

		Methode qui permet d'ajouter a la ligne j, la ligne i qui a ete multipliee par un coef
		qui par defaut est a 1

		Parameters
		----------
		i : int
			Le numero de la ligne que l'on va multiplier puis additionner a la ligne j
		j : int
			Le numero de la ligne qui va etre modifiee lors de l'addition
		coef : float
			Le coefficient par lequel on va multiplier la ligne i avant d'additionner cette
			derniere a la ligne j

		"""
		for k in range(self.nb_cols):
			self.tab[i][k] += self.tab[j][k]*coef

	def mult_line(self,i,coef):
		"""
		Multiplie tous les coeffs de la ligne i par le coefficient coef
		"""
		for k in range(self.nb_cols):
			self.tab[i,k] *= coef

	def get_line(self,i):
		return self.tab[i]

	def get_column(self,j):
		return self.tab[:,j]

	def get_element(self,i,j):
		return self.tab[i,j]

	def is_positive(self,i,exclude_last=True,axis=0):
		"""
		Retourne un booleen vrai si tous les elements d'une ligne ou colonne sont positifs, faux sinon

		Parameters
		----------
		i : int
			Le numero de la ligne ou de la colonne a etudier
		exclude_last : boolean
			Si vrai, on etudie pas le dernier element de la liste, dans le cas du tableau du simplexe,
			cela permet de ne pas prendre en compte les valeurs du Second Membre par exemple
		axis : (0,1)
			0 : etudie la ligne i
			1 : etudie la colonne i
		"""
		if axis == 0:
			return is_positive(self.tab[i],exclude_last=exclude_last)
		elif axis == 1:
			return is_positive(self.tab[:,i],exclude_last=exclude_last)

		
	def __str__(self):
		return np.array_str(self.tab)

def is_positive(array,exclude_last=True):
	"""
	Retourne vrai si la liste contient que des coefficients positifs,
	exclude_last permet de ne pas etudier le dernier coefficient de la liste

	"""
	if exclude_last:
		comp = [x>=0 for x in array[:-1]]
	else:
		comp = [x>=0 for x in array]
	return all(comp)

def main():
	A = np.array([[3,4,5],[6,7,-1]])
	tab = Tableau(A)
if __name__ == "__main__":
	main()