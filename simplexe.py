import numpy as np
from probleme import Probleme_standard
from tableau import Tableau


def simplexe(pb,base):


	# Construction du tableau a partir des donnees du probleme


	A = pb.A
	b = pb.b.reshape(pb.b.size,1) # on met le vecteur en b en colonne
	c = pb.c
	c = np.append(c,0) # ajout du 0 dans derniere ligne derniere colonne du tableau
	tab_matrix = np.vstack((np.hstack((A,b)),c)) # concatenation de A, b et c pour former le tab du simplexe
	tab = Tableau(tab_matrix)

	

def pivot(A,b,d,critere="naturel"):
	if critere=="naturel":
		return pivot_nat(A,b,d)
	elif critere=="bland":
		return privot_bland(A,b,d)
	else:
		print("Critere {0} n'existe pas, application critere naturel".format(critere))
		return pivot(A,b,d)
	argmin = 0
	mini = b[0]/vec[0]
	for i in range(vec.size):
		if vec[i]<0:
			continue
		else:
			t = b[i]/vec[i]
			if t<mini:
				mini = t
				argmin = i
	return argmin

def pivot_nat(A,b,d):
	entrante = np.argmin(d) # plus petit j ou d est le plus petit
	sortante = 0
	vec = A[:,entrante]
	mini = b[0]/vec[0]
	for i in range(b.size):
		if vec[i]<0:
			continue
		else:
			t = b[i]/vec[i]
			if t<mini:
				mini = t
				sortante = i
	return [sortante,entrante]


def resoudre(pb):
	base = [pb.c.size-1-k for k in range(pb.b.size)]
	base.sort()
	print(base)
	x = simplexe(pb,base)

def main():
	A = np.array([[1,1,1,0],[1,2,0,1]])
	b = np.array([3,2])
	c = np.array([-3,4,0,0])
	pb = Probleme_standard(A,b,c)
	pb.affiche()
	resoudre(pb)

if __name__ == "__main__":
	main()