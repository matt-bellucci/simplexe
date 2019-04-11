import numpy as np
from probleme import Probleme_standard
from tableau import Tableau


def simplexe(pb,base):

	max_ite = 1

	# Construction du tableau a partir des donnees du probleme

	A = pb.A
	b = pb.b.reshape(pb.b.size,1) # on met le vecteur en b en colonne
	c = pb.c
	c = np.append(c,0) # ajout du 0 dans derniere ligne derniere colonne du tableau
	tab_matrix = np.vstack((np.hstack((A,b)),c)) # concatenation de A, b et c pour former le tab du simplexe
	tab = Tableau(tab_matrix)

	# Demarrage iterations

	ite = 0
	while ite<max_ite and not tab.is_positive(tab.nb_lines-1):
		print("==========Ite {0}=============".format(ite+1))
		# chercher pivot
		print(tab)
		col = pivot(tab)
		print(col)
		print()
		# actualiser base
		# mettre pivot a 1
		# colonne du pivot a 0

		ite += 1


def pivot(tab,critere="naturel"):
	c = np.array(tab.get_line(tab.nb_lines-1)[:-1])

	if critere == "bland":
		col = pivot_bland(c)
	else:
		col = pivot_naturel(c)
	return col

def pivot_naturel(c):

	return np.argmin(c)

def pivot_bland(c):

	return np.where(c<0)[0][0]
	
def resoudre(pb):
	base = [pb.c.size-1-k for k in range(pb.b.size)]
	base.sort()
	print(base)
	x = simplexe(pb,base)

def main():
	A = np.array([[1,1,1,0],[1,2,0,1]])
	b = np.array([3,2])
	c = np.array([-3,-4,0,0])
	pb = Probleme_standard(A,b,c)
	pb.affiche()
	resoudre(pb)

if __name__ == "__main__":
	main()