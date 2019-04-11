import numpy as np
class Tableau:

	def __init__(self,A):
		self.tab = A
		self.nb_lines = A.shape[0]
		self.nb_cols = A.shape[1]

	def add_lines(self,i,j):
		"""
		Additionne la ligne j à la ligne i

		"""
		for k in range(self.nb_cols):
			self.tab[i][k] += self.tab[j][k]

	def mult_lines(self,i,coef):

		for k in range(self.nb_cols):
			self.tab[i] *= coef

	def get_line(self,i):
		return self.tab[i]

	def is_positive(self,i,exclude_last=True):
		if exclude_last:
			comp = [x>=0 for x in self.tab[i][:-1]]
		else:
			comp = [x>=0 for x in self.tab[i]]
		print(comp)
		return all(comp)

		
	def __str__(self):
		return np.array_str(self.tab)



def main():
	A = np.array([[3,4,5],[6,7,-1]])
	tab = Tableau(A)
	print(tab.is_positive(1))
if __name__ == "__main__":
	main()