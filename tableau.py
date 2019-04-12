import numpy as np
class Tableau:

	def __init__(self,A):
		self.tab = np.array(A,dtype=float)
		self.nb_lines = A.shape[0]
		self.nb_cols = A.shape[1]

	def add_lines(self,i,j,coef=1):
		"""
		Additionne la ligne j * coef à la ligne i

		"""
		for k in range(self.nb_cols):
			self.tab[i][k] += self.tab[j][k]*coef

	def mult_line(self,i,coef):
		for k in range(self.nb_cols):
			self.tab[i,k] *= coef

	def get_line(self,i):
		return self.tab[i]

	def get_column(self,j):
		return self.tab[:,j]

	def get_element(self,i,j):
		return self.tab[i,j]

	def is_positive(self,i,exclude_last=True):
		if exclude_last:
			comp = [x>=0 for x in self.tab[i][:-1]]
		else:
			comp = [x>=0 for x in self.tab[i]]
		return all(comp)

		
	def __str__(self):
		return np.array_str(self.tab)



def main():
	A = np.array([[3,4,5],[6,7,-1]])
	tab = Tableau(A)
if __name__ == "__main__":
	main()